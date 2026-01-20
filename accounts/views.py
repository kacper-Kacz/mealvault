from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import SignUpForm
from .models import Profile

def premium_context(request):
    is_premium = False
    if request.user.is_authenticated:
        try:
            is_premium = request.user.profile.is_premium
        except Profile.DoesNotExist:
            is_premium = False
    return {"is_premium": is_premium}

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data["password1"])
            if user:
                login(request, user)
                messages.success(request, "Account created. Welcome!")
                return redirect("accounts:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Logged in successfully.")
            return redirect("core:home")
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("core:home")

@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")
