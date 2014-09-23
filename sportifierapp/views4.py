from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Needed to manually create HttpResponses or raise an Http404 exception
from django.http import HttpResponse, Http404

from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

# Helper function to guess a MIME type from a file name
from mimetypes import guess_type

import types

from django.utils import timezone

from datetime import datetime

from sportifierapp.models import *


from django.db.models import Q
# from sportifierapp.forms import *

from sportifierapp.forms import *


@login_required
def addfriend(request, other_user_name):
    user = get_object_or_404(User, username=other_user_name)
    alreadyFriends = Friendship.objects.filter(friend1=user)
    alreadyLoggedInUsersFriends = Friendship.objects.filter(friend1=request.user)    
    pendingFriends = PendingFriendship.objects.filter(friend1=request.user)

    af_users = []
    for f in alreadyFriends:
        if f.friend1 == user:
            af_users.append(f.friend2)
    af_loggedinusers = []
    for f in alreadyLoggedInUsersFriends:
        if f.friend1 == request.user:
            af_loggedinusers.append(f.friend2)                
    pf_users = []
    for f in pendingFriends:
        if f.friend1 == request.user:
            pf_users.append(f.friend2)    
    
    new_friendship = PendingFriendship(friend1 = user, friend2 = request.user)
    new_friendship.save()

    youmayknow = Profile.objects.exclude(user=request.user)
    
    profileAlreadyFriends = {}
    profilePendingFriends = {}
    profileAlreadyLoggedInUsersFriends = {}

    if alreadyLoggedInUsersFriends.count() > 0:
        profileAlreadyLoggedInUsersFriends = Profile.objects.filter(user__in = af_loggedinusers)
            
    if alreadyFriends.count() > 0:
        profileAlreadyFriends = Profile.objects.filter(user__in = af_users)

    if pendingFriends.count() > 0:
        profilePendingFriends = Profile.objects.filter(user__in = pf_users)

    p = Profile.objects.filter(user=user)
    
    if p.count() > 0:
        p = Profile.objects.get(user=user)

    if len(profileAlreadyFriends) % 3 == 0:
        frienddivs = len(profileAlreadyFriends)/3
    else:
        frienddivs = (len(profileAlreadyFriends)/3) + 1

    pendinglabel = 'friend request sent'

    context = {'otherusername' : other_user_name,
               'username' :request.user,
               'alreadyFriends' : profileAlreadyFriends,
               'nFriends' : len(af_users),
               'pendingFriends' : profilePendingFriends,
               'alreadyLoggedInUsersFriends' : profileAlreadyLoggedInUsersFriends,
               'youmayknowpeople' : youmayknow,               
               'profile' : p,
               'af_users':af_users,
               'af_loggedinusers':af_loggedinusers,               
               'pf_users':pf_users,               
               'pendinglabel' : pendinglabel,
               'friendcount' : range(frienddivs-1)}
  
    return render(request, 'webapp/otheruserprofile.html', context)

@login_required
def confirmfriend(request, other_user_name):
    user = get_object_or_404(User, username=other_user_name)
    
    new_friendship1 = Friendship(friend1=request.user, friend2=user)
    new_friendship1.save()
    
    new_friendship1_rev = Friendship(friend1=user, friend2=request.user)
    new_friendship1_rev.save()
    
    delete_pendingfriendship = PendingFriendship.objects.get(friend1=request.user, friend2=user)
    delete_pendingfriendship.delete()   
    
    alreadyFriends = Friendship.objects.filter(friend1=user)
    alreadyLoggedInUsersFriends = Friendship.objects.filter(friend1=request.user)    
    pendingFriends = PendingFriendship.objects.filter(friend1=request.user)
    
    af_users = []
    for f in alreadyFriends:
        if f.friend1 == user:
            af_users.append(f.friend2)
    af_loggedinusers = []
    for f in alreadyLoggedInUsersFriends:
        if f.friend1 == request.user:
            af_loggedinusers.append(f.friend2)                
    pf_users = []
    for f in pendingFriends:
        if f.friend1 == request.user:
            pf_users.append(f.friend2)

    youmayknow = Profile.objects.exclude(user=request.user)
    
    profileAlreadyFriends = {}
    profilePendingFriends = {}
    profileAlreadyLoggedInUsersFriends = {}

    if alreadyLoggedInUsersFriends.count() > 0:
        profileAlreadyLoggedInUsersFriends = Profile.objects.filter(user__in = af_loggedinusers)
            
    if alreadyFriends.count() > 0:
        profileAlreadyFriends = Profile.objects.filter(user__in = af_users)
    
    if pendingFriends.count() > 0:
        profilePendingFriends = Profile.objects.filter(user__in = pf_users)

    p = Profile.objects.filter(user=user)
    
    if p.count() > 0:
        p = Profile.objects.get(user=user)

    if len(profileAlreadyFriends) % 3 == 0:
        frienddivs = len(profileAlreadyFriends)/3
    else:
        frienddivs = (len(profileAlreadyFriends)/3) + 1
    
    pendinglabel = 'unfriend'

    context = {'otherusername' : other_user_name,
               'username' :request.user,
               'alreadyFriends' : profileAlreadyFriends,
               'nFriends' : len(af_users),
               'pendingFriends' : profilePendingFriends,
               'alreadyLoggedInUsersFriends' : profileAlreadyLoggedInUsersFriends,
               'youmayknowpeople' : youmayknow,
               'profile' : p,
               'af_users':af_users,
               'af_loggedinusers':af_loggedinusers,               
               'pf_users':pf_users,               
               'pendinglabel' : pendinglabel,
               'friendcount' : range(frienddivs-1)}    
  
    return render(request, 'webapp/friendprofile.html', context)

