from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Document
from .services import retrieve


@override_settings(GROQ_API_KEY="", OPENAI_API_KEY="")
class DocumentWorkflowTests(TestCase):
    def test_retrieval_returns_only_relevant_passages(self):
        text = "The launch date is 14 October.\n\nThe office is closed on Sundays."
        results = retrieve("When is the launch date?", text)

        self.assertEqual(len(results), 1)
        self.assertIn("14 October", results[0])

    def test_text_document_can_be_uploaded_and_queried(self):
        upload = SimpleUploadedFile(
            "project-notes.txt",
            b"The launch date is 14 October. The owner is the product team.",
            content_type="text/plain",
        )
        response = self.client.post(reverse("home"), {"file": upload})
        document = Document.objects.get()
        self.assertRedirects(response, reverse("document", args=[document.pk]))
        self.assertTrue(document.file.size)

        response = self.client.post(reverse("document", args=[document.pk]), {"question": "When is the launch date?"})
        self.assertEqual(response.status_code, 302)
        document.refresh_from_db()
        self.assertEqual(document.questions.count(), 1)
        saved_question = document.questions.first()
        self.assertIn("relevant passages", saved_question.answer)
        self.assertIn("14 October", saved_question.sources[0])
