from django.shortcuts import render, redirect
from pip import main
from .forms import RegisterForm
from main.models import Theme
from django.contrib.auth import *

# Create your views here.


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})
