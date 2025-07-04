from typing import Optional, Any
from django.http import JsonResponse



def api_response( success: bool = False, 
                  message: str = '',
                  error: str = '', 
                  status_code: int = 200, 
                  data: Optional[Any] = None) -> JsonResponse:
    
    return JsonResponse({
        'SUCCESS': success,
        'MESSAGE': message,
        'ERROR': error,
        'DATA': data or {}
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
