from django.conf.urls import patterns, include, url
from django.contrib.auth import login

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'the_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.home'),
    url(r'^accounts/profile/(\d+)/$', 'app.views.userpage', name='userpage'),
    url(r'^accounts/login/$', 'app.views.login'),
    url(r'^register/$', 'app.views.register'),
    url(r'^logout/$', 'app.views.logout'),
    url(r'^search/$', 'app.views.search')
)
