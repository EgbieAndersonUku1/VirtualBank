

from django.urls import path

from . import views

urlpatterns = [
    path('', view=views.home, name="home" ),
    path("register/", view=views.register, name="register"),
    path("login/", view=views.login, name="login"),
    path("verify/<username>", view=views.verify_registration_code, name="verify_registration_code"),
]

