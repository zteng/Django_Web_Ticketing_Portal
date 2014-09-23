from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^', include('sportifierapp.urls')),
    url(r'session_security/', include('session_security.urls')),    
    #url(r'^$', 'django.contrib.auth.views.login', {'template_name':'webapp/register_login.html'}),    
    # url(r'^$', 'sportifiersproject.views.home', name='home'),
    # url(r'^sportifiersproject/', include('sportifiersproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
