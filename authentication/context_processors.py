
def show_pin(request):
    pin = None
    joined_date = None

    if request.user.is_authenticated:
        pin         = request.user.pin 
        joined_date = request.user.joined_on
    return {
        "PIN":pin,
        "JOINED_DATE": joined_date
    }