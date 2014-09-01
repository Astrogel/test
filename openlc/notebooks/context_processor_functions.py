from models import Category

def get_categories(request):
    return {'menu_categories': Category.objects.all()}