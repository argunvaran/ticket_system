from django.shortcuts import render, get_object_or_404, redirect
from customers.models import Customer, CustomerProduct, CustomerServer, CustomerContact, CustomerAttachment, CustomerVPNInfo
from customers.forms import CustomerForm, CustomerProductForm, CustomerServerForm, CustomerContactForm, CustomerAttachmentForm, CustomerVPNInfoForm
from products.models import Product

from django.db import IntegrityError
from django.contrib import messages


def customer_list_view(request):
    customers = Customer.objects.all()
    form = CustomerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('customer_list')

    if request.method == 'POST' and 'delete_customer' in request.POST:
        customer_id = request.POST.get('customer_id')
        customer_to_delete = get_object_or_404(Customer, id=customer_id)
        customer_to_delete.delete()
        return redirect('customer_list')

    return render(request, 'customers/customer_list.html', {'customers': customers, 'form': form})


def customer_detail_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    attachments = customer.attachments.all()

    try:
        vpn_info = customer.vpn_info.get()
    except CustomerVPNInfo.DoesNotExist:
        vpn_info = None

    product_form = CustomerProductForm()
    server_form = CustomerServerForm()
    contact_form = CustomerContactForm()
    attachment_form = CustomerAttachmentForm()
    vpn_info_form = CustomerVPNInfoForm(instance=vpn_info)

    if request.method == 'POST':
        if 'add_product' in request.POST:
            product_form = CustomerProductForm(request.POST)
            if product_form.is_valid():
                try:
                    product = product_form.save(commit=False)
                    product.customer = customer
                    product.save()
                    messages.success(request, 'Product added successfully.')
                    return redirect('customer_detail', customer_id=customer_id)
                except IntegrityError:
                    
                    messages.error(request, 'This product has already been added to this customer.')
                    
        elif 'add_server' in request.POST:
            server_form = CustomerServerForm(request.POST)
            if server_form.is_valid():
                server = server_form.save(commit=False)
                server.customer = customer
                server.save()
                messages.success(request, 'Server added successfully.')
                return redirect('customer_detail', customer_id=customer_id)

        elif 'add_contact' in request.POST:
            contact_form = CustomerContactForm(request.POST)
            if contact_form.is_valid():
                contact = contact_form.save(commit=False)
                contact.customer = customer
                contact.save()
                messages.success(request, 'Contact added successfully.')
                return redirect('customer_detail', customer_id=customer_id)

        elif 'add_attachment' in request.POST or request.FILES:
            attachment_form = CustomerAttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.customer = customer
                attachment.save()
                messages.success(request, 'Attachment uploaded successfully.')
                return redirect('customer_detail', customer_id=customer_id)

        elif 'update_vpn' in request.POST:
            vpn_info_form = CustomerVPNInfoForm(request.POST, instance=vpn_info)
            if vpn_info_form.is_valid():
                vpn_info = vpn_info_form.save(commit=False)
                vpn_info.customer = customer
                vpn_info.save()
                messages.success(request, 'VPN info updated successfully.')
                return redirect('customer_detail', customer_id=customer_id)

    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'attachments': attachments,
        'vpn_info': vpn_info,
        'product_form': product_form,
        'server_form': server_form,
        'contact_form': contact_form,
        'attachment_form': attachment_form,
        'vpn_info_form': vpn_info_form
    })

# ----------------------------------------------

def delete_product(request, customer_id, product_id):
    product = get_object_or_404(CustomerProduct, id=product_id, customer_id=customer_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('customer_detail', customer_id=customer_id)

def delete_server(request, customer_id, server_id):
    server = get_object_or_404(CustomerServer, id=server_id, customer_id=customer_id)
    server.delete()
    messages.success(request, 'Server deleted successfully.')
    return redirect('customer_detail', customer_id=customer_id)

def delete_contact(request, customer_id, contact_id):
    contact = get_object_or_404(CustomerContact, id=contact_id, customer_id=customer_id)
    contact.delete()
    messages.success(request, 'Contact deleted successfully.')
    return redirect('customer_detail', customer_id=customer_id)

def delete_attachment(request, customer_id, attachment_id):
    attachment = get_object_or_404(CustomerAttachment, id=attachment_id, customer_id=customer_id)
    attachment.delete()
    messages.success(request, 'Attachment deleted successfully.')
    return redirect('customer_detail', customer_id=customer_id)