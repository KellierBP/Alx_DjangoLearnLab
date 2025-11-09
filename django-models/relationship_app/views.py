from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

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
        # Redirect to the book list after login
        return reverse_lazy('list_books')


# -----------------------------------
# User Logout View
# -----------------------------------
class CustomLogoutView(LogoutView):
    """Handles user logout."""
    template_name = 'relationship_app/logout.html'
