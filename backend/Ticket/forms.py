from django import forms
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from .models import User  # your custom User model

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'status', 'priority', 'category', 'assigned_to', 'ticket_picture', 'created_by']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        # Only show admin users (is_staff = True) in the dropdown
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



