from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from tickets.models import Ticket, TicketAttachment
from customers.models import Customer, CustomerProduct
from tickets.forms import TicketForm, CreateTicketForm, AssignTicketForm
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
    return render(request, 'index.html')

@login_required
def assign_tickets_view(request):
    customers = Customer.objects.all()
    
    products = CustomerProduct.objects.values('product__id', 'product__name').distinct()
    
    users = User.objects.all()

    customer_id = request.GET.get('customer')
    product_id = request.GET.get('product')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    assigned_to_id = request.GET.get('assigned_to')

    tickets = Ticket.objects.none()

    if customer_id or product_id or start_date or end_date or assigned_to_id:
        tickets = Ticket.objects.all().order_by('-created_at')

        if customer_id:
            tickets = tickets.filter(ticket_customer_id=customer_id)
        if product_id:
            tickets = tickets.filter(ticket_customer_product__product_id=product_id)
        if assigned_to_id and assigned_to_id != 'all':
            if assigned_to_id == 'unassigned':
                tickets = tickets.filter(assigned_to__isnull=True)
            else:
                tickets = tickets.filter(assigned_to_id=assigned_to_id)
        if start_date:
            tickets = tickets.filter(created_at__gte=start_date)
        if end_date:
            tickets = tickets.filter(created_at__lte=end_date)

    if tickets.exists():
        tickets = tickets[:1000]

    if request.method == 'POST':
        success = False
        for ticket in tickets:
            form = AssignTicketForm(request.POST, instance=ticket, prefix=str(ticket.id))
            if form.is_valid():
                assigned_to = form.cleaned_data['assigned_to']
                ticket.assigned_to = assigned_to if assigned_to != 'unassigned' else None
                ticket.save()
                success = True
        if success:
            messages.success(request, "Tickets assigned successfully.")
        return redirect('assign_tickets')

    forms = [AssignTicketForm(instance=ticket, prefix=str(ticket.id)) for ticket in tickets]
    forms_and_tickets = zip(forms, tickets)

    paginator = Paginator(list(forms_and_tickets), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tickets/assign_tickets.html', {
        'page_obj': page_obj,
        'customers': customers,
        'products': products, 
        'users': users,
        'customer_id': customer_id,
        'product_id': product_id,
        'assigned_to_id': assigned_to_id,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
def ticket_create_view(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save()
            if 'attachment' in request.FILES:
                TicketAttachment.objects.create(ticket=ticket, file=request.FILES['attachment'])
            messages.success(request, "Ticket created successfully.")
            return redirect('all_tickets')
        else:
            messages.error(request, "Please fill in all required fields.")
    else:
        form = CreateTicketForm()
    return render(request, 'tickets/ticket_create.html', {'form': form})

@login_required
def my_tickets(request):
    customers = Customer.objects.all()
    products = CustomerProduct.objects.values('product__id', 'product__name').distinct()

    customer_id = request.GET.get('customer')
    product_id = request.GET.get('product')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status')

    tickets = Ticket.objects.none()

    if customer_id or product_id or start_date or end_date or status:
        tickets = Ticket.objects.filter(assigned_to=request.user)

        if customer_id:
            tickets = tickets.filter(ticket_customer_id=customer_id)

        if product_id:
            tickets = tickets.filter(ticket_customer_product__product_id=product_id)

        if start_date:
            tickets = tickets.filter(created_at__gte=start_date)

        if end_date:
            tickets = tickets.filter(created_at__lte=end_date)

        if status and status != 'all':
            tickets = tickets.filter(status=status)

    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tickets/my_tickets.html', {
        'page_obj': page_obj,
        'customers': customers,
        'products': products,
        'customer_id': customer_id,
        'product_id': product_id,
        'start_date': start_date,
        'end_date': end_date,
        'status': status,  
    })


