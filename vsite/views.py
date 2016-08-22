from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import pnj

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
        navbar_user_icon = '<a href="/account"><img class="navbar_img" src="/static/vsite/navbar_account.png"></a>'
    else:
        navbar_user_icon = '<a href="/login"><img class="navbar_img" src="/static/vsite/navbar_login.png"></a>'
    context = {
        'favicon': 'vsite/favicon.ico',
        'style': 'vsite/style.css',
        'main_img': 'vsite/main_img_3.jpg',
        'content': pnj.objects.filter(visible=True),
        'navbar_icon_home':'vsite/navbar_home.png',
        'navbar_icon_login':'vsite/navbar_login.png',
        'navbar_icon_account': 'vsite/navbar_account.png',
        'navbar_user_icon':navbar_user_icon
    }
    template = loader.get_template('pnj_index.html')
    return HttpResponse(template.render(context,request))

def pnj_view(request, character_uid):
    character = pnj.objects.get(uid = character_uid)
    if request.user.is_authenticated():
        navbar_user_icon = '<a href="/account"><img class="navbar_img" src="/static/vsite/navbar_account.png"></a>'
    else:
        navbar_user_icon = '<a href="/login"><img class="navbar_img" src="/static/vsite/navbar_login.png"></a>'
    cast_verbose = character.cast_choice[character.cast-1][1]
    context = {
        'favicon': 'vsite/favicon.ico',
        'style': 'vsite/style.css',
        'main_img': 'vsite/main_img_3.jpg',
        'avatar': character.img_id ,
        'description': character.description ,
        'name': character.name ,
        'cast': 'caste des {}'.format(cast_verbose) ,
        'attributes':character.attributes.split(',') ,
        'stuff': character.stuff.split(',') ,
        'style': 'vsite/style.css',
        'favicon': 'vsite/favicon.ico',
        'navbar_icon_home':'vsite/navbar_home.png',
        'navbar_icon_login':'vsite/navbar_login.png',
        'navbar_icon_account': 'vsite/navbar_account.png',
        'navbar_user_icon':navbar_user_icon
        }
    template = loader.get_template('pnj_view.html')
    return HttpResponse(template.render(context , request ))

def account(request):
    context = {
        'style': 'vsite/style.css',
        }
    template = loader.get_template('account.html')
    return HttpResponse(template.render(context , request ))
