from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

# Create your views here.


@csrf_protect
@login_required
def add_fund_to_wallet(request):
    pass 


@csrf_protect
@login_required
def add_fund_to_bank_account(request):
    pass 

