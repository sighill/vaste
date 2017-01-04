from django.contrib import admin
from .models import *
# Register your models here.


class AdminPjNote(admin.ModelAdmin):
    list_display =['uid','poster_id', 'note_target','note']
    ordering = ['uid']
admin.site.register(PjNote , AdminPjNote)

class AdminHomeItems(admin.ModelAdmin):
    list_display =['uid','name', 'order_position', 'description', 'img_id', 'link']
    ordering = ['uid']
admin.site.register(HomeItems , AdminHomeItems)

class AdminGameLog(admin.ModelAdmin):
    list_display =['uid','img_id', 'img_link', 'created_date']
    ordering = ['created_date']
admin.site.register(GameLog , AdminGameLog)

class AdminJobs(admin.ModelAdmin):
    list_display =['uid','name', 'job_description']
    ordering = ['uid']
admin.site.register(Jobs , AdminJobs)

class AdminSkills(admin.ModelAdmin):
    list_display =['uid','name', 'is_unique']
    ordering = ['uid']
admin.site.register(Skills , AdminSkills)

class AdminItemRecipes(admin.ModelAdmin):
    list_display =['uid', 'item_type', 'name', 'ia_type', 'ia', 'iaq', 'ib_type', 
    'ib', 'ibq', 'ic_type', 'ic', 'icq']
    ordering = ['uid']
admin.site.register(ItemRecipes , AdminItemRecipes)

class AdminItem(admin.ModelAdmin):
    list_display =['uid','owner', 'quantity', 'name', 'recipe', 'ia_type' ]
    ordering = ['owner']
admin.site.register(Item , AdminItem)

class AdminGameEntity(admin.ModelAdmin):
    list_display =['uid','name', 'is_visible', 'more']
    ordering = ['uid']
admin.site.register(GameEntity , AdminGameEntity)

class AdminPnj(admin.ModelAdmin):
    list_display =['uid', 'name', 'first_job', 'second_job']
    ordering = ['uid']
admin.site.register(Pnj , AdminPnj)

class AdminPjCharacter(admin.ModelAdmin):
    list_display =['uid', 'name', 'more']
    ordering = ['uid']
admin.site.register(PjCharacter , AdminPjCharacter)

class AdminCreature(admin.ModelAdmin):
    list_display =['uid', 'name', 'more']
    ordering = ['uid']
admin.site.register(Creature , AdminCreature)

class AdminPlace(admin.ModelAdmin):
    list_display =['uid', 'name', 'more']
    ordering = ['uid']
admin.site.register(Place , AdminPlace)

class AdminPhenomenon(admin.ModelAdmin):
    list_display =['uid', 'name', 'more']
    ordering = ['uid']
admin.site.register(Phenomenon , AdminPhenomenon)

class AdminIgCreature(admin.ModelAdmin):
    list_display =['uid', 'name', 'more']
    ordering = ['uid']
admin.site.register(IgCreature , AdminIgCreature)
