#urls.py
from django.conf.urls import url , include
from . import views

urlpatterns = [
	url(r'^$', views.home ),
	url(r'^pnj/', views.pnj_index)
]