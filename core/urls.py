from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import EventListView, EventListJson, EventCreateView, EventDetailView, MyEventListView, MyEventListJson, \
    EventUpdateView

app_name = 'core'
urlpatterns = [
    path('event/', EventListView.as_view(), name='event_list'),
    path('event/data/', EventListJson.as_view(), name='event_list_data'),
    path('myevent/', MyEventListView.as_view(), name='myevent_list'),
    path('myevent/data/', MyEventListJson.as_view(), name='myevent_list_data'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='events_detail'),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('event/add/', EventCreateView.as_view(), name='event_add'),
]
