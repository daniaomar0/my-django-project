from django import forms
from .models import Step1,Step2,Profile,Booking
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

class Step1Form(forms.ModelForm):
    
    class Meta:
        model = Step1
        fields = '__all__'

class Step2Form(forms.ModelForm):
    
    class Meta:
        model = Step2
        fields = '__all__'

class loginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8,widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

