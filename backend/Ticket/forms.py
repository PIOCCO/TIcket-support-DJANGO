from django import forms
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from .models import User  # your custom User model



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'ticket_picture']  # no assigned_to

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('status'):
            cleaned_data['status'] = 'open'

        if not cleaned_data.get('priority'):
            cleaned_data['priority'] = 'medium'

        if not cleaned_data.get('category'):
            cleaned_data['category'] = 'general'

        return cleaned_data


class AdminTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['created_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show admin users in the assigned_to dropdown
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



