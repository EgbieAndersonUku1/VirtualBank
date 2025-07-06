import json

from typing import Optional, Any
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpRequest

from .models import Profile
from .utils.errors import ProfileAlreadyExistsError, UserDoesNotExistError


def api_response( success: bool = False, 
                  message: str = '',
                  error: str = '', 
                  status_code: int = 200, 
                  update : bool = False,
                  data: Optional[Any] = None) -> JsonResponse:
    
    return JsonResponse({
        'SUCCESS': success,
        'MESSAGE': message,
        'ERROR': error,
        'DATA': data or {},
        'UPDATE': update

    }, status=status_code)



def profile_to_dict(profile):
    
    return {
        "firstName": profile.first_name,
        "surname": profile.surname,
        "mobile": profile.mobile,
        "gender": profile.gender,
        "maritusStatus": profile.maritus_status,
        "country": profile.country,
        "state": profile.state,
        "postcode": profile.postcode,
        "identificationDocuments": profile.identification_documents,
        "signature": profile.signature,
       
      
}


def handle_profile_json(request, func, extract_profile_data, update = False):
    """
    Handles a JSON-based POST request to create or update a user profile.

    A helper function utility function that processes incoming JSON data from a POST request, validates
    its structure, and delegates the creation or update logic to the provided `func`
    callable. The response includes either a success message with the profile data
    (serialised using `extract_profile_data`) or an appropriate error message.

    Parameters:
        request (HttpRequest): The HTTP request object, expected to contain JSON data in the body.
        func (callable): A function that performs the creation or update of the profile.
                        It should accept `data` (dict) and `request` as arguments and return a 
                        profile object.
        extract_profile_data (callable): A function used to serialise the profile object into a dictionary.
        update (bool): A flag to indicate whether the operation is an update (default is False).

    Returns:
        JsonResponse: A standardised JSON response indicating success or failure,
                    including a message, status code, and optionally the serialised data.

    Raises:
        Returns HTTP 400/409/500 responses depending on the exception raised:
            - JSONDecodeError: If the request body cannot be parsed.
            - ValueError: If the data is not a dictionary.
            - IntegrityError: If a database constraint is violated.
            - ProfileAlreadyExistsError: If attempting to create a duplicate profile.
            - UserDoesNotExistError: If no profile exists for the user.
            - Exception: For any other unexpected errors.
    """

    if not isinstance(request, HttpRequest):
        return api_response(error="Something went wrong, please try again later", status_code=500)
    
    if request.method != "POST":
        return api_response(error="Only POST method is allowed", status_code=405)
  
    try:
        data = json.loads(request.body.decode('utf-8'))
     
        if not isinstance(data, dict):
            raise ValueError(f"The data is not an instance of dictionary. Expected the data object to be type dictionary but got type {type(data)}")
        
        profile = func(data, request)
       
    except json.JSONDecodeError as e:
        error_msg = f'Invalid JSON data: {str(e)}'
        return api_response(error=error_msg, status_code=400)
    except ValueError as e:
        return api_response(error=str(e), status_code=400)       
    except IntegrityError as e:
        error_msg = f"A database error occurred. Possible duplicate or invalid data: {str(e)}"
        return api_response(error=error_msg, status_code=409, data=data)
    except ProfileAlreadyExistsError as e:
        return api_response(error=str(e), status_code=409)
    except UserDoesNotExistError as e:
        return api_response(error=str(e), status_code=409)
    except Exception as e:
        error_msg = f"Something went wrong on the server: Additional info {e}"
        return api_response(error=error_msg, status_code=500, data=data)
    
    return api_response(status_code=201, 
                        message="Successfully saved the data",
                        success=True, 
                        update=update,
                         data=extract_profile_data(profile)
                         )        
       


def update_changed_profile_fields(data: dict, profile: Profile):
    """
    Updates only the modified fields of a user profile based on frontend input.

    This function is used in conjunction with `update_profile_details` API function.
    It receives a dictionary containing only the fields that have changed on the frontend
    and updates the corresponding fields in the `Profile` model instance.

    The function first performs a mapping between frontend field names (typically in camelCase)
    and model field names (snake_case) to ensure that only the changed values are persisted
    to the database.

    Note:
        The `data` dictionary is expected to follow this structure:

            {
                "firstName": {
                    "changed": "New value",
                    "current": "Previous value"
                },
                ...
            }

        Only the `changed` value is written to the model.

    Parameters:
        data (dict): A dictionary containing the fields that have been modified,
                    along with their old and new values.
        profile (Profile): The profile instance to be updated.

    Returns:
        Profile: The updated profile instance (saved if any changes were made).
    """

    profile_translation_mapping =  {
        "firstName": "first_name",
        "surname": "surname",
        "mobile": "mobile",
        "gender": "gender",
        "maritusStatus": "maritus_status",
        "country": "country",
        "state": "state",
        "postcode": "postcode",
        "identificationDocuments": "identification_documents",
        "signature": "signature",
    }

    is_changed = False

    for field in data:
        
        updated_field = data[field].get("changed")
        profile_field = profile_translation_mapping.get(field)

        if hasattr(profile, profile_field):
            if not is_changed:
                is_changed = True
            setattr(profile, profile_field, updated_field)
    
    if is_changed:
        profile.save()
    
    return profile

