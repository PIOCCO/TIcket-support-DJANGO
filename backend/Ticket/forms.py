from django import forms
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from .models import User  # your custom User model

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'category', 'assigned_to', 'ticket_picture']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')