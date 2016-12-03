from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Pnj, PjNote, HomeItems, PjCharacter, GameLog, Item
from .forms import PjNoteForm

#####################################################################


def Home(request):
    context = {
        'style': 'vsite/style.css',
        'home_items': HomeItems.objects.filter().exclude(name='Accueil').order_by('order_position'),
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))


#####################################################################
def PnjIndex(request, view_filter):
    if view_filter == 'creatures':
        content = Pnj.objects.filter(is_visible=True, is_creature = True)
    elif view_filter == 'pj':
        content = PjCharacter.objects.all()
    else:
        content = Pnj.objects.filter(is_visible=True, is_creature = False)

    context = {
        'style': 'vsite/style.css',
        'navbar_items': HomeItems.objects.all().order_by('order_position'),
        'content': content,
    }
    template = loader.get_template('pnj_index.html')
    return HttpResponse(template.render(context, request))


#####################################################################
def PnjView(request, character_uid):
    character = Pnj.objects.get(uid=character_uid)

    # Object attributes transformation for better display
    character.stuff = character.stuff.split(',')
    
    # Content choice if the user is auth or not
    if request.user.is_authenticated():
        # Récupération des notes personnelles pour le pnj affiché
        pj_note_qs = PjNote.objects.filter(
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
        # Message générique pour la partie notes personnelles
        pj_note_content = []
    form = PjNoteForm()

    context = {
        # Données génériques communes à toutes les pages
        'style': 'vsite/style.css',
        'navbar_items': HomeItems.objects.all().order_by('order_position'),

        # Données spécifiques à la vue
        'character': character,
        'pj_note_content': pj_note_content,
        'form':form,
        }
    template = loader.get_template('pnj_view.html')

    if request.method == 'GET': 
        return HttpResponse(template.render(context , request ))

    if request.method == 'POST':
        form = PjNoteForm(request.POST)
        if form.is_valid():
            note_to_create = form.cleaned_data['note']
            poster_id = request.user.id
            pnj_id = Pnj.objects.get(pk=character_uid).uid
            post = PjNote.objects.create(
                poster_id=poster_id , pnj_id=pnj_id , note=note_to_create)
        return HttpResponseRedirect(character_uid)

#####################################################################
def PjView(request, character_uid):
    character = PjCharacter.objects.get(uid= character_uid)
    char_stuff = [item for item in Item.objects.filter(owner_id= character_uid)]

    # Object attributes transformation for better display
    character.stuff = character.stuff.split(',')

    context = {
        'style': 'vsite/style.css',
        'navbar_items': HomeItems.objects.all().order_by('order_position'),
        'character': character,
        'char_stuff': char_stuff,
        }
    template = loader.get_template('pj_view.html')

    return HttpResponse(template.render(context , request ))

#####################################################################
def Account(request):
    if request.user.is_authenticated():
        pj_note_qs = PjNote.objects.filter(poster_id = request.user.id).order_by('pnj_id')
        pnj_list = Pnj.objects.all()
        try:
            pj_note_content = []
            for entry in pj_note_qs:
                formatted_entry = '({}-{}-{}) à propos de {} : \n« {} »'.format(entry.created_date.day , entry.created_date.month , entry.created_date.year, entry.pnj_id , entry.note)
                pj_note_content.append(formatted_entry)
            pj_note_content[0] # Retourne IndexError si vide
        except IndexError:
            pj_note_content = ['Pas de note personnelle enregistrée.']

        # Character preparation for display
        character= PjCharacter.objects.get(owner_id=request.user.id)
        character.stuff = character.stuff.split(',')

        context = {
        'style': 'vsite/style.css',
        'pj_note_content': pj_note_content,
        'navbar_items': HomeItems.objects.all().order_by('order_position'),
        'character': character,
        }
        
        template = loader.get_template('account.html')
        return HttpResponse(template.render(context , request ))
    else:
        return HttpResponseRedirect('/login')

#####################################################################
def Log(request):
    # Building dynamic filters to display a part of the logs
    # By date of game
    date_filter= [i[0] for i in GameLog.objects.values_list('chapter_date').distinct()]
    context = {
        'style': 'vsite/style.css',
        'navbar_items': HomeItems.objects.all().order_by('order_position'),
        'log': GameLog.objects.all().order_by('order_position'),
        'date_filter': date_filter,
    }
    template = loader.get_template('game_log.html')
    return HttpResponse(template.render(context, request))