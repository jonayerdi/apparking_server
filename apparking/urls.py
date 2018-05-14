from django.conf.urls import url
from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    url(r'^$', views.index, name='index'),
    #REST API
	url(r'^users/$', views.api_users, name='api_users'),
    url(r'^users/(?P<pk>\d+)/$', views.api_user, name='api_user'),
]
