from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(BusinessUser)
admin.site.register(CheersUser)
admin.site.register(SalePoint)
admin.site.register(DrinkOrderCount)
admin.site.register(DrinkOrder)
admin.site.register(Drink)
admin.site.register(Mixer)
admin.site.register(Location)
admin.site.register(Music)
admin.site.register(Order)
