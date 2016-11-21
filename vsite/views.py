from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import pnj, pj_note, home_items
from .forms import pj_note_form

#####################################################################


def home(request):
    context = {
        'style': 'vsite/style.css',
        'home_items': home_items.objects.filter().exclude(name='Accueil').order_by('order_position'),
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))


#####################################################################
def pnj_index(request, view_filter):
    if view_filter == 'creatures':
        content = pnj.objects.filter(visible=True, is_creature = True)
    else:
        content = pnj.objects.filter(visible=True, is_creature = False)

    context = {
        'style': 'vsite/style.css',
        'navbar_items': home_items.objects.all(),
        'content': content,
    }
    template = loader.get_template('pnj_index.html')
    return HttpResponse(template.render(context, request))


#####################################################################
def pnj_view(request, character_uid):
    character = pnj.objects.get(uid=character_uid)

    # Object attributes transformation for better display
    character.stuff = character.stuff.split(',')
    cast_verbose = character.cast_choice[character.cast-1][1]
    character.cast = 'caste des {}'.format(cast_verbose)
    
    # Content choice if the user is auth or not
    if request.user.is_authenticated():
        # Récupération des notes personnelles pour le pnj affiché
        pj_note_qs = pj_note.objects.filter(
            pnj_id=character_uid, poster_id=request.user.id)
        try:
            pj_note_content = []
            for entry in pj_note_qs:
                formatted_entry = '({}-{}-{}) : « {} »'.format(entry.created_date.day , entry.created_date.month , entry.created_date.year, entry.note)
                pj_note_content.append(formatted_entry)
            pj_note_content[0] # Retourne IndexError si vide
        except IndexError:
            pj_note_content = ['Pas de note personnelle enregistrée.']
    else:
        # Choix des icones de la navbar
        navbar_user_icon = '<a href="/login"><img class="navbar_img" src="/static/vsite/navbar_login.png"></a>'
        # Message générique pour la partie notes personnelles
        pj_note_content = []
    form = pj_note_form()

    context = {
        # Données génériques communes à toutes les pages
        'style': 'vsite/style.css',
        'navbar_items': home_items.objects.all(),

        # Données spécifiques à la vue
        'character': character,
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
        'navbar_items': home_items.objects.all(),
        }
        
        template = loader.get_template('account.html')
        return HttpResponse(template.render(context , request ))
    else:
        return HttpResponseRedirect('/login')


