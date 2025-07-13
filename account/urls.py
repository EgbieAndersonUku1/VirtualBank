from django.urls import path

from . import views

urlpatterns = [
    path('save/', view=views.save_profile_details, name="save_profile_details" ),
    path('update/', view=views.update_profile_details, name="update_profile_details"),
    path('get/', view=views.get_profile_details, name="get_profile_data"),
    path('fund/bankaccount/', view=views.add_fund_to_bank_account, name="add_funds_to_bank_account"),
    path('fund/wallet/', view=views.add_fund_to_wallet, name="add_funds_to_wallet")
    
 
]
