from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import DocumentUploadForm, QuestionForm
from .models import Document, Question
from .services import answer_question, extract_text


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = form.cleaned_data["file"]
            try:
                text = extract_text(uploaded)
            except Exception:
                form.add_error("file", "We couldn't read that file. Please try a text-based PDF, DOCX, or TXT file.")
            else:
                if not text.strip():
                    form.add_error("file", "No readable text was found in this document.")
                else:
                    document = Document.objects.create(file=uploaded, original_name=uploaded.name, extracted_text=text)
                    return redirect("document", pk=document.pk)
    else:
        form = DocumentUploadForm()
    return render(request, "knowledge/home.html", {"form": form, "documents": Document.objects.all()[:6]})


@require_http_methods(["GET", "POST"])
def document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data["question"]
            answer, sources = answer_question(question_text, document.extracted_text)
            Question.objects.create(document=document, text=question_text, answer=answer, sources=sources)
            return redirect("document", pk=document.pk)
    else:
        form = QuestionForm()
    return render(request, "knowledge/document.html", {
        "document": document,
        "form": form,
        "questions": document.questions.all()[:8],
    })
