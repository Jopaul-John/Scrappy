from .models import *
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django import forms

class userform(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password','email']


class Dealer(ModelForm):
    class Meta:
        model=UserProfile

        fields=['ph_no','address','pincode','city','reg_id','reg_image']



class Seller(ModelForm):
    class Meta:
        model=UserProfile

        fields=['ph_no','address','pincode','city','landmark',]


class Adsform(ModelForm):
    class Meta:
        model = Ads
        fields = ['pname','quantity','price','club_friend']


class Bidform(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount','bid_time']

class Contactform(ModelForm):
    class Meta:
        model = ContactUs
        exclude = []