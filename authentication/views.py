from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "authentication/register.html")


def register(request):
    return render(request, "authentication/register.html")


def login(request):
    return render(request, "authentication/login.html")


def verify_registration_code(request, username):
    return render(request, "authentication/verify.html")