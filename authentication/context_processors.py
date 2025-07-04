
def show_pin(request):
    pin         = None
    joined_date = None
    email       = None

    if request.user.is_authenticated:
        pin         = request.user.pin 
        joined_date = request.user.joined_on
        email       = request.user.email
       
    return {
        "PIN":pin,
        "JOINED_DATE": joined_date,
        "EMAIL": email,

    }