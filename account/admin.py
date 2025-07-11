from django.contrib import admin

from .models import BankAccount, Profile,  Wallet, BankAccount


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display         = ["id", "first_name", "surname", "email", "maritus_status", "created_on", "modified_on"]
    list_display_links   = ["id", "first_name", "surname", "email"]
    list_per_page        = 25
    list_filter          = ["maritus_status", "gender"]
    search_fields        = ["first_name", "surname", "email", "country", "mobile", "state"]
    readonly_fields      = ["created_on", "modified_on", "profile_id"]

    fieldsets = [
        (
            None,
            {
                "fields": ["profile_id", "first_name", "surname", "email","mobile", "gender", "user"],
            },
        ),
        (
            "Location",
            {

                "fields": ["country", "state", "postcode"],
            },
        ),

        (
            "Identification documents",
            {
                "fields": ["signature", "identification_documents"]
            }
        )
    ]



admin.site.register(Profile, ProfileAdmin)

