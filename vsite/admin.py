from django.contrib import admin
from .models import pnj
# Register your models here.
class adminPnj(admin.ModelAdmin):
	list_display = ['uid', 'img_id','name','description','age','cast',
		'attributes']
	ordering = ['uid']

admin.site.register(pnj , adminPnj)