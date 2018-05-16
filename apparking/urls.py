from django.conf.urls import url
from . import views

urlpatterns = [
    #Web Pages
    url(r'^$', views.index, name='index'),
    #REST API
	url(r'^api/users/$', views.api_users, name='api_users'),
    url(r'^api/parkings/$', views.api_parkings, name='api_parkings'),
    url(r'^api/reservations/$', views.api_reservations, name='api_reservations'),
]
