from django.db import models


class Document(models.Model):
    file = models.FileField(upload_to="documents/%Y/%m/%d")
    original_name = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.original_name


class Question(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=1000)
    answer = models.TextField()
    sources = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
