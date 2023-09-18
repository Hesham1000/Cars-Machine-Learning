from unicodedata import name
from django.contrib import admin
from .models import Car


class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'active']
    list_display_links = ['name', 'price']
    # list_editable = ['price']
    search_fields = ['name', 'id']
    list_filter = ['brand', 'id', 'price', 'active']


admin.site.register(Car, CarAdmin)
admin.site.site_header = 'Drive Safely'
admin.site.site_title = 'Hesham'

