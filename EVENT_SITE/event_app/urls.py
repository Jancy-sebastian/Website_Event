from django.urls import path , re_path
from event_app import event_mnt

urlpatterns = [
    path('events', event_mnt.EventListView.as_view(), name='events'), 
    path('user/', event_mnt.Registeration.as_view(),name="create_user"),
    path('login', event_mnt.Login.as_view(), name='user-login'),
    path('logout', event_mnt.Logout.as_view(), name='user-logout'),
    path('liked', event_mnt.Likeapi.as_view(), name='like-fetcher'),
    re_path('^filter/(?P<startdate>.+)/(?P<enddate>.+)/(?P<category>.+)/$', event_mnt.EventFilter.as_view()),

]
