from django import forms


class DocumentUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept": ".pdf,.docx,.txt"}))

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        if uploaded.size > 15 * 1024 * 1024:
            raise forms.ValidationError("Please upload a file smaller than 15 MB.")
        if uploaded.name.rsplit(".", 1)[-1].lower() not in {"pdf", "docx", "txt"}:
            raise forms.ValidationError("Supported formats: PDF, DOCX, and TXT.")
        return uploaded


class QuestionForm(forms.Form):
    question = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={
        "placeholder": "Ask something precise about this document…",
        "autocomplete": "off",
    }))
