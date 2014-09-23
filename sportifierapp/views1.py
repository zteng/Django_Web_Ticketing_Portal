# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction

from django.http import HttpResponse, Http404

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

from django.utils import timezone

from datetime import datetime

from mimetypes import guess_type

from sportifierapp.models import *
from sportifierapp.forms import *


@login_required
def home(request):
	people = UniversityAdmin.objects.filter(admin = request.user)
	if people:
		context = {'events':Event.get_events(request.user),'add_form':EventForm()}
		return render(request, 'webapp/admin_landing_page.html',context)

	host_uni = University.objects.all()
	event_type = EventType.objects.all()
	days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
	events = Event.objects.all()
	for event in events:
		event.event_parse_date = event.event_date 
		weekday = datetime.datetime(int(event.event_date[:4]), int(event.event_date[5:7]), int(event.event_date[-2:])).weekday()

                # ensure that the time being displayed on the user landing page are in appropriate format.
		if (int(event.event_time[-2:]) < 10):			 
			event.event_parse_time = days[weekday] + ", " + str(int(event.event_time[:2])) + ":0" + str(int(event.event_time[-2:])) + " AM"
		else:
			event.event_parse_time = days[weekday] + ", " + str(int(event.event_time[:2])) + ":" + str(int(event.event_time[-2:])) + " AM"

		if (int(event.event_time[:2]) > 12) and (int(event.event_time[-2:]) < 10):
			event.event_parse_time = days[weekday] + ", " + str(int(event.event_time[:2]) - 12) + ":0" + str(int(event.event_time[-2:])) + " PM"
		elif (int(event.event_time[:2]) > 12) and (int(event.event_time[-2:]) >= 10):
			event.event_parse_time = days[weekday] + ", " + str(int(event.event_time[:2]) - 12) + ":" + str(int(event.event_time[-2:])) + " PM"			
		elif (int(event.event_time[:2]) == 12) and (int(event.event_time[-2:]) < 10):
			event.event_parse_time = days[weekday] + ", 0" + str(int(event.event_time[:2]) - 12) + ":0" + str(int(event.event_time[-2:])) + " PM"
		elif (int(event.event_time[:2]) == 12) and (int(event.event_time[-2:]) >= 10):
			event.event_parse_time = days[weekday] + ", 0" + str(int(event.event_time[:2]) - 12) + ":" + str(int(event.event_time[-2:])) + " PM"							

		event.save()	
	return render(request, 'webapp/user_landing_page.html',{'username' : request.user,
	                                                        'events' : events,
	                                                        'numberOfEvents' : Event.objects.all().count(),
	                                                        'host_university':host_uni,
	                                                        'event_type':event_type})
@login_required
@transaction.commit_on_success
def add_event(request):
    if request.method == "GET":
        context = {'events':Event.get_events(request.user),'add_form':EventForm()}
        return render(request,'webapp/admin_landing_page.html',context)
    new_event = Event(admin=UniversityAdmin.objects.get(admin=request.user))
    add_form = EventForm(request.POST,instance=new_event)
    if not add_form.is_valid():
        context = {'events':Event.get_events(request.user),'add_form':add_form}
        return render(request,'webapp/admin_landing_page.html',context)
    add_form.save()
    new_event.ticketsleft = new_event.maxnumberoftickets
    new_event.save()    
    return redirect(reverse('home'))

@login_required
@transaction.commit_on_success
def edit_event(request,event_id):
    event_to_edit = get_object_or_404(Event, admin=UniversityAdmin.objects.get(admin=request.user),id=event_id)
    if request.method == 'GET':
        edit_form = EventForm(instance = event_to_edit)
        context = {'edit_form':edit_form,'id':event_id,'event':event_to_edit}
        return render(request,'webapp/admin_edit_event_page.html',context)
    edit_form = EventForm(request.POST, instance = event_to_edit)

    if not edit_form.is_valid():
        context={'edit_form':edit_form,'id':event_id,'event':event_to_edit}
        return render(request,'webapp/admin_edit_event_page.html',context)
    edit_form.save()
    return redirect(reverse('home'))

