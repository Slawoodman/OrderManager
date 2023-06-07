from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import User


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("main")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "main")

        else:
            messages.error(request, "Username OR password is incorrect")
    context = {"page": page}
    return render(request, "users/login_reg.html", context)


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was sucssefully created")
            login(request, user)
            return redirect("main")
        else:
            messages.error(request, "An error dur registations")

    context = {"page": page, "form": form}
    return render(request, "users/login_reg.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "User was logged out ")
    return redirect("main")
