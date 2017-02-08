from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .forms import PjNoteForm, ScribeEntry
from .scripts.ingame_utils import *
from copy import deepcopy
from random import randint

current_gamelog_uid= 19

#####################################################################
def Home(request):
    '''
        Defines the necessary elements to display on the front page.
    '''

    home_items= HomeItems.objects.select_related().filter().exclude(name='Accueil').order_by('order_position')
    # get the first three changelog entries that are announces
    announces= Changelog.objects.filter(is_announce= True).order_by('-created_date')[:3]
    context = {
        'home_items': home_items,
        'announces': announces,
        'glob_var': GameGlobal.objects.get(pk=2),
    } 
    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))

#####################################################################
def Account(request):
    if request.user.is_authenticated():
        # get PjCharacter of current user
        pj = PjCharacter.objects.select_related().get(owner_id= request.user.id)
        # get his skills
        unique_skill= pj.first_job.related_skills.get(is_unique=True)
        # get the skills and combine them in a list excuding duplicates
        f_skills= [i for i in pj.first_job.related_skills.filter(is_unique=False)]
        s_skills= [i for i in pj.second_job.related_skills.filter(is_unique=False)]
        other_skills= list(set(f_skills + s_skills))
        craft_skill= int((pj.dexterite + pj.astuce)/2)
        # get his stuff
        char_stuff = [item for item in Item.objects.filter(
            owner= pj).order_by('name')]
        # get his containers
        containers= [i for i in char_stuff if i.is_container]
        # get his notes
        pj_note_qs = PjNote.objects.filter(
            poster_id = pj).order_by('note_target')
        # make them pretty
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

        context = {
        'pj_note_content': pj_note_content,
        'character': pj,
        'char_stuff': char_stuff,
        'unique_skill': unique_skill,
        'other_skills': other_skills,
        'possible_craft': PossibleCrafts(pj.uid,craft_skill),
        'containers': containers,
        'craft_skill': craft_skill,
        'body_meter_percent': int((pj.current_body / pj.max_body())*100),
        'instinct_meter_percent': int((pj.current_instinct / pj.max_instinct())*100),
        'spirit_meter_percent': int((pj.current_spirit / pj.max_spirit())*100),
        }
        
        template = loader.get_template('account.html')
        return HttpResponse(template.render(context , request ))
    else:
        return HttpResponseRedirect('/login')

#####################################################################
def Log(request):

    context = {
        'navbar_items': HomeItems.objects.all().order_by('order_position'),
        'log': GameLog.objects.all().select_related().order_by('order_position'),
    }
    template = loader.get_template('game_log.html')
    return HttpResponse(template.render(context, request))

#####################################################################
def NotePrivacySwitch(request, note_uid):
    '''
        This view is a simple function called to make a private
        note on a NPC public. 
    '''

    # Retrieve note object
    note_to_switch = PjNote.objects.get(pk= note_uid)

    # switch the wanted one :
    if note_to_switch.is_public == True:
        note_to_switch.is_public = False
        note_to_switch.save()
    else:
        note_to_switch.is_public = True
        note_to_switch.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#####################################################################
def EntityPrivacySwitch(request, entity_uid):
    '''
        This view is a simple function called to make a hide/reveal
        an item in a character inventory.
    '''

    # Retrieve item object
    entity_to_switch = GameEntity.objects.get(pk= entity_uid)

    # Now switch the wanted one :
    if entity_to_switch.is_visible == True:
        entity_to_switch.is_visible = False
        entity_to_switch.save()
    else:
        entity_to_switch.is_visible = True
        entity_to_switch.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#####################################################################
def ItemSwitchPrivacy(request, item_uid):
    '''
        This view is a simple function called to make a hide/reveal
        an item in a character inventory.
    '''

    # Retrieve item object
    item_to_switch = Item.objects.get(pk= item_uid)

    # Now switch the wanted one :
    if item_to_switch.is_visible == True:
        item_to_switch.is_visible = False
        item_to_switch.save()
    else:
        item_to_switch.is_visible = True
        item_to_switch.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#####################################################################
