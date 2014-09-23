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
@transaction.commit_on_success
def settings(request):
	context = {}
	context['username'] = request.user
	if request.method == 'GET':
		return render(request, 'webapp/reset_password_page.html', context)
		
	errors = []
	context['errors'] = errors
        # Checks the validity of current password
	if not 'curpassword' in request.POST or not request.POST['curpassword']:
		errors.append('Current password is needed.')
	else:
		user = request.user
		current_password = request.POST['curpassword']
		if user.check_password(current_password):
			if not 'newpassword' in request.POST or not request.POST['newpassword']:
				errors.append('New password is needed.')
			if not 'comfirmpassword' in request.POST or not request.POST['comfirmpassword']:
				errors.append('Confirm password is required.')
			if 'newpassword' in request.POST and 'comfirmpassword' in request.POST \
				and request.POST['newpassword'] and request.POST['comfirmpassword'] \
				and request.POST['newpassword'] != request.POST['comfirmpassword']:
				errors.append('New passwords did not match.')
		else:
			errors.append('password not matched with old one')
    
	if errors:
		return render(request, 'webapp/reset_password_page.html', context)
    
        # successfully change the password to a new one
	current_user = request.user
	current_user.set_password(request.POST['newpassword'])
	current_user.save()
	return render(request, 'webapp/reset_successfully.html', {})
	
@transaction.commit_on_success
def register(request):
    context = {}
	
    if request.method == 'GET':
        Uni_affiliation = University.objects.all()
        context = {"uni_affiliation":Uni_affiliation}
        return render(request, 'webapp/register_login.html',context)
    
    errors = []
    context['errors'] = errors

    # Checks the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']
    # Checks the validity of the form data
    if not 'email' in request.POST or not request.POST['email']:
        errors.append('Email is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['email'] = request.POST['email']
		
	# Checks if the affiliation has be chosen
	if request.POST['affiliation'] == "Choose your affiliation":
		errors.append('choose your affiliation')
	else:
		# Save the affiliation in the request context to re-fill the affiliation
                # field in case the form has errrors
		context['affiliation'] = request.POST['affiliation']
		
	# Save the affiliation in the request context to re-fill the affiliation
	context['typeList'] = request.POST['typeList']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if 'password1' in request.POST and 'password2' in request.POST \
       and request.POST['password1'] and request.POST['password2'] \
       and request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if len(User.objects.filter(username = request.POST['username'])) > 0:
        errors.append('Username is already taken.')
        
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        errors.append('Email is already taken.')
		
    if errors:
        Uni_affiliation = University.objects.all()
        context['uni_affiliation'] = Uni_affiliation
        return render(request, 'webapp/register_login.html', context)
		
    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'],
                                    email=request.POST['email'],
                                    password=request.POST['password1'])
    new_user.is_active = False
    new_user.save()

    new_profile = Profile(usertype =  request.POST['typeList'],user=new_user,fullName='',address='',sex='',interests='',aboutMe='',univaff=University.objects.get(name=request.POST['affiliation']),email=request.POST['email'],)
    new_profile.save()
    
    # initialize the logged-in user's information
    university = University.objects.get(name=request.POST['affiliation'])
    
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to the sportifier.  Please click the link below to
    verify your email address and complete the registration of your account:
    http://%s%s """ % (request.get_host(), reverse('confirm', args=(new_user.username, token)))
    
    send_mail(subject="Verify your email address",
                    message= email_body,
                    from_email="sportfier@gmail.com",
                    recipient_list=[new_user.email])
                    
    context['email'] = request.POST['email']
    return render(request, 'webapp/needs-confirmation.html', context)

@transaction.commit_on_success
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'webapp/confirmed.html', {})

@login_required
def get_profilephoto(request,other_user_name):
    profile = Profile.objects.get(user=User.objects.get(username=other_user_name))
    if not profile.picture:
        raise Http404
    content_type = guess_type(profile.picture.name)
    if 'image' not in str(content_type[0]):
        profile.picture = ''
        profile.save()
    return HttpResponse(profile.picture, mimetype=content_type)

@login_required
def paymentsuccess(request):
    return render(request, 'webapp/payment_success_page.html', {'username' : request.user })

@login_required
@transaction.commit_on_success
def cancel_transaction(request):

    curr_transaction = TransactionModel.objects.get(id=int(request.POST['transactionid']))
    
    curr_transaction_events = TransactionEvent.objects.filter(trans=curr_transaction).delete()
    curr_transaction.delete()
    redirect_string = 'event/' + request.POST['eventid']
    return redirect(redirect_string)
