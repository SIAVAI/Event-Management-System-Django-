# events/urls.py

from django.urls import path
from events.views import *

urlpatterns = [
    path('', organizer_dashboard, name='dashboard'),
    path('categories/', category_list, name='category-list'),
    path('categories/add/', category_create, name='category-create'),
    path('categories/edit/<int:pk>/', category_update, name='category-update'),
    path('categories/delete/<int:pk>/', category_delete, name='category-delete'),
    path('participants/', participant_list, name='participant-list'),
    path('participants/add/', participant_create, name='participant-create'),
    path('participants/edit/<int:pk>/', participant_update, name='participant-update'),
    path('participants/delete/<int:pk>/', participant_delete, name='participant-delete'),
    path('events/', event_list, name='event-list'),
    path('events/<int:pk>/', event_detail, name='event-detail'),
    path('events/add/', event_create, name='event-create'),
    path('events/edit/<int:pk>/', event_update, name='event-update'),
    path('events/delete/<int:pk>/', event_delete, name='event-delete'),
    path('dashboard/', organizer_dashboard, name='organizer-dashboard'),
]