from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput
         (attrs={
             'class':'form-control','placeholder':'Enter your email'
         }) # Renders the input as a password field
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput
         (attrs={
             'class':'form-control','placeholder':'Enter your username'
         }) # Renders the input as a password field
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
         (attrs={
             'class':'form-control','placeholder':'password'
         }) # Renders the input as a password field
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
         (attrs={
             'class':'form-control','placeholder':'Confirm password'
         }) # Renders the input as a password field
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char in "!@#$%^&*()" for char in password1):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password1

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email
    
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your existing email',}))
    password = forms.CharField(label="New Password", widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your new password'}))
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'custom_password_reset_email.html'
    form_class = CustomPasswordResetForm
    success_url = '/password_reset/done/'  
