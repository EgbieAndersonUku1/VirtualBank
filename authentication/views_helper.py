import logging
from django.conf import settings
from django_email_sender.email_logger import EmailSenderLogger
from django_email_sender.email_sender import EmailSender
from django_email_sender.email_sender_constants import LoggerType

from .forms import VerifyEmailForm
from .models import Verification, EmailLogger, User

logger = logging.getLogger("email_sender")
            
            
def extract_code_from_verification_form(form: VerifyEmailForm) -> bool:
    if not isinstance(form, VerifyEmailForm):
        raise ValueError(f"""The form is not an instance of VerifyEmailForm. 
                         Expected a form with instance VerfiyEmailForm but got {type(VerifyEmailForm)}""")
    
    return "".join([field.value() for field in form if field.value()])



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
        raise ValueError(f"The verification is not an instance of User. Expected a user instance but got type {type(verification)}")    
    
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