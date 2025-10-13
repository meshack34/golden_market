# catalog/context_processors.py
from .models import category
from .models.category import Category

def site_categories(request):
    return {'site_categories': Category.objects.filter(is_active=True)}
