from django.db import models
from django.conf import settings
from customers.models import Customer, CustomerProduct

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]
    
    subject = models.CharField(max_length=255)
    description = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    solution_description = models.TextField(null=True, blank=True)
    
    ticket_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    ticket_customer_product = models.ForeignKey(CustomerProduct, on_delete=models.SET_NULL, null=True, blank=True)
    
    effort = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE) 
    file = models.FileField(upload_to='ticket_attachments/')

    def __str__(self):
        return self.file.name