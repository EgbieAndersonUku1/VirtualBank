import logging

from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from .models import Verification
from .forms import RegisterForm, LoginForm, VerifyEmailForm
from .views_helper import (extract_code_from_verification_form, 
                           send_verification_email, 
                           resend_verification_email
                           )

from .utils.utils import create_verification_url

# Create your views here.


def register(request):
    
    form    = RegisterForm()
    context = {}   
    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
                       
            verification = Verification()
            
            user              = form.save(commit=False)
            verification_link =  create_verification_url(request, user.username)
            
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

    # add the code to login in
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
    
            verification = Verification.get_by_username_and_code(code, username)

            if not verification:
                error_msg = "The code entered is invalid"
                messages.add_message(request, messages.ERROR, error_msg)

            elif not verification and request.user.is_authenticated:
                messages.add_message(request, messages.ERROR, "You verification code has already been verified")

            elif verification.is_code_expired:
                error_msg = "The code has expired. Another one has been sent to your email"
                messages.add_message(request, messages.ERROR, error_msg)

                verification.regenerate_code()
                resend_verification_email(user=verification.user, 
                                          verification=verification,
                                          url=create_verification_url(request, verification.user.username)
                                          )

            else:
                verification.set_email_to_verified()
                verification.delete()
                messages.add_message(request, messages.SUCCESS, "You have successfully verified your email address")
                return redirect(reverse("login"))
            
        
    context = {
        "form": VerifyEmailForm,
        "username": username,
      
    }
    return render(request, "authentication/verify.html", context=context)