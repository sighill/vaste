from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .forms import PjNoteForm

#####################################################################
def Home(request):
    context = {
        'home_items': HomeItems.objects.filter().exclude(name='Accueil').order_by('order_position'),
    }
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

#####################################################################
def Account(request):
    if request.user.is_authenticated():
        # get PjCharacter of current user
        pj = PjCharacter.objects.get(owner_id= request.user.id)
        # get his skills
        unique_skill= Skills.objects.get(
            related_job__uid=pj.first_job.uid, is_unique= True
            )
        other_skills= Skills.objects.filter(
            related_job__in=[pj.first_job.uid, pj.second_job.uid], 
            is_unique= False
            )
        # get his notes
        pj_note_qs = PjNote.objects.filter(
            poster_id = pj).order_by('note_target')
        # get his stuff
        char_stuff_visible = [item for item in Item.objects.filter(
            owner= pj, is_visible= True)]
        char_stuff_not_visible = [item for item in Item.objects.filter(
            owner= pj, is_visible= False)]



        try:
            pj_note_content = []
            for entry in pj_note_qs:
                formatted_entry = '({}-{}-{}) à propos de {} : \n« {} »'.format(
                    entry.created_date.day, 
                    entry.created_date.month, 
                    entry.created_date.year, 
                    entry.note_target, 
                    entry.note)
                pj_note_content.append(formatted_entry)
            pj_note_content[0] # Retourne IndexError si vide
        except IndexError:
            pj_note_content = ['Pas de note personnelle enregistrée.']

        # Character preparation for display
        character= PjCharacter.objects.get(owner_id=request.user.id)
        char_stuff = [item for item in Item.objects.filter(
        owner_id= request.user.id, is_visible= True)]

        context = {
        'pj_note_content': pj_note_content,
        'character': character,
        'char_stuff_visible': char_stuff_visible,
        'char_stuff_not_visible': char_stuff_not_visible,
        'unique_skill': unique_skill,
        'other_skills': other_skills,
        }
        
        template = loader.get_template('account.html')
        return HttpResponse(template.render(context , request ))
    else:
        return HttpResponseRedirect('/login')

#####################################################################
def Log(request):

    context = {
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

    # Get his stuff and set title depending on the object
    stuff_title_dict= {
        Creature: 'Matériaux récupérables :',
        Place: 'Ressources possibles',
        Pnj: 'Possessions visibles',
        Phenomenon: 'Fuse extractible',
        PjCharacter: 'Possessions visibles',
    }
    obj_stuff = Item.objects.filter(
        owner_id= obj_pk, is_visible= True).order_by('name')
    if not obj_stuff:
        obj_stuff= ['Rien apparemment...']
    
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
        'obj': obj,
        'stuff_title': stuff_title_dict[obj_to_display],
        'obj_stuff': obj_stuff,
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
            note_target = GameEntity.objects.get(pk= int(obj_pk))
            post = PjNote.objects.create(
                poster_id= poster_id , note_target= note_target , note= note_to_create)
        return HttpResponseRedirect(note_target.uid)
