from django.contrib import admin
from .models import Flight, Airport, Passenger
# Register your models here.

class flightAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "duration")

class passengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)
    
admin.site.register(Flight, flightAdmin)
admin.site.register(Airport)
admin.site.register(Passenger, passengerAdmin)
