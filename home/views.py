from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from account.form import ProfileForm
from account.models import BankAccount

# Create your views here.


@login_required(login_url="/login/")
def home(request):

    profile_form = ProfileForm()
    bank_account = BankAccount.get_by_user(user=request.user)

    context = {
        "profile_form": profile_form,
        "bank_account": bank_account

    }
    return render(request, "index.html", context=context)
