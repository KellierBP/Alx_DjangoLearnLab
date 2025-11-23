from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden


# ----------------------------
# Import models
# ----------------------------
from .models import Book
from .models import Library
from .forms import CustomUserCreationForm, BookForm

# ----------------------------
# Function-Based View: List all books
# ----------------------------
@permission_required('relationship_app.can_view', raise_exception=True)
def list_books(request):
    """
    Displays a list of all books with their authors.
    Requires 'can_view' permission.
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
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = CustomUserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# ----------------------------
# Role-based Views
# ----------------------------
def is_admin(user):
    return user.is_authenticated and user.profile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.profile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.profile.role == 'Member'

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_dashboard(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_dashboard(request):
    return render(request, 'relationship_app/member_view.html')


# ----------------------------
# Permission-Required Views for Book Operations
# ----------------------------
# These views enforce custom permissions defined in the Book model:
# - list_books: requires 'can_view' permission
# - add_book: requires 'can_create' permission
# - edit_book: requires 'can_edit' permission
# - delete_book: requires 'can_delete' permission
# Permissions are assigned to groups: Viewers, Editors, Admins
# Security: All forms use Django forms for input validation and sanitization to prevent SQL injection
@permission_required('relationship_app.can_create', raise_exception=True)
def add_book(request):
    """
    Allows users with 'can_create' permission to add a new book.
    Uses BookForm for secure input validation and sanitization.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    
    return render(request, 'relationship_app/add_book.html', {'form': form})


@permission_required('relationship_app.can_edit', raise_exception=True)
def edit_book(request, pk):
    """
    Allows users with 'can_edit' permission to edit an existing book.
    Uses BookForm for secure input validation and sanitization.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})


@permission_required('relationship_app.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    Allows users with 'can_delete' permission to delete a book.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})


