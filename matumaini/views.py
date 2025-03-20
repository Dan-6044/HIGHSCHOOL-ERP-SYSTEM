from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout,  authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User


def student(request):
    return render(request, 'studentLandingPage.html')

def sdashboard(request):
    return render(request, 'studentDashbaord.html')

def enroll(request):
    return render(request, 'enroll.html')

def classes(request):
    return render(request, 'classes.html')


def assignment(request):
    return render(request, 'assignment.html')

def result(request):
    return render(request, 'result.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('student')  # Redirect to the home page

def fee(request):
    return render(request, 'fee.html')


def adminFee(request):
    return render(request, 'adminfees.html')

def attendance(request):
    return render(request, 'attendance.html')

def signup(request):
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
            return redirect('sdashbaord')  # Redirect to home after successful registration
        else:
            # Pass the form errors to the template
            return render(request, 'signing.html', {'form': form, 'signup_errors': form.errors})

    else:
        form = SignupForm()

    return render(request, 'signing.html', {'form': form})

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ensure email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.", extra_tags="login_error")
            return redirect('signin')

        # Get user by email
        user = User.objects.filter(email=email).first()

        if user:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                auth_login(request, authenticated_user)
                return redirect(reverse('sdashbaord'))  # Redirect to dashboard
            else:
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'signin.html')  # Ensure the correct template name


