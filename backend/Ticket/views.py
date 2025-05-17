from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from .forms import TicketForm, CustomUserCreationForm, AdminTicketForm
from .models import Ticket, TicketLog
from django.http import HttpResponseForbidden


# ------------------ Home ------------------

class HomeView(View):
    def get(self, request):
        return render(request, 'Ticket/home.html')

# ------------------ Ticket Views ------------------

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import TicketLog

@login_required
def create_ticket(request):
    form = TicketForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        ticket = form.save(commit=False)
        ticket.created_by = request.user
        ticket.save()
        
        # Create the log BEFORE redirecting
        TicketLog.objects.create(
            ticket=ticket,
            created_by=request.user,
            action='Ticket created'
        )
        
        return redirect('ticket_success')

    return render(request, 'Ticket/create_ticket.html', {'form': form})


@login_required
def ticket_list(request):
    priority = request.GET.get('priority')
    if request.user.is_staff or request.user.is_superuser:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)

    if priority:
        tickets = tickets.filter(priority=priority)

    return render(request, 'Ticket/ticket_list.html', {'tickets': tickets})



def ticket_success(request):
    return render(request, 'Ticket/ticket_success.html')


def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    return render(request, 'Ticket/ticket_detail.html', {'ticket': ticket})

@login_required
def ticket_edit(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if not request.user.is_staff:
        return HttpResponseForbidden()  # or redirect if not admin

    if request.method == 'POST':
        form = AdminTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            edited_ticket = form.save(commit=False)
            # Preserve created_by from the original ticket
            edited_ticket.created_by = ticket.created_by
            edited_ticket.save()

              # Log the edit action
            TicketLog.objects.create(
                ticket=edited_ticket,
                created_by=request.user,
                action='Ticket edited'
            )
            # redirect somewhere, e.g. ticket list
            return redirect('ticket_list')
    else:
        form = AdminTicketForm(instance=ticket)
    return render(request, 'Ticket/ticket_edit.html', {'form': form})


@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        # Log deletion before deleting the ticket
        TicketLog.objects.create(
            ticket=ticket,
            created_by=request.user,
            action='Ticket deleted'
        )
        ticket.delete()
        return redirect('ticket_list')
    
    return render(request, 'Ticket/ticket_confirm_delete.html', {'ticket': ticket})

# ------------------ Auth Views ------------------

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'registration/login.html', {'form': form})

# ------------------ Profile Views ------------------

@login_required
def profile_view(request):
    tickets = Ticket.objects.filter(created_by=request.user)
    return render(request, 'accounts/profile.html', {'tickets': tickets})


@login_required
def edit_profile(request):
    form = UserChangeForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'accounts/edit_profile.html', {'form': form})
