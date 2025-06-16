import logging

from django.shortcuts import redirect, render
from django.urls import reverse
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_sender_constants import LoggerType
from django.conf import settings
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from .models import Verification, EmailLogger

# Create your views here.

def home(request):
    return render(request, "authentication/register.html")


def register(request):
    
    form    = RegisterForm()
    context = {}   
    if request.method == "POST":
        
        form = RegisterForm(request.POST)
        
        if form.is_valid():
           
            logger = logging.getLogger("email_sender")
            
            verification = Verification()
            
            user = form.save(commit=False)
            verification_link = request.build_absolute_uri(reverse('verify_registration_code', args=[user.username]))
            
            email = EmailSenderLogger.create()
            (
            
                email.add_email_sender_instance(EmailSender.create())
                .config_logger(log_level=LoggerType.INFO, logger=logger)
                .add_log_model(EmailLogger)
                .enable_email_meta_data_save()
                .start_logging_session()
                .from_address(settings.EMAIL_HOST_USER)
                .to(user.email)
                .with_subject("Verify your email")
                .with_context({"username": user.username, "verification_code": verification.code, "verification_link": verification_link})
                .with_html_template("emails/register.html")
                .with_text_template("emails/register.txt")
                .send()
            )

            

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
    return render(request, "authentication/verify.html")