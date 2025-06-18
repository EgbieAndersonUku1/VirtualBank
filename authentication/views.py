import logging

from django.shortcuts import redirect, render
from django.urls import reverse
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_sender_constants import LoggerType
from django.conf import settings
from django.contrib import messages

from .forms import RegisterForm, LoginForm, VerifyEmailForm
from .models import Verification, EmailLogger

from .views_helper import extract_code_from_verification_form, send_verification_email, resend_verification_email

# Create your views here.

def home(request):
    # change this later but for now use register form
    return render(request, "authentication/register.html")


def register(request):
    
    form    = RegisterForm()
    context = {}   
    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
                       
            verification = Verification()
            
            user             = form.save(commit=False)
            verification_link = request.build_absolute_uri(reverse('verify_registration_code', args=[user.username]))
            
            email = send_verification_email(user=user, verification=verification, url=verification_link)
           
            if email.is_email_sent:
                user.save()
                verification.user = user
                verification.save()
                
                messages.add_message(request, messages.SUCCESS, "A request has been sent to your registered email")
                return redirect(reverse("login"))   
    
    context["form"] = form
    return render(request, "authentication/register.html", context=context)


def login(request):
    form   = LoginForm()
    context = {
        "form": form
    }
    return render(request, "authentication/login.html", context=context)


def verify_registration_code(request, username):
    
    context   = {}
    form      = VerifyEmailForm()
    error_msg = None
    
    if request.method == "POST":
        form = VerifyEmailForm(request.POST)
        
        if form.is_valid():
            code = extract_code_from_verification_form(form)  
            
            verification = Verification.get_by_username_and_code(username, code)

            if not verification:
                error_msg = "The code entered is invalid"
            elif verification.is_code_expired:
                error_msg = "The code has expired. Another one has been sent to your email"
            
         
            # to add more here
        
    context = {
        "form": VerifyEmailForm,
        "username": username,
        "error_msg": error_msg
    }
    return render(request, "authentication/verify.html", context=context)