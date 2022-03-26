from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import fields
from .models import Review

STARCHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)

class ContactUsForm(forms.Form):
    title = forms.CharField(max_length=80 ,widget=forms.TextInput(attrs={
        'class':'contactInput',
        'id': "title",
        'placeholder': ' Title:'
    }))
    subject = forms.CharField(max_length=80, widget=forms.TextInput(attrs={
        'class': 'contactInput',
        'id': 'subject',
        'placeholder': ' Subject:'
    }))
    text = forms.CharField(min_length=20, widget=forms.Textarea(attrs={
        'class': 'contactInputArea',
        'id': 'text',
        'placeholder': ' Text:'
    }))
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={
        'class':'contactInput',
        'placeholder': 'Your Email:'
    }))
    

class AddReviewForm(forms.ModelForm):
    content = forms.CharField(min_length=20,required=True ,widget=forms.Textarea(attrs={
        'class': 'addReviewInputArea',
        'id': 'content',
        'placeholder': ' Write a review:'
    }))
    stars = forms.ChoiceField(initial='Give a Rating',choices=STARCHOICES,required=True, widget=forms.Select(attrs={
        'class': 'mySelect',
        'id': 'starsSelect'
    }))

    class Meta:
        model = Review
        fields = ['content', 'stars']


    def __init__(self, *args, **kwargs):
        super(AddReviewForm, self).__init__(*args, **kwargs)


class OrderReplicaForm(forms.Form):
    quantity = forms.IntegerField(max_value=10, min_value=1 ,widget=forms.NumberInput(attrs={
        'class':'contactInput',
        'id': "quantity",
        'placeholder': ' Quantity:'
    }))
    