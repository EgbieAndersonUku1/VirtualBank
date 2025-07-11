from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Verification, User
from .forms import RegisterForm, LoginForm, VerifyEmailForm, AddPinForm
from .views_helper import (extract_code_from_verification_form, 
                           extract_pin_from_form,
                           send_verification_email, 
                           resend_verification_email,
                           redirect_to_pin_page_if_not_set_else_home
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
            
            user              = form.save()
            verification_link =  create_verification_url(request, user.username)
            
            email = send_verification_email(user=user, verification=verification, url=verification_link)
           
            if email.is_email_sent:

                verification.user = user
                verification.save()
                
                messages.add_message(request, messages.SUCCESS, "A request has been sent to your registered email")
                return redirect(reverse("login"))   
    
    context["form"] = form
    return render(request, "authentication/register.html", context=context)


def login_user(request):

    form = LoginForm()
 
    if request.method == "POST":
        
        form = LoginForm(request.POST)

        if form.is_valid():
            
            email    = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]
            message  = "The email and password is incorrect"
           
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if not user.is_email_verified:
                    message =  "You haven't verified your email address"
                else:
                    login(request, user)
                    return redirect_to_pin_page_if_not_set_else_home(request)
        
        messages.add_message(request, messages.ERROR, message)
          
         
    context = {
        "form": form
    }
    return render(request, "authentication/login.html", context=context)


@login_required(login_url="/login/")
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.", extra_tags="logout")
    messages.success(request, "Your session has been cleared. For added security, please close this browser or tab.")

    return redirect("home")


def verify_registration_code(request, username):
    
    context   = {}
    form      = VerifyEmailForm()
    error_msg = None
    
    if request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, "You verification code has already been verified")
        return redirect("home")
    
    if request.method == "POST":
        form = VerifyEmailForm(request.POST)
        
        if form.is_valid():
            code = extract_code_from_verification_form(form)  
    
            verification = Verification.get_by_username_and_code(code, username)

            if not verification:
                error_msg = "The code entered is invalid"
                messages.add_message(request, messages.ERROR, error_msg)     

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


@login_required(login_url="/login/")
def add_pin(request):
    
    form    = AddPinForm()
    context = {}
    if request.method == "POST":
        form = AddPinForm(request.POST)
        if form.is_valid():
            user = request.user
            user.pin = extract_pin_from_form(form)
            user.save()
            return redirect("home")

    context["form"] = form
    return render(request, "authentication/add_pin.html", context=context)