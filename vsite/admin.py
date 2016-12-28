from django.contrib import admin
from .models import Pnj, PjNote, HomeItems, PjCharacter, GameLog, Jobs, ItemRecipes, Item, Place, Phenomenon, Creature
# Register your models here.

class AdminPnj(admin.ModelAdmin):
    list_display =['uid', 'owner', 'name', 'first_job', 'second_job', 'stuff', 'is_creature', 'is_visible']
    ordering = ['uid']
admin.site.register(Pnj , AdminPnj)

class AdminPjNote(admin.ModelAdmin):
    list_display =['uid','poster_id','pnj_id','note']
    ordering = ['uid']
admin.site.register(PjNote , AdminPjNote)

class AdminHomeItems(admin.ModelAdmin):
    list_display =['uid','name', 'order_position', 'description', 'img_id', 'link']
    ordering = ['uid']
admin.site.register(HomeItems , AdminHomeItems)

class AdminPjCharacter(admin.ModelAdmin):
    list_display =['uid', 'owner', 'name', 'first_job', 'second_job','stuff']
    ordering = ['uid']
admin.site.register(PjCharacter , AdminPjCharacter)

class AdminGameLog(admin.ModelAdmin):
    list_display =['uid','img_id', 'corpus', 'created_date']
    ordering = ['created_date']
admin.site.register(GameLog , AdminGameLog)

class AdminJobs(admin.ModelAdmin):
    list_display =['uid','name', 'job_type', 'job_description']
    ordering = ['uid']
admin.site.register(Jobs , AdminJobs)

class AdminItemRecipes(admin.ModelAdmin):
    list_display =['uid','name',]
    ordering = ['uid']
admin.site.register(ItemRecipes , AdminItemRecipes)

class AdminItem(admin.ModelAdmin):
    list_display =['uid','name', 'owner_id']
    ordering = ['uid']
admin.site.register(Item , AdminItem)

class AdminPlace(admin.ModelAdmin):
    list_display =['gid','name']
    ordering = ['gid']
admin.site.register(Place , AdminPlace)

class AdminPhenomenon(admin.ModelAdmin):
    list_display =['gid','name']
    ordering = ['gid']
admin.site.register(Phenomenon , AdminPhenomenon)

class AdminCreature(admin.ModelAdmin):
    list_display =['uid','name']
    ordering = ['uid']
admin.site.register(Creature , AdminCreature)