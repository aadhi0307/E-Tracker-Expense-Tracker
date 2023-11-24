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



def reset_password_request(request):
    if request.method == 'POST':
        # Assume the user submits their username for password reset
        username = request.POST.get('username')
        user = get_object_or_404(get_user_model(), username=username)

        # Generate and save a reset token
        reset_token = PasswordResetToken(user=user, token=generate_reset_token())
        reset_token.save()

        # Instead of sending an email, you might display the token on the webpage
        reset_link = f"/reset-password/{reset_token.token}/"
        return render(request, 'reset_password_request_success.html', {'reset_link': reset_link})

    return render(request, 'reset_password_request_form.html')

def reset_password(request, token):
    reset_token = get_object_or_404(PasswordResetToken, token=token)

    # Check if the token is still valid (e.g., not expired)
    if reset_token.created_at + timezone.timedelta(hours=1) >= timezone.now():
        # Allow the user to reset their password
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            # Update the user's password
            reset_token.user.set_password(new_password)
            reset_token.user.save()

            # Delete the used reset token
            reset_token.delete()

            # Redirect to the sign-in page after successful password reset
            messages.success(request,"Password updated successfully")
            return redirect(signin)  # Update 'signin' with your actual URL or view name
            
        else:
            return render(request, 'reset_password_form.html', {'token': token})
    else:
        # Token has expired, handle accordingly
        return render(request, 'reset_password_expired.html')
