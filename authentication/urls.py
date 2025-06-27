
from django.urls import path

from . import views

urlpatterns = [
    path("register/", view=views.register, name="register"),
    path("login/", view=views.login_user, name="login"),
    path("logout/", view=views.logout_user, name="logout"),
    path("verify/<username>/", view=views.verify_registration_code, name="verify_registration_code"),
    path("add/pin/", view=views.add_pin, name="add_pin"),
]

