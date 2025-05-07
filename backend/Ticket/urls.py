from django.urls import path, include
from .views import HomeView
from . import views

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),  
    path('tickets/success/', views.ticket_success, name='ticket_success'), 
    path('ticket/<int:id>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/edit/<int:ticket_id>/', views.ticket_edit, name='ticket_edit'),
    path('ticket/delete/<int:pk>/', views.ticket_delete, name='ticket_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/login/', views.user_login, name='login'),
    path('registration/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile_view, name='default_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]