@login_required
def all_tickets(request):
    tickets = Ticket.objects.none()  
    customers = Customer.objects.all()
    users = User.objects.all()

    products = CustomerProduct.objects.values('product__id', 'product__name').distinct()

    customer_id = request.GET.get('customer')
    product_id = request.GET.get('product')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    assigned_to_id = request.GET.get('assigned_to')
    status = request.GET.get('status')  

    if customer_id or product_id or start_date or end_date or assigned_to_id or status:
        tickets = Ticket.objects.all().order_by('-created_at')

        if customer_id:
            tickets = tickets.filter(ticket_customer_id=customer_id)

        if product_id:
            tickets = tickets.filter(ticket_customer_product__product_id=product_id)

        if start_date:
            tickets = tickets.filter(created_at__gte=start_date)
        if end_date:
            tickets = tickets.filter(created_at__lte=end_date)

        if assigned_to_id:
            if assigned_to_id == 'unassigned':
                tickets = tickets.filter(assigned_to__isnull=True)
            else:
                tickets = tickets.filter(assigned_to_id=assigned_to_id)

        if status and status != 'all':  
            tickets = tickets.filter(status=status)

    paginator = Paginator(tickets, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tickets/all_tickets.html', {
        'page_obj': page_obj,
        'customers': customers,
        'products': products,
        'users': users,
        'customer_id': customer_id,
        'product_id': product_id,
        'assigned_to_id': assigned_to_id,
        'status': status,  
        'start_date': start_date,
        'end_date': end_date,
    })




@login_required
def ticket_search(request):
    query = request.GET.get('q')
    tickets = Ticket.objects.none()

    if query:
        tickets = Ticket.objects.filter(
            Q(subject__icontains=query) | Q(description__icontains=query) 

        )

    return render(request, 'tickets/ticket_search.html', {
        'tickets': tickets,
        'query': query,
    })

@login_required
def ticket_search_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket_search_detail.html', {
        'form': form,
        'ticket': ticket,
    })

@login_required
def ticket_confirm_delete_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('all_tickets')
    return render(request, 'tickets/ticket_confirm_delete.html', {'ticket': ticket})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)

        if form.is_valid():
            ticket = form.save(commit=False)
            
            if ticket.subject != form.cleaned_data['subject']:
                messages.success(request, 'Subject updated successfully.')
            if ticket.description != form.cleaned_data['description']:
                messages.success(request, 'Description updated successfully.')
            if ticket.solution_description != form.cleaned_data['solution_description']:
                messages.success(request, 'Solution updated successfully.')
            if ticket.effort != form.cleaned_data['effort']:
                messages.success(request, 'Effort updated successfully.')
            if ticket.status != form.cleaned_data['status']:
                messages.success(request, 'Status updated successfully.')
            if ticket.assigned_to != form.cleaned_data['assigned_to']:
                messages.success(request, 'Assigned to updated successfully.')
            if ticket.ticket_customer != form.cleaned_data['ticket_customer']:
                messages.success(request, 'Customer updated successfully.')
            if ticket.ticket_customer_product != form.cleaned_data['ticket_customer_product']:
                messages.success(request, 'Product updated successfully.')

            if ticket.status == 'resolved' and (not ticket.effort or ticket.effort == 0):
                form.add_error('effort', 'Effort must be non-zero for resolved tickets.')
                return render(request, 'tickets/ticket_detail.html', {'form': form, 'ticket': ticket})

            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = TicketForm(instance=ticket)

    if ticket.ticket_customer:
        form.fields['ticket_customer_product'].queryset = CustomerProduct.objects.filter(customer=ticket.ticket_customer)

    attachments = ticket.attachments.all()

    return render(request, 'tickets/ticket_detail.html', {
        'form': form,
        'ticket': ticket,
        'attachments': attachments
    })



def get_customer_products(request):
    customer_id = request.GET.get('customer_id')
    products = []
    
    if customer_id:
        products = CustomerProduct.objects.filter(customer_id=customer_id).values('id', 'product__name')

    return JsonResponse(list(products), safe=False)



