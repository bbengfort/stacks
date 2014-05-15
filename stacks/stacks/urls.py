from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin URLs
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLs
    url(r'^admin/', include(admin.site.urls)),   # Admin URLs

    # Index page urls
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    # Social Authentication URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='auth_logout'),
    #url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
)
