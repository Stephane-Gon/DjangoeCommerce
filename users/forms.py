from email.policy import default
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.forms import formset_factory
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
import re

from .models import UserAccount
from store.models import Address, RefundedItems


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class':'myInput',
        'id': "rEmail"
        }))
    username = forms.CharField(max_length=100 ,widget=forms.TextInput(attrs={
        'class':'myInput',
        'id': "rUsername"
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'myInput',
        'id': 'rPassword'
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'myInput'}))

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password1', 'password2']


    def clean_email(self, *args, **kwargs):
        email_passed = self.cleaned_data.get('email')
        try:
            email = UserAccount.objects.filter(email = email_passed)
            if email.exists():
                raise forms.ValidationError("This email is already in use.")
        except ObjectDoesNotExist:
            print('Email is avaiable')
        return email_passed
    
        
class UserLoginForm(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class':'myInput',
        'id': "lEmail"
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'myInput',
        'id': 'lPassword'
        }))

    def clean_email(self, *args, **kwargs):

        email_passed = self.cleaned_data['email']
        try:
            user_email = UserAccount.objects.get(email = email_passed)
        except ObjectDoesNotExist: 
            raise forms.ValidationError("There is no account with this email.") 
        return email_passed

    def clean_password1(self, *args, **kwargs):

        email_passed = self.cleaned_data.get('email')
        pass_passed = self.cleaned_data['password1']
        try:
            user = UserAccount.objects.get(email = email_passed)
            if check_password(pass_passed, user.password) == False:
                raise forms.ValidationError("Wrong password!")
            else:
                return pass_passed
        except ObjectDoesNotExist: 
            return None


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'myInput',
        'type': 'email',
        'name': 'email'
        }))


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs ):
        super(UserSetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'myInput',
            'type': 'password',
            'name': 'new_password1'
            }),
        strip=False,
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'myInput',
            'type': 'password',
            'name': 'new_password2'
            }),
    )  


class UserChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs ):
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({'class' : 'myInput','type': 'password', 'name': 'old_password', 'id': 'old_password'})
        self.fields['new_password1'].widget.attrs.update({'class' : 'myInput','type': 'password', 'name': 'new_password', 'id': 'new_password1'})
        self.fields['new_password2'].widget.attrs.update({'class' : 'myInput','type': 'password', 'name': 'confirm_password', 'id': 'new_password2'})
    

class UserPersonalInfoForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100, required=False ,widget=forms.TextInput(attrs={
        'class':'myInput',
        'id': "first_name",
        'required' : True
        }))
    last_name = forms.CharField(max_length=100, required=False ,widget=forms.TextInput(attrs={
        'class':'myInput',
        'id': "last_name"
        }))

    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name']
    
    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if first_name == '' and last_name == '':
            print('ERROR')
            raise forms.ValidationError("You have to fill at least one field.")
    
    def clean_first_name(self, *args, **kwargs):
        first_name = self.cleaned_data['first_name']
        
        if re.search('[0-9]', first_name):
            raise forms.ValidationError("Your first name can't contain numbers.")
        if(bool(re.search('^[a-zA-Z]*$', first_name)) == False):
            raise forms.ValidationError("Your first name can't contain special characters.")
        if first_name == '':
            raise forms.ValidationError("Your first name can't be blank.")
        return first_name

    def clean_last_name(self, *args, **kwargs):
        last_name = self.cleaned_data['last_name']
        
        if re.search('[0-9]', last_name):
            raise forms.ValidationError("Your last name can't contain numbers.") 
        if(bool(re.search('^[a-zA-Z]*$', last_name)) == False):
            raise forms.ValidationError("Your last name can't contain special characters.")
        return last_name
    

class UserAddressInfoForm(forms.ModelForm):

    street_address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class':'myInput',
        'required' : True
    }))

    apartment_address = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class':'myInput',
    }))

    city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class':'myInput',
        'required' : True
    }))

    state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class':'myInput',
    }))

    zip = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class':'myInput',
        'required' : True
    }))

    country = CountryField(blank_label='(select country)').formfield(required=False,
        widget=CountrySelectWidget(attrs={
        'class': 'mySelect',
        'required' : True
    }))
    
    class Meta:
        model = Address
        fields = ['street_address', 'apartment_address', 'city', 'state', 'country', 'zip']

    def clean_street_address(self, *args, **kwargs):
        street_address = self.cleaned_data['street_address']
        
        if street_address == '':
            raise forms.ValidationError("Your street address can't be blank.")
        return street_address
    
    def clean_city(self, *args, **kwargs):
        city = self.cleaned_data['city']
        
        if city == '':
            raise forms.ValidationError("Your city can't be blank.")
        elif re.search('[0-9]', city):
            raise forms.ValidationError("Your city name can't contain numbers.")
        return city
    
    def clean_zip(self, *args, **kwargs):
        zip = self.cleaned_data['zip']
        
        if zip == '':
            raise forms.ValidationError("Your zip address can't be blank.")
        return zip
    
    def clean_country(self, *args, **kwargs):
        country = self.cleaned_data['country']
        
        if country == '':
            raise forms.ValidationError("Your country can't be blank.")
        return country


class RefundItemForm(forms.Form):
   
    reason = forms.CharField(min_length=20, required=True ,widget=forms.Textarea(attrs={
        'class': 'myInput myTextArea',
        'id': 'refund-reason',
        'placeholder': ' Why do you want to refund:'
    }))

    item = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'item-input',
            'value': '',
            'type': 'hidden'
        }),
    )

    images = forms.ImageField(max_length=100, required=True, widget=forms.ClearableFileInput(attrs={
        'id': 'refund-image',
        'class': 'refund-image',
        'multiple': True,
        'name': 'images'
    }))
    quantity = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'id': 'refund-quantity',
            'class': 'refund-quantity',
            'label': ''
        }),
    )


