from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLs
    url(r'^admin/', include(admin.site.urls)),   # Admin URLs

    # Index page urls
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

)
