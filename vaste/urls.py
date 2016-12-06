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

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Home),
    url(r'^pnj/$', views.PnjIndex, {'view_filter': 'pnj'}),
    url(r'^creatures/$', views.PnjIndex, {'view_filter': 'creatures'}),
    url(r'^pj/$', views.PnjIndex, {'view_filter': 'pj'}),
    url(r'^pnj/view/(?P<pnj_uid>\d+)', views.PnjView, name='pnj'),
    url(r'^creatures/view/(?P<pnj_uid>\d+)', views.PnjView, name='pnj'),
    url(r'^pj/view/(?P<character_uid>\d+)', views.PjView, name='pj'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^account/', views.Account, name='account'),
    url(r'^log/', views.Log, name='gamelog'),
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