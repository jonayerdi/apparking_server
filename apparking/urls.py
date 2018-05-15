from django.conf.urls import url
from . import views

urlpatterns = [
    #Web Pages
    url(r'^$', views.index, name='index'),
    #REST API
	url(r'^users/$', views.api_users, name='api_users'),
    url(r'^users/(?P<pk>\d+)/$', views.api_user, name='api_user'),
    url(r'^parkings/$', views.api_parkings, name='api_parkings'),
    url(r'^parkings/(?P<pk>\d+)/$', views.api_parking, name='api_parking'),
    url(r'^reservations/$', views.api_reservations, name='api_reservations'),
]
