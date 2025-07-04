from django.urls import path

from . import views

urlpatterns = [
    path('save/', view=views.save_profile_details, name="save_profile_details" ),
    
 
]
