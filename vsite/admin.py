from django.contrib import admin
from .models import pnj , pj_note
# Register your models here.
class adminPnj(admin.ModelAdmin):
    list_display = ['uid', 'img_id','name','description','age','cast',
        'attributes']
    ordering = ['uid']

class admin_pj_note(admin.ModelAdmin):
    list_display =['uid','poster_id','pnj_id','note'    ]
    ordering = ['uid']


admin.site.register(pnj , adminPnj)
admin.site.register(pj_note , admin_pj_note)