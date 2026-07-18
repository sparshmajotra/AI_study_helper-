import re
from collections import Counter
from pathlib import Path

from django.conf import settings

WORD = re.compile(r"[a-zA-Z0-9']+")


def extract_text(uploaded_file):
    """Extract text from one supported uploaded file."""
    extension = Path(uploaded_file.name).suffix.lower()
    uploaded_file.seek(0)
    if extension == ".txt":
        text = uploaded_file.read().decode("utf-8", errors="replace")
        uploaded_file.seek(0)
        return text
    if extension == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        uploaded_file.seek(0)
        return text
    if extension == ".docx":
        from docx import Document as DocxDocument
        doc = DocxDocument(uploaded_file)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        uploaded_file.seek(0)
        return text
    raise ValueError("Unsupported file format")


def chunks(text, size=900, overlap=180):
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    return [cleaned[i:i + size] for i in range(0, len(cleaned), size - overlap)]


def retrieve(question, document_text, limit=4):
    """Lightweight lexical retrieval; no vector database required for small documents."""
    question_terms = Counter(WORD.findall(question.lower()))
    ranked = []
    for index, chunk in enumerate(chunks(document_text)):
        words = Counter(WORD.findall(chunk.lower()))
        score = sum(words[term] * weight for term, weight in question_terms.items())
        if score:
            ranked.append((score, index, chunk))
    return [item[2] for item in sorted(ranked, reverse=True)[:limit]]


def answer_question(question, document_text):
    evidence = retrieve(question, document_text)
    if not evidence:
        return (
            "I couldn't find information in this document that answers that question. "
            "Try using terms that appear in the document.",
            [],
        )

    api_key = settings.GROQ_API_KEY or settings.OPENAI_API_KEY
    if api_key:
        try:
            from openai import OpenAI
            prompt = "\n\n---\n\n".join(evidence)
            client_options = {"api_key": api_key}
            model = settings.OPENAI_MODEL
            if settings.GROQ_API_KEY:
                # Groq implements the OpenAI-compatible Chat Completions API.
                client_options["base_url"] = "https://api.groq.com/openai/v1"
                model = settings.GROQ_MODEL
            response = OpenAI(**client_options).chat.completions.create(
                model=model,
                temperature=0.1,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer only from the supplied document excerpts. If they do not contain "
                            "the answer, say so clearly. Write in easy, everyday English: use short "
                            "sentences and explain technical terms briefly. Start with the direct answer, "
                            "then use no more than 5 short bullet points if extra detail helps. Keep the "
                            "whole answer under 140 words. Do not copy long passages or repeat information. "
                            "Cite supporting excerpts as [1], [2], etc."
                        ),
                    },
                    {"role": "user", "content": f"Question: {question}\n\nDocument excerpts:\n{prompt}"},
                ],
            )
            return response.choices[0].message.content.strip(), evidence
        except Exception:
            # Keep the document assistant usable if the optional provider is unavailable.
            pass

    return (
        "I found relevant passages, but an AI-generated summary is not available. "
        "Open the source passages below, or check that your Groq API key is configured correctly.",
        evidence,
    )