def ItemContainerChange(request, item_uid, container_uid):
    '''
        This view allows a player to change the value of contained_by
        of his in game items.
    '''
    # retrieve item object
    entity_to_change = Item.objects.get(pk= item_uid)
    # retrieve the container or give value None if the object is put
    # on the belt (no container)
    if container_uid== "0":
        entity_to_change.contained_by= None
        entity_to_change.is_visible= True
        entity_to_change.save()
    else:
        container= Item.objects.get(pk= container_uid)
        entity_to_change.contained_by= container
        entity_to_change.is_visible= False
        entity_to_change.save()

    return HttpResponseRedirect('/account#Possessions')

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
    '''
        provides a clear index of the specified game entity.
    '''
    # Some tables have  a 'is_visible' value that we have to filter
    # out before filling the content. 
    if request.user.id== 1 :
        content = obj_to_display.objects.select_related().all()
        is_admin= True
    else: 
        content = obj_to_display.objects.select_related().filter(is_visible= True)
        is_admin= False

    # Choose the page title depending on which type of GameEntity is displayed
    index_title_dict= {
        Creature: 'Créatures',
        Place: 'Lieux du Vaste',
        Pnj: 'Personnages non joueurs',
        Phenomenon: 'Phénomènes du Vaste',
        PjCharacter: 'Personnages joueurs',
    }

    context = {
        'content': content,
        'is_admin': is_admin,
        'request user': request.user.id,
        'index_title': index_title_dict[obj_to_display],
    }
    template = loader.get_template('entity_index.html')
    return HttpResponse(template.render(context, request))

