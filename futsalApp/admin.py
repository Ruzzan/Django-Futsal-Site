from django.contrib import admin
from . import models
# Register your models here.

class FutsalAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(models.Futsal, FutsalAdmin)

