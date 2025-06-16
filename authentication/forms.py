
from django import forms
from django.forms import ModelForm
from .models import User, Verification



class RegisterForm(ModelForm):
    password = forms.CharField(
        max_length=40,
        widget=forms.PasswordInput(),
        label="Password"
    )
    
    confirm_password = forms.CharField(
        max_length=40,
        widget=forms.PasswordInput(),
        label="Confirm Password"
    )

    class Meta:
        model  = User
        fields = ["email", "username", "first_name", "password"]

    def clean(self):
        cleaned_data     = super().clean()
        password         = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")  

        if password and len(password) < 8:
            self.add_error("password", "Password must be at least 8 characters long.")
        
        if password != confirm_password:
            self.add_error("confirm_password", "The password and confirm password don't match.")

        return cleaned_data


class LoginForm(forms.Form):
    
    username = forms.CharField(
        max_length=40,
        label="Username"
    )
    
    password = forms.CharField(
        max_length=40,
        widget=forms.PasswordInput(),
        label="Password"
    )
    
    
class VerificationModelAdminForm(forms.ModelForm):
    
    class Meta:
        model   = Verification
        fields  = "__all__"
        widgets = {'code': forms.TextInput(attrs={'size': '20', 'style': 'font-family: monospace;'}),}
    
    class Media:
        js = ('admin/js/generate_code.js',)

    def clean_code(self):
        code            = self.cleaned_data["code"]
        required_length = 9 
        
        if len(code) != required_length:
            raise forms.ValidationError(f"Code must be exactly {required_length} characters long.")
        return code
    


