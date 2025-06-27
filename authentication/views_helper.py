import logging
from django.conf import settings
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_sender_constants import LoggerType
from django.shortcuts import redirect
from django.forms import Form

from django.http import HttpRequest

from .forms import VerifyEmailForm, AddPinForm
from .models import Verification, EmailLogger, User

logger = logging.getLogger("email_sender")
            
            
def extract_code_from_verification_form(form: VerifyEmailForm) -> str:
    return _extract_code_from_form(form, VerifyEmailForm)
  

def extract_pin_from_form(form: AddPinForm) -> str:
    return _extract_code_from_form(form, AddPinForm)


def _extract_code_from_form(form: Form, form_class: type[Form]) -> str:
    if not isinstance(form, form_class):
        raise ValueError(
            f"The form is not an instance of {form_class.__name__}. "
            f"Expected an instance of {form_class.__name__} but got {type(form).__name__}."
        )
    return "".join(field.value() for field in form if field.value())





def send_verification_email(user: User, verification: Verification, url: str, subject: str = "Verify your email"):
    return _send_email_helper(subject=subject,
                              html_template="emails/register.html",
                              text_template="emails/register.txt",
                              user=user,
                              verification=verification,
                              verification_link=url
                              )



def resend_verification_email(user: User, 
                              verification: Verification, 
                              url: str, 
                              subject: str = "Expired code, please verify your email again"):
    
    return _send_email_helper(subject=subject,
                              html_template="emails/expired_email.html",
                              text_template="emails/expired_email.txt",
                              user=user,
                              verification=verification,
                              verification_link=url
                              )
    



def _send_email_helper(subject : str, 
                       html_template: str, 
                       text_template: str, 
                       user: User, 
                       verification: Verification, 
                       verification_link: str):
    
    if not isinstance(user, User):
        raise ValueError(f"The user is not an instance of User. Expected a user instance but got type {type(user)}")
    
    if not isinstance(verification, Verification):
        raise ValueError(f"The verification is not an instance of Verification. Expected a verification instance but got type {type(verification)}")    
    
    verification.description = subject

    email = EmailSenderLogger.create()
    (
            
        email.add_email_sender_instance(EmailSender.create())
        .config_logger(log_level=LoggerType.INFO, logger=logger)
        .add_log_model(EmailLogger)
        .enable_email_meta_data_save()
        .start_logging_session()
        .from_address(settings.EMAIL_HOST_USER)
        .to(user.email)
        .with_subject(subject)
        .with_context({"username": user.username, 
                       "verification_code": verification.code,
                       "verification_link": verification_link}
                      )
        .with_html_template(html_template)
        .with_text_template(text_template)
        .send()
    )
    return email


def redirect_to_pin_page_if_not_set_else_home(request):

    if not isinstance(request, HttpRequest):
        raise ValueError(f"The request is not an instance of HttpRequest. Expected an instance of request but got type {type(request)}")

    if not request.user.pin:
        return redirect("add_pin")
    return redirect("home")
