from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import pandas as pd
from tickets.models import Ticket, Customer
from customers.models import CustomerProduct  
from django.contrib.auth import get_user_model

User = get_user_model()

def is_manager_check(user):
    return user.is_authenticated and user.is_manager

@user_passes_test(is_manager_check)
def report_view(request):
    customers = Customer.objects.all()
    products = CustomerProduct.objects.values('product__id', 'product__name').distinct()
    users = User.objects.all()  

    tickets = Ticket.objects.none()

    if request.GET.get('start_date') or request.GET.get('customer') or request.GET.get('product') or request.GET.get('status') or request.GET.get('effort') or request.GET.get('assigned_to'):
        tickets = Ticket.objects.all()

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        customer = request.GET.get('customer')
        product = request.GET.get('product')
        status = request.GET.get('status')
        effort = request.GET.get('effort')
        assigned_to = request.GET.get('assigned_to')  

        if start_date:
            try:
                start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
                tickets = tickets.filter(created_at__date__gte=start_date)
            except (ValueError, TypeError):
                pass

        if end_date:
            try:
                end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')
                tickets = tickets.filter(created_at__date__lte=end_date)
            except (ValueError, TypeError):
                pass

        if customer == 'none':
            tickets = tickets.filter(ticket_customer__isnull=True)
        elif customer and customer != 'all':
            tickets = tickets.filter(ticket_customer_id=customer)

        if product == 'none':
            tickets = tickets.filter(ticket_customer_product__isnull=True)
        elif product and product != 'all':
            tickets = tickets.filter(ticket_customer_product__product_id=product)

        if status and status != 'all':
            tickets = tickets.filter(status=status)

        if effort:
            try:
                tickets = tickets.filter(effort=effort)
            except ValueError:
                pass

        if assigned_to == 'none':
            tickets = tickets.filter(assigned_to__isnull=True)
        elif assigned_to and assigned_to != 'all':
            tickets = tickets.filter(assigned_to_id=assigned_to)

    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if 'export' in request.GET:
        ticket_values = list(tickets.values('subject', 'description', 'solution_description', 'ticket_customer__name', 'assigned_to__username', 'status', 'effort'))
        df = pd.DataFrame(ticket_values)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="tickets_report.xlsx"'
        df.to_excel(response, index=False)
        return response

    return render(request, 'reports/report_form.html', {
        'page_obj': page_obj,
        'customers': customers,
        'products': products,
        'users': users,  
    })