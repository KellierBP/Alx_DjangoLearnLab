from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.detail import DetailView


# ----------------------------
# Import models
# ----------------------------
from .models import Book
from .models import Library

# ----------------------------
# Function-Based View: List all books
# ----------------------------
def list_books(request):
    """
    Displays a list of all books with their authors.
    """
    books = Book.objects.all()  # ✅ required for tests
    return render(request, 'relationship_app/list_books.html', {'books': books})  # ✅ required for tests

# ----------------------------
# Class-Based View: Library Details
# ----------------------------
class LibraryDetailView(DetailView):
    """
    Displays details of a library and all books it contains.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# ----------------------------
# User Registration View
# ----------------------------
def register(request):
    """
    Handles user registration using Django's built-in UserCreationForm.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


