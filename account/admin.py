from django.contrib import admin

from .models import BankAccount, Profile,  Wallet, BankAccount


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display         = ["id", "email", "first_name", "surname", "maritus_status", "created_on", "modified_on"]
    list_display_links   = ["id", "first_name", "surname", "email"]
    list_per_page        = 25
    list_filter          = ["maritus_status", "gender"]
    search_fields        = ["first_name", "surname", "email", "country", "mobile", "state"]
    readonly_fields      = ["created_on", "modified_on", "profile_id", "email"]


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



class WalletAdmin(admin.ModelAdmin):
    list_display       = ["pin", "user_email", "amount", "total_cards", "maximum_cards", "last_amount_received", "created_on", "modified_on"]
    list_display_links = ["pin", "user_email"]
    list_filter        = ["wallet_id"]
    list_per_page      = 25
    search_fields      = ["wallet_id", "amount", "maximum_cards", "pin"]
    readonly_fields    = ["wallet_id", "created_on", "modified_on", "user_email"]

    @admin.display(description="Pin")
    def pin(self, obj):
        return obj.pin
    
    def user_email(self, obj):
        return obj.user.email
   
    fieldsets = [
        (
            None,
            {
                "fields": ["wallet_id", "amount", "last_amount_received", "user","bank_account"],
            },
        ),
        (
            "Cards",
            {

                "fields": ["total_cards", "maximum_cards", "cards"],
            },
        ),

        (
            "Additional information",
            {
                "fields": ["created_on", "modified_on"]
            }
        )
    ]



class BankAdmin(admin.ModelAdmin):
    list_display        = ["id", "username", "email", "sort_code", "account_number", "amount"]
    list_display_links  = ["id", "username", "email"]
    list_per_page       = 25
    readonly_fields     = ["created_on", "modified_on", "bank_id", "sort_code", "account_number"]

    @admin.display(description="Username")
    def username(self, obj):
        return obj.username
    
    @admin.display(description="Email")
    def email(self, obj):
        return obj.email


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(BankAccount, BankAdmin)
