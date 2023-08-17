from django.contrib import admin
from . import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'f_name', 'l_name', 'group']
    list_filter = ['group']
    # search_fields = ['username']


admin.site.register(models.Profile, ProfileAdmin)
