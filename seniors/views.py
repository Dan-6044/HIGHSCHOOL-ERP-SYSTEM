from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout,  authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User


def admin(request):
    return render(request, 'adminLandingPage.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def sattendance(request):
    return render(request, 'Sattendance.html')

def sresult(request):
    return render(request, 'Sresult.html')

def sadminFee(request):
    return render(request, 'Sadminfees.html')

def logouts_view(request):
    logout(request)  # Logs out the user
    return redirect('admin')  # Redirect to the home page

def accessup(request):
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
            return redirect('dashboard')  # Redirect to home after successful registration
        else:
            # Pass the form errors to the template
            return render(request, 'access.html', {'form': form, 'signup_errors': form.errors})

    else:
        form = SignupForm()

    return render(request, 'access.html', {'form': form})

def accessin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ensure email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.", extra_tags="login_error")
            return redirect('accessin')

        # Get user by email
        user = User.objects.filter(email=email).first()

        if user:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                auth_login(request, authenticated_user)
                return redirect(reverse('dashboard'))  # Redirect to dashboard
            else:
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'access.html')  # Ensure the correct template name


