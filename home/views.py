from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from account.form import ProfileForm

# Create your views here.


@login_required(login_url="/login/")
def home(request):
    profile_form = ProfileForm()

    context = {
        "profile_form": profile_form,
    }
    return render(request, "index.html", context=context)
