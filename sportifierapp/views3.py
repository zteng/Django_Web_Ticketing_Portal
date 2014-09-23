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
def userprofile(request, user_name):
    user = get_object_or_404(User, username=user_name)
    alreadyFriends = Friendship.objects.filter(friend1=request.user)
    pendingFriends = PendingFriendship.objects.filter(friend1=request.user)
    af_users = []
    for f in alreadyFriends:
        if f.friend1 == request.user:
            af_users.append(f.friend2)
    pf_users = []
    for f in pendingFriends:
        if f.friend1 == request.user:
            pf_users.append(f.friend2)
    
    youmayknow = Profile.objects.exclude(user=request.user)
    profileAlreadyFriends = {}
    profilePendingFriends = {}
    
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
    context = {'username' : user_name,
               'alreadyFriends' : profileAlreadyFriends,
               'nFriends' : len(af_users),
               'pendingFriends' : profilePendingFriends,
               'youmayknowpeople' : youmayknow,
               'profile' : p,
               'af_users':af_users,
               'pf_users':pf_users,
               'friendcount' : range(frienddivs-1)}
  
    return render(request, 'webapp/loggedinprofile.html', context)

@login_required
def otheruserprofile(request, other_user_name):
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
    otherUserPendingFriends = PendingFriendship.objects.filter(friend1=user)
    loggedinUserPendingFriends = PendingFriendship.objects.filter(friend1=request.user)
    
    oUPFCount = otherUserPendingFriends.count();
    liUPFCount = loggedinUserPendingFriends.count();
    
    if oUPFCount == 0:
        otherUserPendingFriends = []
    else:     
        otherUserPendingFriends = PendingFriendship.objects.filter(friend1=user)
        
    if liUPFCount == 0:
        loggedinUserPendingFriends = []
    else:     
        loggedinUserPendingFriends = PendingFriendship.objects.filter(friend1=request.user)
    
    checkifpresentinotherusersPF = []
    for f in otherUserPendingFriends:
        if f.friend2 == request.user:
            checkifpresentinotherusersPF.append(f.friend2)
            
    checkifotheruserpresentinmyPF = []
    for f in loggedinUserPendingFriends:
        if f.friend2 == user:
            checkifotheruserpresentinmyPF.append(f.friend2)               
    pendinglabel = 'add friend'
    if (oUPFCount != 0 and len(checkifpresentinotherusersPF) == 0) and (liUPFCount != 0 and len(checkifotheruserpresentinmyPF) == 0):
        pendinglabel = 'add friend'        
    elif (oUPFCount != 0 and len(checkifpresentinotherusersPF) > 0):
        pendinglabel = 'friend request sent'
    elif (liUPFCount != 0 and len(checkifotheruserpresentinmyPF) > 0):
        pendinglabel = 'awaiting request approval'

    
    p = Profile.objects.filter(user=user)
    
    if p.count() > 0:
        p = Profile.objects.get(user=user)
        
    if len(profileAlreadyFriends) % 3 == 0:
        frienddivs = len(profileAlreadyFriends)/3
    else:
        frienddivs = (len(profileAlreadyFriends)/3) + 1            
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
def friendprofile(request, other_user_name):
    user = get_object_or_404(User, username=other_user_name)
    alreadyFriends = Friendship.objects.filter(friend1=user)
    alreadyLoggedInUsersFriends = Friendship.objects.filter(friend1=request.user)
    pendingFriends = PendingFriendship.objects.filter(friend1=request.user)    
    
    youmayknow = Profile.objects.exclude(user=request.user)

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
    
    profileAlreadyFriends = {}
    profilePendingFriends = {}
    profileAlreadyLoggedInUsersFriends = {}

    if alreadyLoggedInUsersFriends.count() > 0:
        profileAlreadyLoggedInUsersFriends = Profile.objects.filter(user__in = af_loggedinusers)
            
    if alreadyFriends.count() > 0:
        profileAlreadyFriends = Profile.objects.filter(user__in = af_users)
    if pendingFriends.count() > 0:
        profilePendingFriends = Profile.objects.filter(user__in = pf_users)
    otherUserPendingFriends = PendingFriendship.objects.filter(friend1=user)
    loggedinUserPendingFriends = PendingFriendship.objects.filter(friend1=request.user)
    
    oUPFCount = otherUserPendingFriends.count();
    liUPFCount = loggedinUserPendingFriends.count();
    
    if oUPFCount == 0:
        otherUserPendingFriends = []
    else:     
        otherUserPendingFriends = PendingFriendship.objects.filter(friend1=user)
        
    if liUPFCount == 0:
        loggedinUserPendingFriends = []
    else:     
        loggedinUserPendingFriends = PendingFriendship.objects.filter(friend1=request.user)
    
    checkifpresentinotherusersPF = []
    for f in otherUserPendingFriends:
        if f.friend2 == request.user:
            checkifpresentinotherusersPF.append(f.friend2)
            
    checkifotheruserpresentinmyPF = []
    for f in loggedinUserPendingFriends:
        if f.friend2 == user:
            checkifotheruserpresentinmyPF.append(f.friend2)               
    pendinglabel = 'add friend'
    if (oUPFCount != 0 and len(checkifpresentinotherusersPF) == 0) and (liUPFCount != 0 and len(checkifotheruserpresentinmyPF) == 0):
        pendinglabel = 'add friend'        
    elif (oUPFCount != 0 and len(checkifpresentinotherusersPF) > 0):
        pendinglabel = 'friend request sent'
    elif (liUPFCount != 0 and len(checkifotheruserpresentinmyPF) > 0):
        pendinglabel = 'awaiting request approval'
        
    checkifpresentinotherusersFriends = []
    for f in af_users:
        if f == request.user:
            checkifpresentinotherusersFriends.append(f)
    if (len(checkifpresentinotherusersFriends) > 0):
        pendinglabel = 'unfriend'
    
    if request.user == user:
        pendinglabel = 'edit'
    
    p = Profile.objects.filter(user=user)
    
    if p.count() > 0:
        p = Profile.objects.get(user=user) 
    
    if len(profileAlreadyFriends) % 3 == 0:
        frienddivs = len(profileAlreadyFriends)/3
    else:
        frienddivs = (len(profileAlreadyFriends)/3) + 1   

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
  
    return render(request, 'webapp/friendprofile.html', context)
