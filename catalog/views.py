from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    products = Product.objects.filter(is_active=True)[:12]
    return render(request, 'catalog/home.html', {'products': products})
