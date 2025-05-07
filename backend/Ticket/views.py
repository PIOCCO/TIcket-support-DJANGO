from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import TicketForm
from .models import Ticket
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm

class HomeView(View):
    def get(self, request):
        return render(request, 'Ticket/home.html')  # Adjust path as needed

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_success')  # Define this URL in urls.py
    else:
        form = TicketForm()
    
    return render(request, 'Ticket/create_ticket.html', {'form': form})  # Adjust path if needed

def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'Ticket/ticket_list.html', {'tickets': tickets})

def ticket_success(request):
    return render(request, 'Ticket/ticket_success.html')

def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'Ticket/ticket_detail.html', {'ticket': ticket})

def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')  # or another success URL
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'Ticket/ticket_edit.html', {'form': form, 'ticket': ticket})

def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list')



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the user and log them in
            user = form.save()
            login(request, user)
            return redirect('home')  # Make sure 'home' is the correct URL name for the landing page after signup
    else:
        form = CustomUserCreationForm()  # Create a new form if GET request
    
    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        # Using the AuthenticationForm to handle user login
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authentication is successful, log the user in
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Adjust this to your desired success page
        else:
            # If form is invalid, return to the login page with an error message
            return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid credentials'})
    
    else:
        form = AuthenticationForm()  # Create an empty form on GET requests
        return render(request, 'registration/login.html', {'form': form})
    
@login_required
def profile_view(request):
    user_tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'accounts/profile.html', {'tickets': user_tickets})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever you want
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})