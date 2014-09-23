from django.conf.urls import patterns, include, url
from django.views.generic import *
from sportifierapp.models import *

# Generates the routes for the controller
# Typical use is a regular expression for a URL pattern, and then the
# action to call to process requests for that URL pattern.

urlpatterns = patterns('',
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'webapp/register_login.html','extra_context':{'uni_affiliation':University.objects.all()}}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^add-event', 'sportifierapp.views1.add_event', name='add'),
    url(r'^search_by_date$', 'sportifierapp.views1.search_date'),
    url(r'^search_by_type$', 'sportifierapp.views1.search_type', name='search_type'),
    url(r'^search_by_hosting_university$', 'sportifierapp.views1.search_home_uni', name='search_host_uni'),
    url(r'^settings$', 'sportifierapp.views2.settings'),
    url(r'^edit-event/(?P<event_id>\d+)$', 'sportifierapp.views1.edit_event', name='edit'),
    url(r'^register$', 'sportifierapp.views2.register',name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'sportifierapp.views2.confirm_registration', name='confirm'),
    url(r'^$', 'sportifierapp.views1.home',name='home'),
    url(r'^userprofile/(?P<user_name>[a-zA-Z0-9_]+)$', 'sportifierapp.views3.userprofile', name = 'userprofile'),
    url(r'^editprofile$', 'sportifierapp.views4.edit_profile', name='editprofile'),
    url(r'^otheruserprofile/(?P<other_user_name>[a-zA-Z0-9_]+)$', 'sportifierapp.views3.otheruserprofile'),
    url(r'^friendprofile/(?P<other_user_name>[a-zA-Z0-9_]+)$', 'sportifierapp.views3.friendprofile'),
    url(r'^event/(?P<event_id>\d+)$', 'sportifierapp.views4.event'),
    url(r'^payment$', 'sportifierapp.views1.payment', name='payment'),
    url(r'^cancel_transaction$', 'sportifierapp.views2.cancel_transaction', name='cancel_transaction'),
    url(r'^paymentsuccess$', 'sportifierapp.views2.paymentsuccess', name='paymentsuccess'),
    url(r'^addfriend/(?P<other_user_name>[a-zA-Z0-9_]+)$', 'sportifierapp.views4.addfriend'),
    url(r'^confirmfriend/(?P<other_user_name>[a-zA-Z0-9_]+)$', 'sportifierapp.views4.confirmfriend'),
    url(r'^unfriend/(?P<other_user_name>[a-zA-Z0-9_]+)$', 'sportifierapp.views4.unfriend'),
    url(r'^get_profilephoto/(?P<other_user_name>[a-zA-Z0-9_]+)$', 'sportifierapp.views2.get_profilephoto',name='profile_photo'),
)
