from django.db import models

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django_email_sender.models import EmailBaseLog
from utils.generator import generate_code


# Create your models here.
class CustomUser(BaseUserManager):
    
    def create_user(self, username, email, password=None, **extra_fields):
        self._validate_fields(username, email)
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username=username,
                                email=email, 
                                password=password, **extra_fields)
    
    def _validate_fields(self, username, email):
        if not username:
            raise ValueError("The username cannot be none, expected a string but got None")
        
        if not email:
            raise ValueError("The email cannot be none. Expected an email but got none")
    
   
    
class User(AbstractBaseUser, PermissionsMixin):
    
    first_name        = models.CharField(max_length=40)
    surname           = models.CharField(max_length=10)
    username          = models.CharField(unique=True, db_index=True)
    email             = models.EmailField(unique=True, db_index=True, max_length=40)
    is_active         = models.BooleanField(default=True)    
    is_staff          = models.BooleanField(default=False)
    is_admin          = models.BooleanField(default=False)
    is_superuser      = models.BooleanField(default=False)
    last_login        = models.DateTimeField(auto_now=True)
    joined_on         = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD    = "email"
    REQUIRED_FIELDS   = ["username", "first_name", "surname"]
    objects           = CustomUser()
    
    def __str__(self):
        return f"{self.first_name.capitalize()} {self.surname.capitalize()}"
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def full_name(self):
        return f"{self.first_name.capitalize()} {self.surname.capitalize()}"
    
    @classmethod
    def get_by_email(cls, email):
        return cls._get_by_field_name(field_name="email", field_value=email)
    
    @classmethod
    def get_by_username(cls, username):
        return cls._get_by_field_name(field_name="username", field_value=username)
    
    @classmethod
    def _get_by_field_name(cls, field_name: str, field_value: str):
        
        try:
            match field_name.lower():
                case "email":
                    return cls.objects.get(email=field_value)
                case "username":
                    return cls.objects.get(username=field_value)
        except cls.DoesNotExist:
            return None
        
   
        

class Verification(models.Model):
    
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification")
    code                   = models.CharField(max_length=9, db_index=True, default=generate_code())
    num_of_days_to_expire  = models.PositiveSmallIntegerField(default=1)
    description           = models.CharField(max_length=255)
    verify_by              = models.DateTimeField(blank=True, null=True, editable=False)
    created_on             = models.DateTimeField(auto_now_add=True)
    modified_on            = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'code']),
        ]

    def __str__(self):
        return self.code
    
    @property
    def full_name(self):
        return self.user.full_name
    
    @classmethod
    def get_by_username_and_code(cls, code, username):
        
        if not code or not username:
            return None
        try:
            return cls.objects.get(user__username=username.lower(), code=code)
        except cls.DoesNotExist:
            return None

        
    def is_code_expired(self):
        return timezone.now() > self.verify_by
       
    def save(self, *args, **kwargs):
        
        current_time = timezone.now()
        self.verify_by = current_time + timedelta(days=self.num_of_days_to_expire)
        super().save(*args, **kwargs)


class EmailLogger(EmailBaseLog):
    pass