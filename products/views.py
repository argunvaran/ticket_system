from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def product_list_view(request):
    products = Product.objects.all()  
    form = ProductForm(request.POST or None)
    
    if form.is_valid():
        form.save()  
        return redirect('product_list')  

    if request.method == 'POST' and 'delete_product' in request.POST:
        product_id = request.POST.get('product_id')
        product_to_delete = get_object_or_404(Product, id=product_id)
        product_to_delete.delete()
        return redirect('product_list')

    return render(request, 'products/product_list.html', {'products': products, 'form': form})
