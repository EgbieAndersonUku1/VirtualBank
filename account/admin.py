from django.contrib import admin
from django.http import HttpRequest
from simple_history.admin import SimpleHistoryAdmin

from .models import BankAccount, Profile,  Wallet, BankAccount, Card


# Register your models here.
class ProfileAdmin(SimpleHistoryAdmin):
    list_display         = ["id", "email", "first_name", "surname", "maritus_status", "created_on", "modified_on"]
    list_display_links   = ["id", "first_name", "surname", "email"]
    list_per_page        = 25
    list_filter          = ["maritus_status", "gender"]
    search_fields        = ["first_name", "surname", "email", "country", "mobile", "state"]
    readonly_fields      = ["created_on", "modified_on", "profile_id", "email"]


    fieldsets = [(None, {"fields": ["profile_id", "first_name", "surname", "email","mobile", "gender", "user"],},),
                ("Location", {"fields": ["country", "state", "postcode"],},),
                ("Identification documents", { "fields": ["signature", "identification_documents"]}
        )
    ]



class WalletAdmin(SimpleHistoryAdmin):
    list_display       = ["pin", "user_email", "amount", "total_cards", "maximum_cards", "last_amount_received", "created_on", "modified_on"]
    list_display_links = ["pin", "user_email"]
    list_filter        = ["wallet_id"]
    list_per_page      = 25
    search_fields      = ["wallet_id", "amount", "maximum_cards", "pin"]
    readonly_fields    = ["wallet_id", "created_on", "modified_on", "user_email"]

    def get_readonly_fields(self, request, obj=None):   
        readonly = ["wallet_id", "created_on", "modified_on", "user_email",]
        if obj:
            # Make amount read-only after creation
            readonly += ["user", "bank_account", "last_amount_received"]
        return readonly

    @admin.display(description="Pin")
    def pin(self, obj):
        return obj.pin
    
    def user_email(self, obj):
        return obj.user.email

    def get_fieldsets(self, request, obj=None):
        """
        Customize the fieldsets displayed in the admin form.

        This method allows you to specify which fields are shown
        when creating a new object versus editing an existing one.

        Parameters:
            request (HttpRequest): The current request object.
            obj (Model instance or None): The object being edited, or None if creating.

        Returns:
            list: A list of fieldset tuples to be used in the admin form.
        """
        if obj:
            # Allows fields listed as readonly to be editable when creating a new wallet
            # This is necessary because readonly fields are excluded by default on creation,
            # and since some of these fields are required by the model, omitting them would cause a failure.
            return [
                ("Wallet Information", {"fields": ["wallet_id", "amount", "last_amount_received", "user","bank_account"],}),
                ("Additional information", {"fields": ["created_on", "modified_on"]}),
            ]
        else:
            # Adding — show real account input fields
              return [("Wallet Information", {"fields": ["amount", "last_amount_received", "user","bank_account"]}),
                ("Cards", {"fields": ["total_cards", "maximum_cards",],}),
                ("Additional information", { "fields": ["created_on", "modified_on"] }),
            ]
   
 
class BankAdmin(SimpleHistoryAdmin):
    list_display        = ["id", "username", "email", "masked_sort_code", "masked_account_number", "amount", "created_on"]
    list_display_links  = ["id", "username", "email"]
    list_per_page       = 25
    search_fields       = ["username", "email"]

    def get_fieldsets(self, request, obj=None):
        """
        Customize the fieldsets displayed in the admin form.

        This method allows you to specify which fields are shown
        when creating a new object versus editing an existing one.

        Parameters:
            request (HttpRequest): The current request object.
            obj (Model instance or None): The object being edited, or None if creating.

        Returns:
            list: A list of fieldset tuples to be used in the admin form.
        """
        if obj:
            # Ensures that masked sort code and account number remain masked when editing.
            return [
                ("Bank Information", { "fields": ["bank_id", "masked_sort_code", "masked_account_number", "amount" ]}),
                ("Metadata", {"fields": ["created_on", "modified_on", "user"]}),
            ]
        else:
            # Allows fields listed as readonly to be editable when creating a new Bank account model.
            # This is necessary because readonly fields are excluded by default on creation,
            # and since some of these fields are required by the model, omitting them would cause a failure.
            return [
                ("Bank Information", { "fields": ["sort_code", "account_number", "amount"]}),
                ("Metadata", {"fields": ["created_on", "modified_on", "user"]}),
            ]

    def get_readonly_fields(self, request, obj=None):
        readonly = ["created_on", "modified_on"]
        if obj:
            readonly += ["bank_id", "masked_sort_code", "masked_account_number", "user"]
        return readonly

    @admin.display(description="Username")
    def username(self, obj):
        return obj.username
    
    @admin.display(description="Email")
    def email(self, obj):
        return obj.email
    
    @admin.display(description="Masked Sort Code")
    def masked_sort_code(self, obj):
        return obj.masked_sort_code
    
    @admin.display(description="Masked Account Number")
    def masked_account_number(self, obj):
        return obj.masked_account_number

    

class CardAdmin(SimpleHistoryAdmin):
    list_display         = ["id", "card_name", "masked_card_number", "masked_cvc", "expiry_month", "expiry_year", "card_type", "card_options"]
    list_display_links   = ["id", "card_name"]
    list_per_page        = 25
    list_filter          = ["card_type", "card_options"]
    search_fields        = ["card_name", "card_type", "card_options"]

    # Show correct fields depending on add/edit
    def get_fieldsets(self, request, obj=None):
        """
        Customize the fieldsets displayed in the admin form.

        This method allows you to specify which fields are shown
        when creating a new object versus editing an existing one.

        Parameters:
            request (HttpRequest): The current request object.
            obj (Model instance or None): The object being edited, or None if creating.

        Returns:
            list: A list of fieldset tuples to be used in the admin form.
        """

        # Ensures that masked card number remain masked when editing.

        if obj:  
            return [
                (None, { "fields": ["card_id", "card_name", "amount", "masked_card_number", "expiry_month", "expiry_year", "masked_cvc"]}),
                ("Card Options", {"fields": ["card_options", "card_type"]}),
                ("Account linkage", { "fields": ["bank_account", "wallet"]}),
                ("Meta", {"fields": ["created_on", "modified_on"]}),
            ]
        else:  
            
            # Creating new card 

            # Allows fields listed as readonly to be editable when creating a new card.
            # This is necessary because readonly fields are excluded by default on creation,
            # and since some of these fields are required by the model, omitting them would cause a failure.
            return [
                (None, {"fields": ["card_name", "card_number", "amount", "cvc", "expiry_month", "expiry_year",]}),
                ("Card Options", { "fields": ["card_options", "card_type"]}),
                ("Account linkage", { "fields": ["bank_account", "wallet"]}),
                ("Meta", {"fields": ["created_on", "modified_on"]}),
            ]

    def get_readonly_fields(self, request, obj=None):
        base = ["created_on", "modified_on"]
        if obj:
            return base + ["masked_card_number", "masked_cvc", "card_id", "bank_account", "wallet"]
        return base

    @admin.display(description="Masked Card Number")
    def masked_card_number(self, obj):
        return obj.masked_card_number

    @admin.display(description="Masked CVC Number")
    def masked_cvc(self, obj):
        return obj.masked_cvc


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(BankAccount, BankAdmin)
admin.site.register(Card, CardAdmin)