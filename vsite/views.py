from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
from django.template import loader
from .models import pnj , pj_note
from .forms import pj_note_form

#####################################################################
def home(request):
    if request.user.is_authenticated():
        main_userbay_title = 'Journal ({})'.format(request.user)
        main_userbay_href = '/account'
    else:
        main_userbay_title = 'Se connecter'
        main_userbay_href = '/login'
    context = {
        'style': 'vsite/style.css',
        'main_userbay_title' : main_userbay_title,
        'main_userbay_href' : main_userbay_href,
        'main_img': 'vsite/main_img_3.jpg',
        'main_profile': 'vsite/main_char_1.jpg',
        'main_char': 'vsite/main_pnj.jpg',
        'main_github': 'vsite/main_github_1.png',
        'navbar_skull': 'vsite/navbar_skull.png',
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context,request))


#####################################################################
def pnj_index(request):
    if request.user.is_authenticated():
        navbar_user_icon = '<a href="/account"><img class="navbar_img" src="/static/vsite/navbar_account.png"></a>'
    else:
        navbar_user_icon = '<a href="/login"><img class="navbar_img" src="/static/vsite/navbar_login.png"></a>'
    context = {
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


#####################################################################
def pnj_view(request, character_uid):
    character = pnj.objects.get(uid = character_uid)
    # Différenciation du contenu en fonction de 
    if request.user.is_authenticated():
        # Choix des icones de la navbar
        navbar_user_icon = '<a href="/account"><img class="navbar_img" src="/static/vsite/navbar_account.png"></a>'
        # Récupération des notes personnelles pour le pnj affiché
        pj_note_qs = pj_note.objects.filter(pnj_id = character_uid , poster_id = request.user.id)
        try:
            pj_note_content = []
            for entry in pj_note_qs:
                formatted_entry = '({}-{}-{}) : \n« {} »'.format(entry.created_date.day , entry.created_date.month , entry.created_date.year, entry.note)
                pj_note_content.append(formatted_entry)
            pj_note_content[0] # Retourne IndexError si vide
        except IndexError:
            pj_note_content = ['Pas de note personnelle enregistrée.']
    else:
        # Choix des icones de la navbar
        navbar_user_icon = '<a href="/login"><img class="navbar_img" src="/static/vsite/navbar_login.png"></a>'
        # Message générique pour la partie notes personnelles
        pj_note_content = ['Connectez vous pour voir/poster une note personnelle.']
    cast_verbose = character.cast_choice[character.cast-1][1]
    form = pj_note_form()
    context = {
        # Données génériques communes à toutes les pages
        'style': 'vsite/style.css',
        'main_img': 'vsite/main_img_3.jpg',
        'navbar_icon_home': 'vsite/navbar_home.png',
        'navbar_icon_login': 'vsite/navbar_login.png',
        'navbar_icon_account': 'vsite/navbar_account.png',
        'navbar_user_icon': navbar_user_icon,
        # Données spécifiques à la vue
        'avatar': character.img_id ,
        'description': character.description ,
        'name': character.name ,
        'cast': 'caste des {}'.format(cast_verbose) ,
        'attributes': character.attributes.split(',') ,
        'stuff': character.stuff.split(',') ,
        'pj_note_content': pj_note_content,
        'form':form,
        }
    template = loader.get_template('pnj_view.html')

    if request.method == 'GET': 
        return HttpResponse(template.render(context , request ))

    if request.method == 'POST':
        form = pj_note_form(request.POST)
        if form.is_valid():
                note_to_create = form.cleaned_data['note']
                poster_id = request.user
                pnj_id = pnj.objects.get(pk=character_uid)
                post = pj_note.objects.create(
                    poster_id=poster_id , pnj_id=pnj_id , note=note_to_create)
        return HttpResponseRedirect(character_uid)


#####################################################################
def account(request):
    if request.user.is_authenticated():
        pj_note_qs = pj_note.objects.filter(poster_id = request.user.id).order_by('pnj_id')
        pnj_list = pnj.objects.all()
        try:
            pj_note_content = []
            for entry in pj_note_qs:
                formatted_entry = '({}-{}-{}) à propos de {} : \n« {} »'.format(entry.created_date.day , entry.created_date.month , entry.created_date.year, entry.pnj_id , entry.note)
                pj_note_content.append(formatted_entry)
            pj_note_content[0] # Retourne IndexError si vide
        except IndexError:
            pj_note_content = ['Pas de note personnelle enregistrée.']
        context = {
        'style': 'vsite/style.css',
        'pj_note_content': pj_note_content,
        'main_img': 'vsite/main_img_3.jpg',
        'navbar_icon_home': 'vsite/navbar_home.png',
        }
        template = loader.get_template('account.html')
        return HttpResponse(template.render(context , request ))
    else:
        HttpResponseRedirect('/login')


