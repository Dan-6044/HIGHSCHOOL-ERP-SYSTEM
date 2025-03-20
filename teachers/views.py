from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout,  authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User

def teachers(request):
    return render(request, 'teachersLandingPage.html')

def tdashboard(request):
    return render(request, 'tdashboard.html')

def tenroll(request):
    return render(request, 'tenroll.html')

def tclasses(request):
    return render(request, 'tclasses.html')

def tattendance(request):
    return render(request, 'tattendance.html')

def logout_views(request):
    logout(request)  # Logs out the user
    return redirect('teachers')  # Redirect to the home page


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the new user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_id = user.id  # Get the user's ID

            # Log the user in automatically after registration
            login(request, user)
            return redirect('tdashboard')  # Redirect to home after successful registration
        else:
            # Pass the form errors to the template
            return render(request, 'auth.html', {'form': form, 'signup_errors': form.errors})

    else:
        form = SignupForm()

    return render(request, 'auth.html', {'form': form})

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ensure email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.", extra_tags="login_error")
            return redirect('register')

        # Get user by email
        user = User.objects.filter(email=email).first()

        if user:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                auth_login(request, authenticated_user)
                return redirect(reverse('tdashboard'))  # Redirect to dashboard
            else:
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'auth.html')  # Ensure the correct template name