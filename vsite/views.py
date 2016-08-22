from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *

def home(request):
    context = {
        'favicon': 'vsite/favicon.ico',
        'style': 'vsite/style.css',
        'main_img': 'vsite/main_img_3.jpg',
        'main_profile': 'vsite/main_char_1.jpg',
        'main_char': 'vsite/main_char_1.jpg',
        'main_github': 'vsite/main_github_1.png',
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context,request))

def pnj_index(request):
    if request.user.is_authenticated():
        current_user = '<a href="/account">{} : gérer son compte</a>'.format(request.user)
    else:
        current_user = '<a href="/login">Se connecter</a>'
    context = {
        'favicon': 'vsite/favicon.ico',
        'style': 'vsite/style.css',
        'main_img': 'vsite/main_img_3.jpg',
        'content': models.pnj.objects.filter(visible=True),
        'current_user': current_user,
    }
    template = loader.get_template('pnj_index.html')
    return HttpResponse(template.render(context,request))

def pnj_view(request, character_uid):
    characters = pnj.objects.all()
    character = pnj.objects.get(uid = character_uid)
    if request.user.is_authenticated():
        current_user = '<a href="/account">{} : gérer son compte</a>'.format(request.user)
    else:
        current_user = '<a href="/login">Se connecter</a>'
    cast_verbose = character.cast_choice[character.cast-1][1]
    context = { 'content':characters ,
                'avatar': character.img_id ,
                'description': character.description ,
                'name': character.name ,
                'cast': 'caste des {}'.format(cast_verbose) ,
                'attributes':character.attributes.split(',') ,
                'stuff': character.stuff.split(',') ,
                'style': 'vsite/style.css',
                'current_user': current_user,
                'favicon': 'vsite/favicon.ico'
    }
    template = loader.get_template('pnj_view.html')
    return HttpResponse(template.render(context , request ))