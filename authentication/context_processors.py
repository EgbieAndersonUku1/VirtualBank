from account.models import Profile

def show_pin(request):
    pin                 = None
    joined_date         = None
    email               = None
    is_profile_created  = False

    if request.user.is_authenticated:
        pin                = request.user.pin 
        joined_date        = request.user.joined_on
        email              = request.user.email
        is_profile_created = Profile.objects.filter(user=request.user).exists()
       
    return {
        "PIN":pin,
        "JOINED_DATE": joined_date,
        "EMAIL": email,
        "IS_PROFILE_CREATED": is_profile_created

    }