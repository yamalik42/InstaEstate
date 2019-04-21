from django.forms import ModelForm
from django import forms
from rest_api.models import Profile, Property, Inquiry
from rest_api.serializers import ( 
    UserSerializer, ProfileSerializer, PropertySerializer
)
from django.contrib.auth.models import User


class UserForm(ModelForm):
    username = forms.CharField(help_text=None)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, user=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['autocomplete'] = 'new-password'
        if user:
            self.initial = UserSerializer(user).data
            self.fields['password'].required = False

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(ModelForm):

    def __init__(self, profile=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if profile:
            del self.fields['seller']
            self.initial = ProfileSerializer(profile).data
            
    class Meta:
        model = Profile
        exclude = ['user']


class PropertyForm(ModelForm):
    def __init__(self, property=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = PropertySerializer(property).data if property else {}

    class Meta:
        model = Property
        exclude = ['seller', 'listing_date']


class EnquiryForm(ModelForm):
    class Meta:
        model = Inquiry
        fields = ['comment']