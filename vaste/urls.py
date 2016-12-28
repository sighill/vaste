"""vaste URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin
from  django.contrib.auth.views import password_change
from vsite import views
from vsite.models import Place, Phenomenon, Creature, Pnj, PjCharacter

urlpatterns = [
    # general urls
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Home),
    url(r'^account/', views.Account, name='account'),
    url(r'^log/', views.Log, name='gamelog'),
    # game entity indexes
    url(r'^pnj/$', views.EntityIndex, {'obj_to_display': Pnj}),
    url(r'^pj/$', views.EntityIndex, {'obj_to_display': PjCharacter}),
    url(r'^places/$', views.EntityIndex, {'obj_to_display': Place}),
    url(r'^creatures/$', views.EntityIndex, {'obj_to_display': Creature}),
    url(r'^pheno/$', views.EntityIndex, {'obj_to_display': Phenomenon}),
    # game entity specific views
    url(r'^pnj/view/(?P<obj_pk>\d+)', 
        views.EntityView, 
        {'obj_to_display': Pnj}, 
        name='pnj'),
    url(r'^creatures/view/(?P<obj_pk>\d+)', 
        views.EntityView, 
        {'obj_to_display': Creature}, 
        name='creature', ),
    url(r'^pj/view/(?P<character_uid>\d+)', views.PjView, name='pj'),
    url('^', include('django.contrib.auth.urls')),
    # note mechanisms spcial urls
    url(r'^switchprivacy/(?P<note_uid>\d+)', views.NotePrivacySwitch, name= 'switch_privacy'),
    url(r'^notedelete/(?P<note_uid>\d+)', views.NoteDelete, name= 'note_delete'),

]

'''
^login/$ [name='login']
^logout/$ [name='logout']
^password_change/$ [name='password_change']
^password_change/done/$ [name='password_change_done']
^password_reset/$ [name='password_reset']
^password_reset/done/$ [name='password_reset_done']
^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
^reset/done/$ [name='password_reset_complete']
'''