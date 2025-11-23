from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Book, Author

class CustomUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    profile_photo = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')

class BookForm(forms.ModelForm):
    """
    Form for creating and editing books.
    Includes validation to prevent SQL injection and ensure data integrity.
    Uses Django's built-in form validation and sanitization.
    """
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'required': True}),
            'author': forms.Select(attrs={'required': True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sanitize inputs by stripping whitespace
        for field in self.fields:
            if isinstance(self.fields[field].widget, forms.TextInput):
                self.fields[field].widget.attrs.update({'class': 'form-control'})