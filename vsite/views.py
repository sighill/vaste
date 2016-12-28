from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Pnj, PjNote, HomeItems, PjCharacter, GameLog, Item, Creature, Place, Phenomenon
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

    context = {
        'style': 'vsite/style.css',
        'navbar_items': HomeItems.objects.all().order_by('order_position'),
        'log': GameLog.objects.all().order_by('order_position'),
    }
    template = loader.get_template('game_log.html')
    return HttpResponse(template.render(context, request))

#####################################################################
def NotePrivacySwitch(request, note_uid):
    '''
        This view is a simple function called to make a private
        note on a NPC public. Only one note from an user can be made
        public so the system makes any public note private.
        Only private notes will have this option.
    '''

    # Retrieve poster id
    poster_id = PjCharacter.objects.get(owner_id= request.user.id)

    # Retrieve note object
    note_to_switch = PjNote.objects.get(pk= note_uid)

    # make any other note private (only one normally)
    notes_to_discard = PjNote.objects.filter(poster_id= poster_id, is_public= True)

    # Discard public note and any other public note from 
    # same user (bug proof amirite)
    for public_note in notes_to_discard:
        if public_note.is_public == True:
            public_note.is_public = False
            public_note.save()
        else:
            pass

    # Now switch the wanted one :
    if note_to_switch.is_public == True:
        note_to_switch.is_public = False
        note_to_switch.save()
    else:
        note_to_switch.is_public = True
        note_to_switch.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#####################################################################
def NoteDelete(request, note_uid):
    '''
        This view is a simple function called to delete a note.
    '''

    # Retrieve poster id
    pjchar = PjCharacter.objects.get(owner_id= request.user.id)

    # Retrieve note object
    note_to_delete = PjNote.objects.get(pk= note_uid)

    # make sure the to-delete posts is owned by current user
    if pjchar.uid == note_to_delete.poster_id:
        note_to_delete.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#####################################################################
def EntityIndex(request, obj_to_display):
    
    # Some tables have  a 'is_visible' valeu that we have to filter
    # out before filling the content.
    if obj_to_display in [Pnj, Creature, Place, Phenomenon]:
        content = obj_to_display.objects.filter(is_visible= True)
    else:
        content = obj_to_display.objects.all()

    context = {
        'style': 'vsite/style.css',
        'content': content,
    }
    template = loader.get_template('generic_index.html')
    return HttpResponse(template.render(context, request))

#####################################################################
def EntityView(request, obj_to_display, obj_pk):
    '''
        DEV PHASE
        Entity view is the single entity viewer usable for every
        entity in the game, be it NPC, creature, place or phenomenon.
    '''

    # Get the object instance the user wants to display
    obj = obj_to_display.objects.get(pk= obj_pk)

    # If it's an NPC, get his stuff
    if obj_to_display in [Pnj, Creature]:
        obj.stuff = obj.stuff.split(',')
    
    # load notes if the user is authenticated
    if request.user.is_authenticated():

        # Get the PjCharacter of current user
        current_character = PjCharacter.objects.get(
            owner_id= request.user.id)

        # get all his PRIVATE notes ---------------------------------
        private_notes = [i for i in PjNote.objects.filter(
        note_target= obj_pk, poster_id= current_character, is_public= False)]
        
        # initiate the list
        private_notes_formatted = []

        # check if there's no private note
        if len(private_notes) == 0:
            private_notes_formatted = ['Pas de note personnelle enregistrée.']

        # if there are notes in the list of queried elements, we format them
        else:
            for private_note in private_notes:
                private_notes_formatted.append(
                    '<p>[ <a style="font-size:70%" href="/switchprivacy/{}">O</a> | <a style="font-size:70%" href="/notedelete/{}">X</a> ] <i>« {} »</i> - {}'.format(
                        private_note.uid, private_note.uid, private_note.note, private_note.poster
                        )
                    )

        # get all the PUBLIC notes ----------------------------------
        public_notes = [i for i in PjNote.objects.filter(
        note_target= obj_pk, is_public= True)]

        # initiate the list
        public_notes_formatted = []

        # for each public note, format the content in a string
        for public_note in public_notes:

            # if the note belongs to the current character, add the option to
            # switch the privacy of said note
            if public_note.poster_id == current_character.uid:
                public_notes_formatted.append(
                    '<p>[ <a style="font-size:70%" href="/switchprivacy/{}">Ø</a> | <a style="font-size:70%" href="/notedelete/{}">X</a> ] <i>« {} »</i> - {}'.format(
                        public_note.uid, public_note.uid, public_note.note, public_note.poster
                        )
                    )

            # if the note does not belong to current character, don't give
            # the privacy swith option
            else:
                public_notes_formatted.append(
                    '<i>« {} »</i> - {}'.format(
                        public_note.note, public_note.poster
                        )
                    )

    # if user is not authenticated
    else:
        # generic message leading to login page.
        private_notes_formatted = ['<a href ="/login">Connectez vous.</a>']

        # Load public notes
        public_notes_formatted = []
        public_notes = [i for i in PjNote.objects.filter(
            note_target= obj_pk, is_public= True)]
        for public_note in public_notes:
            public_notes_formatted.append(
                '<i>« {} »</i> - {}'.format(
                    public_note.note, public_note.poster
                    )
                )

    # Filling the context passed to the template
    context = {
        # Generic data
        'style': 'vsite/style.css',

        # Specific data
        'obj': obj,
        'private_notes': private_notes_formatted,
        'public_notes': public_notes_formatted,
        'form': PjNoteForm(),
        }
    template = loader.get_template('entity_view.html')

    if request.method == 'GET': 
        return HttpResponse(template.render(context , request ))

    if request.method == 'POST':
        form = PjNoteForm(request.POST)
        if form.is_valid():
            note_to_create = form.cleaned_data['note']
            poster_id = PjCharacter.objects.get(owner_id= request.user.id).uid
            note_target = obj_pk
            post = PjNote.objects.create(
                poster_id= poster_id , note_target= note_target , note= note_to_create)
        return HttpResponseRedirect(note_target)