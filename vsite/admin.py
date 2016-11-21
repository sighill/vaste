from django.contrib import admin
from .models import pnj , pj_note, home_items
# Register your models here.

class adminPnj(admin.ModelAdmin):
    list_display = ['uid', 'img_id','name','description','cast',
        'attributes']
    ordering = ['uid']
admin.site.register(pnj , adminPnj)


class admin_pj_note(admin.ModelAdmin):
    list_display =['uid','poster_id','pnj_id','note'    ]
    ordering = ['uid']
admin.site.register(pj_note , admin_pj_note)

class admin_home_items(admin.ModelAdmin):
    list_display =['uid','name', 'order_position', 'description', 'img_id', 'link']
    ordering = ['uid']
admin.site.register(home_items , admin_home_items)