from django.contrib import admin
from .models import Booking
# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'futsal', 'date', 'time')
    search_fields = ('date',)


admin.site.register(Booking, BookingAdmin)