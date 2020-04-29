from django.contrib import admin
from .models import *

admin.site.register(Maker)
admin.site.register(PModel)
admin.site.register(PPhoto)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pmodel', 'nickname', 'price', 'year')
    search_fields = ('nickname',)
    ordering = ('-price',)

admin.site.register(Product, ProductAdmin)
