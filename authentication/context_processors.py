from account.models import Profile


def is_account_active(request):
    user = request.user
    if user.is_authenticated:
        return "Active account" if user.is_active else "Account is not active"


def is_user_logged_in(request):
    return f"You are currently logged in as {request.user.username.title()}" if request.user.is_authenticated else "Not logged in"

def show_user_information(request):
    pin                 = None
    joined_date         = None
    email               = None
    is_profile_created  = False
    username            = None
    is_active           = "Account is not active"
    is_logged_in        = False
    
    if request.user.is_authenticated:
        pin                = request.user.pin 
        joined_date        = request.user.joined_on
        email              = request.user.email
        is_profile_created = Profile.objects.filter(user=request.user).exists()
        username           = request.user.username
        is_active          = is_account_active(request)
        is_logged_in       = is_user_logged_in(request)
       
    return {
        "PIN":pin,
        "JOINED_DATE": joined_date,
        "EMAIL": email,
        "IS_PROFILE_CREATED": is_profile_created,
        "USERNAME": username,
        "IS_ACTIVE": is_active,
        "LOGGED_IN": is_logged_in


    }