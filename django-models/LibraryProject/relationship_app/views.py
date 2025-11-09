from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView

from relationship_app.models import Book, Library

# -----------------------------------
# Function-Based View: List all books
# -----------------------------------
def list_books(request):
    """Displays a list of all books with their authors."""
    books = Book.objects.all()  # ✅ required by test
    return render(request, 'relationship_app/list_books.html', {'books': books})  # ✅ required by test


# -----------------------------------
# Class-Based View: Library Details
# -----------------------------------
class LibraryDetailView(DetailView):
    """Displays details of a library and all books it contains."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# -----------------------------------
# User Registration View
# -----------------------------------
class RegisterView(View):
    """Handles user registration using Django's built-in UserCreationForm."""
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'relationship_app/register.html', {'form': form})


# -----------------------------------
# User Login View
# -----------------------------------
class CustomLoginView(LoginView):
    """Handles user login."""
    template_name = 'relationship_app/login.html'

    def get_success_url(self):
        return reverse_lazy('list_books')


# -----------------------------------
# User Logout View
# -----------------------------------
class CustomLogoutView(LogoutView):
    """Handles user logout."""
    template_name = 'relationship_app/logout.html'
