from django import forms
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from .models import User  # your custom User model

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'category', 'assigned_to']



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')  # Add fields you want