from simple_history.admin import SimpleHistoryAdmin
from django.contrib import admin
from .models import User, Verification, EmailLogger
from .forms import VerificationModelAdminForm


# Register your models here.

class UserAdmin(SimpleHistoryAdmin):
    
    list_display       = ["id", "username", "email", "joined_on", "last_login"]
    list_display_links = ["id", "username", "email"]
    list_per_page      = 25
    readonly_fields    = ["last_login", "joined_on"]
    search_fields      = ["username", "email", "first_name", "surname"]
    list_filter        = ["is_staff", "is_superuser", "is_admin", "is_email_verified"]

    fieldsets = [
        (
            "User information",
            {
                "fields": ["username", "email",  "first_name", "surname", "pin"],
            },
        ),
        (
            "Advanced options",
            {

                "fields": ["is_active", "is_staff", "is_email_verified", "is_admin", "is_superuser"],
            },
        ),
        (
            "Account information",
            
            {
              "fields": ["last_login", "joined_on"]  
            },
        )
        
    ]



    
class EmailLoggerAdmin(admin.ModelAdmin):
    
    list_display        = ["from_email", "to_email", "subject", "status", "sent_on", "created_on"]
    list_display_links  = ["from_email", "to_email"]
    readonly_fields     = ["sent_on", "created_on", "status", "from_email", "to_email", "subject", "email_body"]
    list_per_page       = 25
    search_fields       = ["from_email", "to_email"]
    list_filter         = ["status"]    
    
    
class VerificationAdminModel(admin.ModelAdmin):
    form                 = VerificationModelAdminForm
    list_display         = ["full_name", "code", "num_of_days_to_expire", "created_on", "verify_by"]
    list_display_links   = ["full_name", "code"]
    list_per_page        = 25
    search_fields        = ["user__username", "user__email", "user__first_name", "user__surname"]
    readonly_fields      = ["verify_by", "created_on"]    
  
    @admin.display(description="Full name")
    def full_name(self, obj):
        return obj.full_name
    
    
    
    
admin.site.register(User, UserAdmin)
admin.site.register(Verification, VerificationAdminModel)
admin.site.register(EmailLogger, EmailLoggerAdmin)