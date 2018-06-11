from django.conf.urls import url
from . import views

urlpatterns = [
    #Web Pages
    url(r'^$', views.index, name='index'),
    url(r'^parkings/$', views.parkings_list, name='parkings_list'),
    url(r'^parkings/(?P<pk>\d+)/$', views.parking, name='parking'),
    url(r'^cameras/$', views.camera_list, name='camera_list'),
    url(r'^cameras/(?P<pk>\d+)/$', views.camera, name='camera'),
    #Camera images
    url(r'^cameras/image/(?P<pk>\d+)/$', views.camera_image, name='camera_image'),
    #Authentication
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    #REST API
	url(r'^api/users/$', views.api_users, name='api_users'),
    url(r'^api/parkings/$', views.api_parkings, name='api_parkings'),
    url(r'^api/cameras/$', views.api_cameras, name='api_cameras'),
    url(r'^api/reservations/$', views.api_reservations, name='api_reservations'),
]