@login_required
def unfriend(request, other_user_name):
    user = get_object_or_404(User, username=other_user_name)
    
    curr_friendship = Friendship.objects.filter(friend1 = request.user, friend2 = user)
    curr_friendship = Friendship.objects.get(friend1 = request.user, friend2 = user)
    curr_friendship.delete()
    curr_friendship_rev = Friendship.objects.get(friend1 = user, friend2 = request.user)
    curr_friendship_rev.delete()    
    
    alreadyFriends = Friendship.objects.filter(friend1=user)
    alreadyLoggedInUsersFriends = Friendship.objects.filter(friend1=request.user)    
    pendingFriends = PendingFriendship.objects.filter(friend1=request.user)
    
    af_users = []
    for f in alreadyFriends:
        if f.friend1 == user:
            af_users.append(f.friend2)
    af_loggedinusers = []
    for f in alreadyLoggedInUsersFriends:
        if f.friend1 == request.user:
            af_loggedinusers.append(f.friend2)                
    pf_users = []
    for f in pendingFriends:
        if f.friend1 == request.user:
            pf_users.append(f.friend2) 

    youmayknow = Profile.objects.exclude(user=request.user)
    
    profileAlreadyFriends = {}
    profilePendingFriends = {}
    profileAlreadyLoggedInUsersFriends = {}

    if alreadyLoggedInUsersFriends.count() > 0:

        profileAlreadyLoggedInUsersFriends = Profile.objects.filter(user__in = af_loggedinusers)
            
    if alreadyFriends.count() > 0:
        profileAlreadyFriends = Profile.objects.filter(user__in = af_users)       
    if pendingFriends.count() > 0:
        profilePendingFriends = Profile.objects.filter(user__in = pf_users)

    p = Profile.objects.filter(user=user)
    
    if p.count() > 0:
        p = Profile.objects.get(user=user)

    if len(profileAlreadyFriends) % 3 == 0:
        frienddivs = len(profileAlreadyFriends)/3
    else:
        frienddivs = (len(profileAlreadyFriends)/3) + 1
    pendinglabel = 'add as a friend'
    context = {'otherusername' : other_user_name,
               'username':request.user,
               'alreadyFriends' : profileAlreadyFriends,
               'nFriends' : len(af_users),
               'pendingFriends' : profilePendingFriends,
               'alreadyLoggedInUsersFriends' : profileAlreadyLoggedInUsersFriends,
               'youmayknowpeople' : youmayknow,               
               'profile' : p,
               'af_users':af_users,
               'af_loggedinusers':af_loggedinusers,               
               'pf_users':pf_users,               
               'pendinglabel' : pendinglabel,
               'friendcount' : range(frienddivs-1)}    
  
    return render(request, 'webapp/otheruserprofile.html', context)

@login_required
def event(request, event_id):
    
    event = get_object_or_404(Event, id = event_id)
    related_events = Event.objects.exclude(id = event_id).filter(type = event.type)
    p = Profile.objects.get(user = request.user)

    alreadyFriends = Friendship.objects.filter(friend1=request.user)    
    af_users = []
    for f in alreadyFriends:
        af_users.append(f.friend2)
    
    if (p.univaff == event.host):
        userlocation = 'host'
    else:
        userlocation = 'away'
        
    if p.usertype == 'student' and userlocation == 'host':
        usercategory = 'homestudent'
        userprice = event.homestudentticketprice
    if p.usertype == 'staff' and userlocation == 'host':
        usercategory = 'homestaff'
        userprice = event.homestaffticketprice       
    if p.usertype == 'supporter' and userlocation == 'host':
        usercategory = 'homesupporter'
        userprice = event.homesupporterticketprice
    if p.usertype == 'student' and userlocation == 'away':
        usercategory = 'awaystudent'
        userprice = event.awaystudentticketprice
    if p.usertype == 'staff' and userlocation == 'away':
        usercategory = 'awaystaff'
        userprice = event.awaystaffticketprice
    if p.usertype == 'supporter' and userlocation == 'away':
        usercategory = 'awaysupporter'
        userprice = event.awaysupporterticketprice                        
    
    context = {'username' : request.user,
               'userprice' : userprice,
               'event' : event,
                'eventid' : event_id,
                   'related_events':related_events,
                   'friendList' : af_users}
    return render(request, 'webapp/event_detail.html', context)

@login_required
@transaction.commit_on_success
def edit_profile(request):
    errors = []
    profile_to_edit = get_object_or_404(Profile, user=User.objects.get(username=request.user))
    if request.method == 'GET':
        edit_form = ProfileForm(instance = profile_to_edit)
        context = {'edit_form':edit_form,'username':request.user,'profile':profile_to_edit, 'errors':errors}
        return render(request,'webapp/edit_profile.html',context)
    edit_form = ProfileForm(request.POST, request.FILES, instance = profile_to_edit)
    if not edit_form.is_valid():
        context={'edit_form':edit_form,'username':request.user,'profile':profile_to_edit,'errors':errors}
        return render(request,'webapp/edit_profile.html',context)
    edit_form.save()
    profile_edited = get_object_or_404(Profile, user=User.objects.get(username=request.user))
    content_type = guess_type(profile_edited.picture.name)
    if ("image" not in str(content_type[0])):
        errors.append("Wrong image type selected! Please find a proper image to upload.")
        profile_edited.picture = ''
        profile_edited.save()
        context={'edit_form':edit_form,'username':request.user,'profile':profile_edited,'errors':errors}
        return render(request,'webapp/edit_profile.html',context)
    redirect_string = 'userprofile/' + request.user.username
    return redirect(redirect_string)
