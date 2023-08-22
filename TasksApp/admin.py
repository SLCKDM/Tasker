from django.contrib import admin
from . import models
# Register your models here.


class CheckListsStack(admin.StackedInline):
    model = models.CheckList
    show_change_link=True
    extra = 0


class CheckListsElementsStack(admin.TabularInline):
    model = models.CheckListItem
    show_change_link=True
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    inlines = [CheckListsStack]
    list_display = ['title', 'deadline', 'description', 'author', 'done',
                    'done_dt']
    fieldsets = [
        ('Main', {'classes': ["extrapretty"],
                  'fields': ['title', 'description']}),
        ('Users', {'classes': ["extrapretty"],
                   'fields': ['author', 'executors']}),
        ('Dates', {'classes': ["extrapretty"],
                   'fields': ['deadline', 'done', 'done_dt']}),
    ]
    list_filter = ['title', 'deadline', 'author', 'done', 'done_dt',
                   'executors']
    search_fields = ['title', 'description']


class CheckListAdmin(admin.ModelAdmin):
    inlines = [CheckListsElementsStack]
    list_display = ['name', 'task']

class CheckListItemAdmin(admin.ModelAdmin):
    list_display = ['text', 'done', 'check_list']

admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.CheckList, CheckListAdmin)
admin.site.register(models.CheckListItem, CheckListItemAdmin)
