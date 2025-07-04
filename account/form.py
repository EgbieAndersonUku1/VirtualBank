from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model  =  Profile
        fields =  "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={"id": "first-name", "minlength": "3", "maxlength": "40", "required": "required", "class": "center"}),
            "surname": forms.TextInput(attrs={"id": "surname", "minlength": "3", "maxlength": "40", "class": "center"}),
            "mobile": forms.TextInput(attrs={"type": "tel", "id": "mobile", "maxlength": "11", "minlength": "11", "class": "center"}),
            "country": forms.TextInput(attrs={"id": "country", "minlength": "4", "maxlength": "50", "class": "center"}),
            "state": forms.TextInput(attrs={"id": "state", "maxlength": "11", "minlength": "11", "class": "center"}),
            "postcode": forms.TextInput(attrs={"id": "postcode", "minlength": "5", "maxlength": "5", "class": "center"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "First Name"
        self.fields["surname"].label    = "Surname"
      