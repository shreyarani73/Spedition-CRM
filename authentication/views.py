from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

@login_required
def Dashboard(request):
    return render(request, "index.html", {})


def LoginHandler(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("authentication:home")
    else:
        message = "Failed login"
        return render(request, "login.html", {"message":message})


def logout(request):
    logout(request)
    return render(request, "login.html", {})