from django.contrib import admin
from .models import User, Category, Subcategory, Service, Address

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Service)
admin.site.register(Address)

