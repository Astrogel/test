from django.contrib import admin
from models import UserProfile, Notebook, Category

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Notebook)
admin.site.register(Category)
