from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .forms import TicketForm
from .models import Ticket
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

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
            user = form.save()
            login(request, user)
            return redirect('Ticket/home.html')  # or any page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # adjust as needed
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')