import json

from django.db import IntegrityError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


from .views_helper import api_response, profile_to_dict
from .models import Profile


@csrf_protect
@login_required
def save_profile_details(request):
 
    if request.method != "POST":
        return api_response(error="Only POST method is allowed", status_code=405)
  
    user = request.user
    if Profile.objects.filter(user=user).exists():
        return api_response(error="Profile for this user already exists", status_code=409)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        error_msg = f'Invalid JSON data: {str(e)}'
        return api_response(error=error_msg, status_code=400)
    
    try:
        # Handle Profile
        profile = Profile.objects.create(user=request.user,
    
                        first_name=data.get("firstName"),
                        surname=data.get("surname"),
                        mobile=data.get("mobile"),
                        gender=data.get("gender"),
                        maritus_status=data.get("maritusStatus"),
                        country=data.get("country"),
                        state=data.get("state"),
                        postcode= data.get("postcode"),
                        signature=data.get("signature"),
                        identification_documents=data.get("identificationDocuments")
                        
                )

    except IntegrityError as e:
        error_msg = f"A database error occurred. Possible duplicate or invalid data: {str(e)}"
        return api_response(error=error_msg, status_code=409, data=data)

    except Exception as e:
        error_msg = f"Something went wrong on the server: Additional info {e}"
        return api_response(error=error_msg, status_code=500, data=data)
    return api_response(status_code=201, message="Successfully saved the data", success=True, data=profile_to_dict(profile))        
       
   
      