from django.contrib import admin
from .models import pnj, pj_note, home_items, pj_character, game_log
# Register your models here.

class adminPnj(admin.ModelAdmin):
    list_display = ['uid', 'img_id','name','description','cast',
        'attributes']
    ordering = ['uid']
admin.site.register(pnj , adminPnj)


class admin_pj_note(admin.ModelAdmin):
    list_display =['uid','poster_id','pnj_id','note']
    ordering = ['uid']
admin.site.register(pj_note , admin_pj_note)

class admin_home_items(admin.ModelAdmin):
    list_display =['uid','name', 'order_position', 'description', 'img_id', 'link']
    ordering = ['uid']
admin.site.register(home_items , admin_home_items)

class admin_pj_character(admin.ModelAdmin):
    list_display =['uid', 'owner', 'name', 'img_id', 'first_job', 'second_job', 'attributes','skills','stuff']
    ordering = ['uid']
admin.site.register(pj_character , admin_pj_character)

class admin_game_log(admin.ModelAdmin):
    list_display =['uid','img_id', 'corpus', 'created_date']
    ordering = ['created_date']
admin.site.register(game_log , admin_game_log)