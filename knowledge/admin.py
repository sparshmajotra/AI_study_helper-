from django.contrib import admin
from .models import Document, Question


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("original_name", "created_at")
    search_fields = ("original_name",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "document", "created_at")
    search_fields = ("text", "answer")
