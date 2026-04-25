from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(MealBooking)
admin.site.register(Inventory)
admin.site.register(Waste)
admin.site.register(Donation)
admin.site.register(ScanLog)