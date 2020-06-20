from django.contrib import admin
from .import models
# Register your models here.
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
admin.site.register(models.Team,TeamAdmin)
admin.site.register(models.TeamMember)
