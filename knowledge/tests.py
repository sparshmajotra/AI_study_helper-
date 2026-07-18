from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Document


class DocumentWorkflowTests(TestCase):
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
