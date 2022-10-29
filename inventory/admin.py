from django.contrib import admin

from .models import Blueprint, Device, BOM, Inventory, Part

admin.site.register(Blueprint)
admin.site.register(BOM)
admin.site.register(Inventory)
admin.site.register(Device)
admin.site.register(Part)