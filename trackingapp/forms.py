from django.contrib.auth.forms import UserCreationForm
from django.forms import ChoiceField, ModelForm, TextInput, EmailInput, PasswordInput, CharField, NumberInput
from .models import MyUser, Userprofile

class SignUpForm(UserCreationForm):
    password1 = CharField(widget = PasswordInput(attrs = {'placeholder' : 'password', 'id' : 'password'}))
    password2 = CharField(widget = PasswordInput(attrs = {'placeholder' : 'confirm_password', 'id' : 'confirm_password'}))

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username' : TextInput(attrs = {'id' : 'name', 'placeholder' : 'username'}),
            'email' : EmailInput(attrs = {'id' : 'email', 'placeholder' : 'email'}),
        }


class ProfileForm(ModelForm):
    GENDER_CHOICES = [
        ('', '--Please choose an option--'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = ChoiceField(choices=GENDER_CHOICES, required=True)

    class Meta: 
        model = Userprofile
        fields = ['height', 'weight', 'age', 'gender']
        widgets = {
            'height' : NumberInput(attrs = {'id' : 'height'}),
            'weight' : NumberInput(attrs = {'id' : 'weight'}),
            'age' : NumberInput(attrs = {'id' : 'age'}),
        }