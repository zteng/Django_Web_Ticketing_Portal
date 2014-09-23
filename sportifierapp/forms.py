from django import forms

from django.contrib.auth.models import User
from sportifierapp.models import *


##class HTML5DateTimeInput(django.forms.widgets.DateTimeInput):
##    input_type = 'datetime-local'

class EventForm(forms.ModelForm):
    CHOICES = (('no','no'),('yes','yes'))
    CHAM_CHOICES = (('Regional','Regional'),('National Playoff','National Playoff'),('Friendly','Friendly'))
    type = forms.ModelChoiceField(queryset=EventType.objects.all(),initial=0,widget=forms.Select(
        attrs={'class':'span6'}),label='')
    host = forms.ModelChoiceField(queryset=University.objects.all(),initial=0,widget=forms.Select(
        attrs={'class':'span6'}),label='')
    away = forms.ModelChoiceField(queryset=University.objects.all(),initial=0,widget=forms.Select(
        attrs={'class':'span6'}),label='')
    championship = forms.ChoiceField(choices=CHAM_CHOICES,initial='Regional',widget=forms.Select(
        attrs={'class':'span6'}),label='')
    event_date = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'type':'date','class':'input-xlarge span6'}), label='')
    event_time = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'type':'time','class':'input-xlarge span6'}), label='')
    locationname = forms.CharField(max_length=25, widget=forms.TextInput(
        attrs={'type':'text','class':'input-xlarge span6'}), label='') 
    locationlattitude = forms.CharField(max_length = 30,widget=forms.HiddenInput(
        attrs={'type':'hidden','id':'lat'}), label='')
    locationlongitude = forms.CharField(max_length = 30,widget=forms.HiddenInput(
        attrs={'type':'hidden','id':'lon'}), label='')
    description = forms.CharField(max_length = 42,widget=forms.Textarea(
        attrs={'class':'form-control span6 counted','placeholder':'Type in your message',
               'rows':'5','style':'margin-bottom:10px;','onkeyup':'countChar(this)'}), label='')
    homestudentticketprice = forms.DecimalField(max_digits=5,decimal_places=2,widget=forms.TextInput(
        attrs={'type':'number', 'step': '0.25','class':'input-medium'}), label='')
    homestaffticketprice = forms.DecimalField(max_digits=5,decimal_places=2,widget=forms.TextInput(
        attrs={'type':'number', 'step': '0.25','class':'input-medium'}), label='')
    homesupporterticketprice = forms.DecimalField(max_digits=5,decimal_places=2,widget=forms.TextInput(
        attrs={'type':'number', 'step': '0.25','class':'input-medium'}), label='')
    awaystudentticketprice = forms.DecimalField(max_digits=5,decimal_places=2,widget=forms.TextInput(
        attrs={'type':'number', 'step': '0.25','class':'input-medium'}), label='')
    awaystaffticketprice = forms.DecimalField(max_digits=5,decimal_places=2,widget=forms.TextInput(
        attrs={'type':'number', 'step': '0.25','class':'input-medium'}), label='')
    awaysupporterticketprice = forms.DecimalField(max_digits=5,decimal_places=2,widget=forms.TextInput(
        attrs={'type':'number', 'step': '0.25','class':'input-medium'}), label='')
    maxnumberoftickets = forms.IntegerField(widget=forms.TextInput(
        attrs={'type':'number','placeholder':'create number of tickets here','class':'input-xlarge span6'}), label='')
    areticketsavailableatvenue = forms.ChoiceField(choices=CHOICES,initial='no',widget=forms.Select(
        attrs={'class':'span6'}),label='')
    
    
    class Meta:
        model = Event
        exclude = ('admin', 'ticketsleft',)


class ProfileForm(forms.ModelForm):
    GENDER_CHOICES = (('Female','Female'),('Male','Male'),)
    
    fullName = forms.CharField(max_length=42, widget=forms.TextInput(
        attrs={'type':'text','value':' ','class':'info-value'}), label='', initial='')
    address = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'type':'text','value':' ','class':'info-value'}), label='', initial='')
    sex = forms.ChoiceField(choices=GENDER_CHOICES,initial='Female',widget=forms.Select(
        attrs={'class':'span2'}),label='',)
    interests = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'type':'text','value':' ','class':'info-value'}), label='', initial='')
    aboutMe = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'type':'text','value':' ','class':'info-value'}), label='', initial='')
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type':'tel', 'pattern' : '[\(]\d{3}[\)]\d{3}[\-]\d{4}', 'placeholder' :'e.g. (###)###-####','class':'info-value'}), label='')
    
    
    class Meta:
        model = Profile
        exclude = ('usertype','user','email','univaff','userprice','userdiscountprice')
        widgets = {'picture' : forms.FileInput(attrs={}) }