@login_required
def search_date(request):
    startDate = request.GET['start_date']
    endDate = request.GET['end_date']
    search_events = Event.objects.exclude(event_date__lt=startDate).exclude(event_date__gt=endDate)
    context = {'events' : search_events,
               'numberOfEvents' : search_events.count()}
    return render(request,'webapp/search_by_date.xml',context,content_type='application/xml')

@login_required
def search_type(request):
    typeInput = request.GET['eventType']
    search_events = Event.objects.filter(type=EventType.objects.get(type=typeInput))
    context = {'events' : search_events,
               'numberOfEvents' : search_events.count()}
    return render(request,'webapp/search_by_type.xml',context,content_type='application/xml')

@login_required
def search_home_uni(request):
	host_uni = request.GET['hostUni']
	univ = University.objects.filter(name=host_uni)
	if len(univ)>0:
		univ = University.objects.get(name=host_uni)
		search_events = Event.objects.filter(host=univ)
	else:
		search_events = []
	context = {'events' : search_events,'numberOfEvents' : search_events.count()}
	return render(request,'webapp/search_by_home_uni.xml',context,content_type='application/xml')

@login_required
@transaction.commit_on_success
def payment(request):
    event = get_object_or_404(Event, id = int(request.POST['eventid']))
    related_events = Event.objects.exclude(id = int(request.POST['eventid'])).filter(type = event.type)
    selected_friend_names = request.POST.getlist('field')
    
    context = {}
    errors = []
    
    for friend1 in selected_friend_names:
        count = 0
        for friend2 in selected_friend_names:
            if friend2 != "" and friend1 != "" and (friend1 == friend2):
                count += 1
        if count > 1:
            errors.append('Same friend add twice. Please add all your friends again!')    
    
    alreadyFriends = Friendship.objects.filter(friend1=request.user)    
    af_users = []
    for f in alreadyFriends:
        af_users.append(f.friend2)
        
    for friend in selected_friend_names:
        if friend != "":
            friend_user_objects = User.objects.filter(username = friend)
            if len(friend_user_objects) > 0:
                added_friend = User.objects.get(username = friend)
                if af_users.count(added_friend) == 0:
                    errors.append('The added user is not your friend. You can add only your friend here!')
            else:
                errors.append('The person added is not a user of this website.')
    
    
    members_in_transaction = []
    if len(selected_friend_names) > 0:
        for friend in selected_friend_names:
            if friend:
                users = User.objects.filter(username=friend)
                if len(users) != 0:
                	user = get_object_or_404(User, username=friend)
                	members_in_transaction.append(user)
    
    discount_percent = 0
    if len(members_in_transaction) + 1 >= 2 and len(members_in_transaction) + 1 <=3:
        discount_percent = 5
    if len(members_in_transaction) + 1 >= 4 and len(members_in_transaction) + 1 <=6:
        discount_percent = 10
    if len(members_in_transaction) + 1 > 6:
        discount_percent = 20
    
    event.ticketleft = event.ticketsleft - len(members_in_transaction) - 1
    event.save()
    
    totalamount = 0                
    for member in members_in_transaction:
        p = Profile.objects.get(user = member)
        if (p.univaff == event.host):
            userlocation = 'host'
        else:
            userlocation = 'away'
            
        if p.usertype == 'student' and userlocation == 'host':
            p.userprice = event.homestudentticketprice
            p.userdiscountprice = float(event.homestudentticketprice) - (float(event.homestudentticketprice * discount_percent)/100);
        if p.usertype == 'staff' and userlocation == 'host':
            p.userprice = event.homestaffticketprice
            p.userdiscountprice = float(event.homestaffticketprice) - (float(event.homestaffticketprice * discount_percent)/100);       
        if p.usertype == 'supporter' and userlocation == 'host':
            p.userprice = event.homesupporterticketprice
            p.userdiscountprice = float(event.homesupporterticketprice) - (float(event.homesupporterticketprice * discount_percent)/100);
        if p.usertype == 'student' and userlocation == 'away':
            p.userprice = event.awaystudentticketprice
            p.userdiscountprice = float(event.awaystudentticketprice) - (float(event.awaystudentticketprice * discount_percent)/100);
        if p.usertype == 'staff' and userlocation == 'away':
            p.userprice = event.awaystaffticketprice
            p.userdiscountprice = float(event.awaystaffticketprice) - (float(event.awaystaffticketprice * discount_percent)/100);
        if p.usertype == 'supporter' and userlocation == 'away':
            p.userprice = event.awaysupporterticketprice
            p.userdiscountprice = float(event.awaysupporterticketprice) - (float(event.awaysupporterticketprice * discount_percent)/100);
        p.save()
        totalamount = totalamount + p.userdiscountprice
        
    p = Profile.objects.get(user = request.user)
    if (p.univaff == event.host):
        userlocation = 'host'
    else:
        userlocation = 'away'
        
    if p.usertype == 'student' and userlocation == 'host':
        p.userprice = event.homestudentticketprice
        p.userdiscountprice = float(event.homestudentticketprice) - (float(event.homestudentticketprice * discount_percent)/100);
    if p.usertype == 'staff' and userlocation == 'host':
        p.userprice = event.homestaffticketprice
        p.userdiscountprice = float(event.homestaffticketprice) - (float(event.homestaffticketprice * discount_percent)/100);       
    if p.usertype == 'supporter' and userlocation == 'host':
        p.userprice = event.homesupporterticketprice
        p.userdiscountprice = float(event.homesupporterticketprice) - (float(event.homesupporterticketprice * discount_percent)/100);
    if p.usertype == 'student' and userlocation == 'away':
        p.userprice = event.awaystudentticketprice
        p.userdiscountprice = float(event.awaystudentticketprice) - (float(event.awaystudentticketprice * discount_percent)/100);
    if p.usertype == 'staff' and userlocation == 'away':
        p.userprice = event.awaystaffticketprice
        p.userdiscountprice = float(event.awaystaffticketprice) - (float(event.awaystaffticketprice * discount_percent)/100);
    if p.usertype == 'supporter' and userlocation == 'away':
        p.userprice = event.awaysupporterticketprice
        p.userdiscountprice = float(event.awaysupporterticketprice) - (float(event.awaysupporterticketprice * discount_percent)/100);
    p.save()
    
    if errors:
        Uni_affiliation = University.objects.all()
        context['errors'] = errors
        context['username'] = request.user
        context['userprice'] = p.userprice
        context['event'] = event
        context['eventid'] = int(request.POST['eventid'])
        context['related_events'] = related_events
        context['friendList'] = af_users
        return render(request, 'webapp/event_detail.html', context)
        
    totalamount = totalamount + p.userdiscountprice

    tax_percent = 7
    
    tax_amount = float(tax_percent * totalamount)/100
    
    total_transaction_price = totalamount + tax_amount
    
    profileTransactionMembers = {}
    if len(members_in_transaction) > 0:
        profileTransactionMembers = Profile.objects.filter(user__in = members_in_transaction)

    transaction_date = timezone.now()
    curr_transaction = TransactionModel(t_creator=request.user, event=event, date=transaction_date)
    curr_transaction.save()
 
    curr_transaction_event = TransactionEvent(trans=curr_transaction,t_creator=request.user,member=request.user,event=event,date=transaction_date,amount=p.userdiscountprice)
    curr_transaction_event.save()
    
    if len(members_in_transaction) > 0:
        for memberprofile in profileTransactionMembers:
            curr_transaction_event = TransactionEvent(trans=curr_transaction,t_creator=request.user,member=memberprofile.user,event=event,date=transaction_date,amount=memberprofile.userdiscountprice)
            curr_transaction_event.save()

    context = {'username' : request.user,
            'userprofile' : Profile.objects.get(user = request.user),
             'transactionMembers' : profileTransactionMembers,
             'totalamount' : totalamount,
             'totaltransactionamount' : total_transaction_price,
             'taxamount' : tax_amount,
             'eventid' : int(request.POST['eventid']),
             'event' : event,
             'curr_transaction' : curr_transaction,
             }
    return render(request,'webapp/payment_page.html',context)
