from .models import Category
def global_vars(request):
    categories = Category.objects.all()
    cart_count = 0
    return {'categories': categories, 'cart_count': cart_count}
