
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from .utils.errors import ProfileAlreadyExistsError, UserDoesNotExistError
from .views_helper import (handle_profile_json,
                           update_changed_profile_fields, 
                            api_response
                            )
from .models import Profile
from .utils.utils import profile_to_dict



@csrf_protect
@login_required
def save_profile_details(request):
    """
    Handle a POST request from the frontend to save user profile details.

    This view is intended to be called via JavaScript (e.g. `fetch`) and delegates
    the creation of the profile to a helper function. Since the data is being sent
    as a POST It ensures that the request is authenticated and protected against 
    CSRF attacks.

    The actual logic for creating the profile is handled by the `create_profile` 
    closure, and serialisation is performed using `profile_to_dict`.

    Only users who do not already have a profile may create one. Each user can 
    only have one profile, if an Attempt to create a profile where one exists 
    a `ProfileAlreadyExistsError` will be raised.

    Returns:
        JsonResponse: A JSON response containing the saved profile data or an error.
    """

    def create_profile(data: dict, request: HttpRequest):
        """
        Create a new user profile if one does not already exist.

        Called by `handle_profile_json`, this function receives a dictionary
        containing user profile details and creates a new profile. If the
        user already has a profile, it raises a ProfileAlreadyExistsError.

        Note:
            The `data` dictionary must contain the following keys:

                - firstName
                - surname
                - mobile
                - gender
                - maritalStatus
                - country
                - state
                - postcode
                - signature
                - identificationDocuments

            If any of these keys are missing, `handle_profile_json` will raise an error.

        Parameters:
            data (dict): A dictionary containing the user profile details.
            request (HttpRequest): The request object, containing user info and HTTP method.

        Raises:
            ProfileAlreadyExistsError: If a profile for the user already exists.

        Returns:
            Profile: The newly created user profile object.
        """
        user = request.user
        if Profile.objects.filter(user=user).exists():
            raise ProfileAlreadyExistsError("Profile for this user already exists")
                
        profile = Profile.objects.create(
            user=request.user,
            first_name=data.get("firstName"),
            surname=data.get("surname"),
            mobile=data.get("mobile"),
            gender=data.get("gender"),
            maritus_status=data.get("maritusStatus"),
            country=data.get("country"),
            state=data.get("state"),
            postcode= data.get("postcode"),
            signature=data.get("signature"),
            identification_documents=data.get("identificationDocuments"),
        )
        return profile

    return handle_profile_json(request, create_profile, profile_to_dict)  
       
@csrf_protect
@login_required
def update_profile_details(request):
    """
    Handle a POST request from the frontend to update the user profile details.

    This view is intended to be called via JavaScript (e.g. `fetch`) and delegates
    the updation of the profile to a helper function. Since the data is being sent
    as a POST It ensures that the request is authenticated and protected against 
    CSRF attacks.

    The actual logic for updating the profile is handled by the `update_profile` 
    closure, and serialisation is performed using `profile_to_dict`.

    Only users who already have a profile can update their profile. if the user
    doesn't have a profile then fetch API will send the request to `save_profile_details`
    which in turn will create a new profile.

    Returns:
        JsonResponse: A JSON response containing the saved profile data or an error.
    """
    def update_profile(data: dict, request: HttpRequest):
        """
        Updates an existing user profile with modified fields.

        This function is called by `handle_profile_json` and receives a dictionary
        containing only the fields that have changed on the frontend. It updates 
        only those fields in the corresponding user profile.

        Note:
            The `data` dictionary includes only the modified fields, which ensures that
            only those fields are updated in the database.

        Parameters:
            data (dict): A dictionary containing the updated user profile fields.
            request (HttpRequest): The HTTP request object, containing user information.

        Raises:
            UserDoesNotExistError: If no profile exists for the current user.

        Returns:
            Profile: The updated user profile instance.
        """
        
        profile = Profile.get_by_user(request.user)
        if profile == None:
            raise UserDoesNotExistError("The user doesn't exist")

        profile = update_changed_profile_fields(data, profile)
        return profile
    
    return handle_profile_json(request, update_profile, profile_to_dict, update=True)  
    


@login_required
def get_profile_details(request):
    """
    Handles a GET request from the frontend to retrieve the user's profile details.

    This view is intended to be called via JavaScript (e.g. `fetch`) and returns the
    user's profile data as a JSON response. Since this is a read-only GET request, a
    CSRF token or decorator is not required.

    Returns:
        JsonResponse: A JSON response containing the user's profile data or an error
                    message if retrieval fails.
    """

    if request.method != "GET":
        return api_response(error="Only GET method is allowed", status_code=405)
    
    profile = Profile.get_by_user(request.user)

    if profile:
        updated_data = profile_to_dict(profile)

        return api_response(status_code=200, message="Successfully retrieved the data", success=True, data=updated_data)        
    
    return api_response(status_code=400, message="Failed to retrieve data", success=True, data={})    

 


