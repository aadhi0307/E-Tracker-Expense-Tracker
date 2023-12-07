from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from userapp.views import index
from django.shortcuts import render, redirect, get_object_or_404
from .models import PasswordResetToken, generate_reset_token
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(signin)  # Redirect to the home page or another desired page upon successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User authentication succeeded; log the user in
            login(request, user)
            return redirect(index)  # Redirect to the home page or another desired page upon successful sign-in
        else:
            # User authentication failed; display an error message
            error_message = "Invalid credentials. Please try again."
    else:
        error_message = None

    return render(request, 'signin.html', {'error_message': error_message})

def user_logout(request):
    logout(request)
    return redirect(signin)




