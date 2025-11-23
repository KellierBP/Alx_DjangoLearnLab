from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form handling.
    This form includes validation to prevent malicious inputs.
    """
    name = forms.CharField(max_length=100, required=True, help_text="Enter your name")
    email = forms.EmailField(required=True, help_text="Enter a valid email address")
    message = forms.CharField(widget=forms.Textarea, required=True, help_text="Enter your message")

    def clean_name(self):
        """
        Custom validation for name field to prevent XSS.
        """
        name = self.cleaned_data['name']
        # Basic sanitization - in production, use bleach or similar
        if '<' in name or '>' in name:
            raise forms.ValidationError("Invalid characters in name")
        return name

    def clean_message(self):
        """
        Custom validation for message field.
        """
        message = self.cleaned_data['message']
        if len(message) > 1000:
            raise forms.ValidationError("Message too long")
        return message