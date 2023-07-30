from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from .models import Contact

class UserRegistration(UserCreationForm):
    username = forms.CharField(max_length=250,help_text="username is required.")
    email = forms.EmailField(max_length=250,help_text="The email field is required.")
    mobile_no = forms.CharField(max_length=250,help_text="mobile number is required.")
    password1 = forms.CharField(max_length=250,help_text="mobile number is required.")
    password2 = forms.CharField(max_length=250,help_text="mobile number is required.")
    class Meta:
        model = User
        fields = ('username', 'email', 'mobile_no','password1', 'password2', )
     

class AddContactForm():
    mobile_no = forms.CharField(max_length=17)
    username  = forms.CharField(max_length=30)
    email_id  = forms.EmailField()
    spam = forms.BooleanField(label='Spam',widget={
        
    })
    class Meta :
        model = Contact
        fields = ('mobile_no', 'username', 'email_id' )