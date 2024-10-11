from django.db import models
from products.models import Product

class Customer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class CustomerProduct(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['customer', 'product']

    def __str__(self):
        return f"{self.customer.name} - {self.product.name}"

class CustomerServer(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='servers')
    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class CustomerContact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.contact_name

class CustomerVPNInfo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='vpn_info')
    vpn_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.name} - VPN Info"

class CustomerAttachment(models.Model):
    customer = models.ForeignKey(Customer, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='customer_attachments/')

    def __str__(self):
        return self.file.name
