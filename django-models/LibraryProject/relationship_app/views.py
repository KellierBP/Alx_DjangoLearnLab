from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponseForbidden


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
@permission_required('relationship_app.can_add_book')
def add_book(request):
    """
    Allows users with 'can_add_book' permission to add a new book.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        
        if title and author_id:
            from .models import Author
            author = get_object_or_404(Author, id=author_id)
            Book.objects.create(title=title, author=author)
            return redirect('list_books')
    
    from .models import Author
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    """
    Allows users with 'can_change_book' permission to edit an existing book.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        
        if title and author_id:
            from .models import Author
            author = get_object_or_404(Author, id=author_id)
            book.title = title
            book.author = author
            book.save()
            return redirect('list_books')
    
    from .models import Author
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})


@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    """
    Allows users with 'can_delete_book' permission to delete a book.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})


