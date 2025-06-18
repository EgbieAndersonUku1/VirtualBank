
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
  
  
class VerifyEmailForm(forms.Form):
    first_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'first-char',
            'class': 'verification-char',
            'maxlength': '1',
            'required': True,
        })
    )
    second_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'second-char',
            'class': 'verification-char',
            'maxlength': '1',
            'required': True,
        })
    )
    third_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'third-char',
            'class': 'verification-char',
            'maxlength': '1',
        })
    )
    fourth_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'fourth-char',
            'class': 'verification-char',
            'maxlength': '1',
        })
    )
    fifth_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'fifth-char',
            'class': 'verification-char',
            'maxlength': '1',
        })
    )
    sixth_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'sixth-char',
            'class': 'verification-char',
            'maxlength': '1',
        })
    )
    seventh_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'seventh-char',
            'class': 'verification-char',
            'maxlength': '1',
        })
    )
    eighth_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'eighth-char',
            'class': 'verification-char',
            'maxlength': '1',
        })
    )
    ninth_char = forms.CharField(
        max_length=1,
        min_length=1,
        widget=forms.TextInput(attrs={
            'id': 'ninth-char',
            'class': 'verification-char',
            'maxlength': '1',
        })
    )

    


