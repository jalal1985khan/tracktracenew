from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User , Group
from django.forms import forms ,ModelForm
from django.db.models import fields
from trackandtrace.models import *
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2','is_active','is_staff','is_superuser']
        #exclude =['username']



class CreateProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

    class Meta:
        model = Profile
        fields = '__all__'
        exclude =['user']  