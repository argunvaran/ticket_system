from django import forms
from tickets.models import Ticket, TicketAttachment
from customers.models import Customer, CustomerProduct
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import JsonResponse

User = get_user_model()

class AssignTicketForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Assign to')

    class Meta:
        model = Ticket
        fields = ['assigned_to']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'subject', 
            'description', 
            'ticket_customer',
            'ticket_customer_product',
            'solution_description', 
            'effort', 
            'status', 
            'assigned_to'
        ]
        widgets = {
            'ticket_customer': forms.Select(attrs={'class': 'form-control'}),  
            'ticket_customer_product': forms.Select(attrs={'class': 'form-control'}),  
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'solution_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'effort': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

        if 'ticket_customer' in self.data:
            try:
                customer_id = int(self.data.get('ticket_customer'))
                self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.filter(customer_id=customer_id)
            except (ValueError, TypeError):
                self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.none()
        elif self.instance.pk and self.instance.ticket_customer:
            self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.filter(customer=self.instance.ticket_customer)
        else:
            self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.none()


class CreateTicketForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Assign to')
    ticket_customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=True, label='Customer')
    ticket_customer_product = forms.ModelChoiceField(queryset=CustomerProduct.objects.none(), required=True, label='Product')
    attachment = forms.FileField(required=False, label='Attachment')

    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'assigned_to', 'ticket_customer', 'ticket_customer_product', 'attachment']

    def __init__(self, *args, **kwargs):
        super(CreateTicketForm, self).__init__(*args, **kwargs)

        if 'ticket_customer' in self.data:
            try:
                customer_id = int(self.data.get('ticket_customer'))
                products = CustomerProduct.objects.filter(customer_id=customer_id)
                
                unique_products = set()
                unique_customer_products = []
                for customer_product in products:
                    if customer_product.product not in unique_products:
                        unique_products.add(customer_product.product)
                        unique_customer_products.append(customer_product)
                
                self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.filter(id__in=[p.id for p in unique_customer_products])
            except (ValueError, TypeError):
                self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.none()
        elif self.instance.pk and self.instance.ticket_customer:

            products = CustomerProduct.objects.filter(customer=self.instance.ticket_customer)
            unique_products = set()
            unique_customer_products = []
            for customer_product in products:
                if customer_product.product not in unique_products:
                    unique_products.add(customer_product.product)
                    unique_customer_products.append(customer_product)
            
            self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.filter(id__in=[p.id for p in unique_customer_products])
        else:
            self.fields['ticket_customer_product'].queryset = CustomerProduct.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('ticket_customer')
        customer_product = cleaned_data.get('ticket_customer_product')
        subject = cleaned_data.get('subject')
        description = cleaned_data.get('description')

        if not customer:
            self.add_error('ticket_customer', "Please select a customer.")
        if not customer_product:
            self.add_error('ticket_customer_product', "Please select a product.")
        if not subject:
            self.add_error('subject', "Subject field is required.")
        if not description:
            self.add_error('description', "Description field is required.")

        return cleaned_data





