from django import forms
from customers.models import Customer, CustomerProduct, CustomerServer, CustomerContact, CustomerAttachment, CustomerVPNInfo

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer name'}),  # Bootstrap 'form-control' class
        }

class CustomerProductForm(forms.ModelForm):
    class Meta:
        model = CustomerProduct
        fields = ['product']

    def __init__(self, *args, **kwargs):
        super(CustomerProductForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Select a product'  # Placeholder ekliyoruz
        })


class CustomerVPNInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerVPNInfo
        fields = ['vpn_info']

    def __init__(self, *args, **kwargs):
        super(CustomerVPNInfoForm, self).__init__(*args, **kwargs)
        self.fields['vpn_info'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter VPN information'  # Placeholder ekliyoruz
        })


class CustomerServerForm(forms.ModelForm):
    class Meta:
        model = CustomerServer
        fields = ['name', 'ip_address']

    def __init__(self, *args, **kwargs):
        super(CustomerServerForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter server name'  # Placeholder ekliyoruz
        })
        self.fields['ip_address'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter server IP address'  # Placeholder ekliyoruz
        })


class CustomerContactForm(forms.ModelForm):
    class Meta:
        model = CustomerContact
        fields = ['contact_name', 'contact_email', 'contact_phone']

    def __init__(self, *args, **kwargs):
        super(CustomerContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter contact name'  # Placeholder ekliyoruz
        })
        self.fields['contact_email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter contact email'  # Placeholder ekliyoruz
        })
        self.fields['contact_phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter contact phone (optional)'  # Placeholder ekliyoruz
        })


class CustomerAttachmentForm(forms.ModelForm):
    class Meta:
        model = CustomerAttachment
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(CustomerAttachmentForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Upload an attachment'  # Placeholder ekliyoruz
        })




