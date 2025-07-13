from django.urls import path

from . import views

urlpatterns = [
    path('bankaccount/', view=views.add_fund_to_bank_account, name="add_funds_to_bank_account"),
    path('wallet/', view=views.add_fund_to_wallet, name="add_funds_to_wallet")
    
 
]
