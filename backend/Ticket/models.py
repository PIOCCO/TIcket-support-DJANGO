from django.db import models
from django.contrib.auth.models import AbstractUser

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

# Permission Model
class CustomPermission(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# User Model (extending Django's AbstractUser)
class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users')
    permissions = models.ManyToManyField(CustomPermission, related_name='users')

    def __str__(self):
        return self.username

# Ticket Model (with status, priority, category, assigned user, etc.)
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# TicketLog Model (linked to Ticket)
class TicketLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='logs')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.ticket.title} by {self.created_by.username}"

# Issue Model (merged into Ticket if needed)
# If you do not want to have a separate Issue model, you can disregard this.
class Issue(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='issues')
    issue_description = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Issue for {self.ticket.title}"
