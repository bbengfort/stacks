from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from member.views import ProfileView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin URLs
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLs
    url(r'^admin/', include(admin.site.urls)),   # Admin URLs

    # Static Pages
    url(r'^$', TemplateView.as_view(template_name='site/index.html'), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),

    # Social Authentication URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='auth_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='auth_logout'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile'),
)
