from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import User

class University(models.Model):
    short_name = models.CharField(max_length=10,blank=True)
    name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.short_name
    
class Profile(models.Model):
    usertype = models.CharField(max_length=10)
    picture = models.FileField(upload_to="profile-photos",blank=True)    
    user = models.OneToOneField(User)
    fullName = models.CharField(max_length=42)
    address = models.CharField(max_length=200)
    sex = models.CharField(max_length=10)
    interests = models.CharField(max_length=200)
    aboutMe = models.CharField(max_length=200)
    univaff = models.ForeignKey(University)
    email = models.EmailField(max_length=75)
    phone = models.CharField(max_length=20,blank=True)
    userprice = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    userdiscountprice = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __unicode__(self):
        return self.user.username
    
class UniversityAdmin(models.Model):
    univaff = models.ForeignKey(University)
    admin = models.OneToOneField(User)

    def __unicode__(self):
        return self.admin.username
 
class EventType(models.Model):
    type = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.type   
        
class Event(models.Model):
    host = models.ForeignKey(University, related_name='host_university')
    away = models.ForeignKey(University, related_name='away_university')
    type = models.ForeignKey(EventType)
    championship = models.CharField(max_length=25)
    event_date = models.CharField(max_length=25)
    event_parse_date = models.CharField(max_length=25,blank=True)
    event_time = models.CharField(max_length=25)
    event_parse_time = models.CharField(max_length=25,blank=True)
    locationname = models.CharField(max_length=50,blank=True)
    locationlattitude = models.CharField(max_length=30)
    locationlongitude = models.CharField(max_length=30)
    description = models.CharField(max_length=42)
    homestudentticketprice = models.DecimalField(max_digits=5, decimal_places=2)
    homestaffticketprice = models.DecimalField(max_digits=5, decimal_places=2)
    homesupporterticketprice = models.DecimalField(max_digits=5, decimal_places=2)
    awaystudentticketprice = models.DecimalField(max_digits=5, decimal_places=2)
    awaystaffticketprice = models.DecimalField(max_digits=5, decimal_places=2)
    awaysupporterticketprice = models.DecimalField(max_digits=5, decimal_places=2)
    admin = models.ForeignKey(UniversityAdmin)
    maxnumberoftickets = models.IntegerField(default=0)
    areticketsavailableatvenue = models.CharField(max_length=6,default="no")
    ticketsleft =  models.IntegerField(default=0)    
    
    def __unicode__(self):
        return self.description
    
    @staticmethod
    def get_events(uni_admin):
        return Event.objects.filter(admin=uni_admin)

class Friendship(models.Model):
    friend1 = models.ForeignKey(User, related_name='friend_reqsent')
    friend2 = models.ForeignKey(User, related_name='friend_reqreceive')
    
    def __unicode__(self):
        return self.friend1.username   

class PendingFriendship(models.Model):
    friend1 = models.ForeignKey(User, related_name='friend_penreqreceived')
    friend2 = models.ForeignKey(User, related_name='friend_penreqsent')
    
    def __unicode__(self):
        return self.friend1.username 

class TransactionModel(models.Model):
    t_creator = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    date = models.DateTimeField('transaction date')
      
    def __unicode__(self):
        return str(self.id) + ":" + self.t_creator.username

class TransactionEvent(models.Model):
    trans = models.ForeignKey(TransactionModel)
    t_creator = models.ForeignKey(User, related_name='transaction creator')
    member = models.ForeignKey(User, related_name='transaction member')
    event = models.ForeignKey(Event)
    date = models.DateTimeField('transaction date')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
      
    def __unicode__(self):
        return str(self.id) + ":" + self.t_creator.username + "-" + self.member.username