#####################################################################
def EntityView(request, obj_to_display, obj_pk):
    '''
        DEV PHASE
        Entity view is the single entity viewer usable for every
        entity in the game, be it NPC, creature, place or phenomenon.
    '''

    # Get the object instance the user wants to display
    obj = obj_to_display.objects.select_related().get(pk= obj_pk)
    img= [i for i in obj.img_name.all()]

    # Get his stuff and set title depending on the object
    stuff_title_dict= {
        Creature: 'Matériaux récupérables :',
        Place: 'Ressources possibles',
        Pnj: 'Possessions visibles',
        Phenomenon: 'Fuse extractible',
        PjCharacter: 'Possessions visibles',
    }
    if request.user.id== 1 :
        obj_stuff = Item.objects.filter(
            owner_id= obj_pk)
        is_admin= True
    else: 
        obj_stuff = Item.objects.filter(
            owner_id= obj_pk, contained_by= None).order_by('name')
        is_admin= False

    
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
                    '[ <a style="font-size:70%" href="/switchprivacy/{}">O</a> | <a style="font-size:70%" href="/notedelete/{}">X</a> ] <i>« {} »</i> - {}'.format(
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
                    '[ <a style="font-size:70%" href="/switchprivacy/{}">Ø</a> | <a style="font-size:70%" href="/notedelete/{}">X</a> ] <i>« {} »</i> - {}'.format(
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
        'img': img,
        'stuff_title': stuff_title_dict[obj_to_display],
        'obj_stuff': obj_stuff,
        'private_notes': private_notes_formatted,
        'public_notes': public_notes_formatted,
        'form': PjNoteForm(),
        'is_admin': is_admin,
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

#####################################################################
def ItemBreakdownByUser(request, item_uid):
    '''
        This view is meant to call the external function ItemBreakdown
        by an user wanting to breakdown on of his item, through
        a button in his inventory, page account.
    '''

    ItemBreakdown(item_uid)

    return HttpResponseRedirect('/account#Possessions')

#####################################################################
def ItemCraftByUser(request, recipe_identifier):
    '''
        This view is meant to call the external function CraftItem
        by an user wanting to craft an item, through
        a button in his inventory, page account.
    '''
    char_obj= PjCharacter.objects.get(owner_id= request.user.id)
    CraftItem(char_obj, recipe_identifier)

    return HttpResponseRedirect('/account#Possessions')

#####################################################################
def ChangelogView(request):
    content= Changelog.objects.all().order_by('created_date').reverse()
    context = {
        'content': content,
    } 
    template = loader.get_template('changelog.html')
    return HttpResponse(template.render(context, request))

#####################################################################
def GiveItemTo(request, item_uid, recipient_uid):
    '''
        Dirty way to give an item to a player. Will do better next time.
    '''
    # get the obj to give
    item_to_give= Item.objects.select_related().get(pk=item_uid)
    # get the recipient pj
    recipient_pj= PjCharacter.objects.select_related().get(pk= recipient_uid)
    # get the recipient inventory
    try:
        similar_item_in_recipient_inv= Item.objects.filter(owner= recipient_pj).filter(recipe= item_to_give.recipe)[0]
    except IndexError:
        similar_item_in_recipient_inv= False
    #
    if similar_item_in_recipient_inv:
        similar_item_in_recipient_inv.quantity = similar_item_in_recipient_inv.quantity + 1
        similar_item_in_recipient_inv.save()
    elif similar_item_in_recipient_inv is False:
        new_item= deepcopy(item_to_give)
        new_item.uid= None
        new_item.owner= recipient_pj
        new_item.quantity= 1
        new_item.save()

    item_to_give.quantity = item_to_give.quantity -1
    if item_to_give.quantity <= 0:
        item_to_give.delete()
    else:
        item_to_give.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#####################################################################
def GameTable(request):
    '''
        Main page for the game. Every current event, NPC and PC are
        on the same window for quick display. Every item links to more
        detailed views.
    '''

    if request.method== 'GET':
        # get game globals
        game_global= GameGlobal.objects.get(pk= 2)
        # then
        if request.user.is_authenticated():
            pj_active= PjCharacter.objects.get(owner_id= request.user.id)
            # unlock admin options
            if request.user.id== 1:
                is_scribe= False
                is_admin= True
            elif request.user.id== 2:
                is_scribe= True
                is_admin= False
            else:
                is_scribe= False
                is_admin= False
            # To pass all objects in a clean way with additional information
            # for the template, we give properties to each object.
            all_pj= PjCharacter.objects.select_related().filter(is_visible=True).order_by('uid')
            for pj in all_pj:
                pj.body_meter_percent= int((pj.current_body / pj.max_body())*100)
                pj.instinct_meter_percent= int((pj.current_instinct / pj.max_instinct())*100)
                pj.spirit_meter_percent= int((pj.current_spirit / pj.max_spirit())*100)
                pj.visible_items= [i for i in Item.objects.filter(owner=pj, is_visible= True)]
            # Idem for all creatures present
            creatures_present= IgCreature.objects.filter(location=game_global.current_place)
            for c in creatures_present:
                c.body_meter_percent= int((c.current_body / c.max_body())*100)
                c.instinct_meter_percent= int((c.current_instinct / c.max_instinct())*100)
                c.spirit_meter_percent= int((c.current_spirit / c.max_spirit())*100)
                c.visible_items= [i for i in Item.objects.filter(owner=c, is_visible= True)]

            # Idem for all NPC present
            npc_present= Pnj.objects.filter(location=game_global.current_place, is_visible=True)
            for n in npc_present:
                n.body_meter_percent= int((n.current_body / n.max_body())*100)
                n.instinct_meter_percent= int((n.current_instinct / n.max_instinct())*100)
                n.spirit_meter_percent= int((n.current_spirit / n.max_spirit())*100)
                n.visible_items= [i for i in Item.objects.filter(owner=n, is_visible= True)]

            context = {
                'all_pj': all_pj,
                'current_place': game_global.current_place,
                'creatures_present': creatures_present,
                'npc_present': npc_present,
                'pj_active': pj_active.pk,
                'table_log': TableLog.objects.all().order_by('created_date').reverse()[:10],
                'is_admin': is_admin,
                'is_scribe': is_scribe,
                'form': ScribeEntry(),
            } 
            template = loader.get_template('game_table.html')
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('/login')
    # if request.method== 'POST'
    else: 
        game_global= GameGlobal.objects.get(pk= 2)
        form = ScribeEntry(request.POST)
        if form.is_valid():
            log_receiving_entry= game_global.current_gamelog
            log_receiving_entry.corpus+= ' {}'.format(form.cleaned_data['entry'])
            log_receiving_entry.save()
        return HttpResponseRedirect('/gametable')

#####################################################################
def RollDice(request, entity_rolling_pk):
    '''
        Roll a D100 on the gametable.
    '''
    # entity rolling the die
    entity_rolling= GameEntity.objects.get(pk= entity_rolling_pk)
    # Get the dice result
    result= randint(0,100)
    if result > 90:
        roll_log= 'a fait un résultat de <b>{}</b> sur 1D100 - ECHEC CRITIQUE !'.format(result)
    elif result < 10:
        roll_log= 'a fait un résultat de <b>{}</b> sur 1D100 - REUSSITE CRITIQUE !'.format(result)
    else:
        roll_log= 'a fait un résultat de <b>{}</b> sur 1D100.'.format(result)
    # Create a new log line with the new entry
    log= TableLog()
    log.title= roll_log
    log.source_entity= entity_rolling
    log.save()

    return HttpResponseRedirect('/gametable')