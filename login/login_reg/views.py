from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django import forms
from django.contrib.auth.forms import UserCreationForm
import pyrebase

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyAYu-nGMlvOveGr9F1jLw0JI-T1_7bZbDo",
    "authDomain": "loginregister-aaa51.firebaseapp.com",
    "databaseURL": "https://loginregister-aaa51-default-rtdb.firebaseio.com",
    "projectId": "loginregister-aaa51",
    "storageBucket": "loginregister-aaa51.appspot.com",
    "messagingSenderId": "790120905661",
    "appId": "1:790120905661:web:e06394ee94b5c54aadf0d4",
    "measurementId": "G-46VBHK6T08"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login_reg:register')  # Redirect to the home page or any other desired page
    else:
        form = AuthenticationForm()
    return render(request, 'login_reg/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_reg:login')  # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'login_reg/register.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            auth.send_password_reset_email(email)
            messages.success(request, 'Password reset email has been sent.')
            return redirect('login_reg:login')
        except Exception as e:
            messages.error(request, 'An error occurred while sending the password reset email. Please try again.')
            return redirect('login_reg:forgot_password')
    else:
        form = PasswordResetForm()
    return render(request, 'login_reg/forgot_password.html', {'form': form})

