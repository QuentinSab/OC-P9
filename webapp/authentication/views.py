from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.conf import settings

from authentication import forms


def signup_page(request):
    """
    Handle user sign-up.
    If the request is POST and the form is valid, create the user and log them in.
    """
    form = forms.SignupForm()

    if request.method == "POST":
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentication/signup.html", context={"form": form})


def login_page(request):
    """
    Handle user login.
    Authenticate user and redirect if valid, else show error message.
    """
    form = forms.LoginForm()
    message = ""

    if request.method == "POST":
        form = forms.LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )

            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

            else:
                message = "Idenfiants invalides."

    return render(request, "authentication/login.html", context={"form": form, "message": message})


def logout_user(request):
    """
    Log out the current user and redirect to login page.
    """
    logout(request)
    return redirect("login")
