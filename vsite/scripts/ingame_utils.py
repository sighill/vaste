#python3
'''
Scripts meant to be used after being imported in manage.py's shell.
Quick import command :
from vsite.scripts.ingame_utils import *

'''
from vsite.models import *
from django.core.exceptions import *
import pprint
from copy import deepcopy

#####################################################################
def NewItem():
    '''
        Creates a new item for a game entity. Everything is entered
        manually.
    '''
    try:
        # Initiate new item and populate attributes
        item_to_create= Item()
        item_recipe= ItemRecipes.objects.get(pk= input('Recipe: '))
        item_to_create.recipe= item_recipe
        item_to_create.name= str(
            input('Nom de l\'item (defaut: {}): '.format(
                item_recipe.__str__())) or item_recipe.__str__()
            )
        item_to_create.owner= GameEntity.objects.get(
            name= input('Destinataire: ')
            )
        item_to_create.ia_type= item_recipe.ia_type
        item_to_create.ib_type= item_recipe.ib_type
        item_to_create.ic_type= item_recipe.ic_type
        item_to_create.quantity= input('Quantity: ')
        item_to_create.description= str(
            input('Description: (defaut: {}): '.format(
                item_recipe.description)) or item_recipe.description
            )

        item_is_visible= input('Visible (y/n): ')
        if item_is_visible == 'y':
            item_to_create.is_visible= True
        else:
            item_to_create.is_visible= False
    # Catch exceptions
    except (ValueError, TypeError, ObjectDoesNotExist,
        PermissionDenied, FieldError, ValidationError) as e:
        raise e
        func_state = 'fail'
    # Ask for validation and commit if Y or y
    validation= input('Valider ? y/n : ')
    if validation in ['Y','y']:
        item_to_create.save()
        func_state= 'Item créé.'
    else:
        func_state= 'Création abandonnée.'
        pass
    # End function
    return func_state

#####################################################################
def DelItem(owner_name):
    '''
        Deletes an entity's item manually.
    '''
    try:
        # get the list of items owned by the entity
        items_to_delete= Item.objects.filter(
            owner_id= GameEntity.objects.get(
                name= owner_name))
        # print them in a tidy list
        for item in items_to_delete:
            print('{} - {}'.format(item.uid, item.name))
        # ask for which item to delete
        item_to_del= Item.objects.get(pk= 
            input('uid de l\'objet à détruire: '))
        # ask for validation
        print('objet: {}'.format(item_to_del.name))
        validation= input('Valider ? y/n : ')
        if validation in ['Y','y']:
            item_to_del.delete()
            func_state= 'Item détruit.'
        else:
            func_state= 'Destruction abandonnée.'
            pass
    # raise exceptions
    except (ValueError, TypeError, ObjectDoesNotExist,
        PermissionDenied, FieldError, ValidationError) as e:
        raise e
        func_state = 'fail'
    # end function
    return func_state

#####################################################################
def CopyItem():
    '''
        Copies an entity's item manually.
    '''
    item_list= ['{}\t| {}\t\t|\t{}'.format(i.uid, i.owner, i.name) for i in Item.objects.all()]
    for i in item_list:
        print(i)
    try:
        # ask for which item to copy
        item_to_copy= Item.objects.get(pk= 
            input('uid de l\'objet à copier: '))
        give_item_to= input('Nouveau possesseur: ')
        # ask for validation
        validation= input('Valider ? y/n : ')
        if validation in ['Y','y']:
            item_copied= item_to_copy
            item_copied.uid= None
            item_copied.owner= GameEntity.objects.get(name= give_item_to)
            item_copied.save()
            func_state= 'Item copié.'
        else:
            func_state= 'Abandon.'
            pass
    # raise exceptions
    except (ValueError, TypeError, ObjectDoesNotExist,
        PermissionDenied, FieldError, ValidationError) as e:
        raise e
        func_state = 'fail'
    # end function
    return func_state

#####################################################################
def Loot():
    '''
        Allows to loot an entity by the PC. For a given entity, you
        can manually change the owner. Items can be kept at their 
        initial place.
    '''
    try:
        # ask for the entity to loot (creature, npc, place)
        entity_to_loot= GameEntity.objects.get(
            name= input('Entité à looter: ')
            )
        # get its stuff and display it
        items_avail= Item.objects.filter(owner_id= entity_to_loot)
        for item in items_avail:
            print('{} - {}'.format(item.uid, item.name))
        # for each item ask who is the recipient
        for item in items_avail:
            item_recipient = input(
                'Destinataire de {}: '.format(item.name)
                )
            item.owner_id= GameEntity.objects.get(
                name= item_recipient)
            # ask for validation
            validation= input('Valider ? y/n : ')
            if validation in ['Y','y']:
                item.save()
                print('Item donné.')
            else:
                print('Item laissé.')
                pass
    # raise exceptions
    except (ValueError, TypeError, ObjectDoesNotExist,
        PermissionDenied, FieldError, ValidationError) as e:
        raise e
        func_state = 'fail'
    # end function
    return 'loot fini.'

#####################################################################
def NewCrea():
    '''
        Create a new IgCreature based on a Creature. It inherits its
        attributes, but does NOT do it dynamically. 
        It appears less pythonic and dirty, but has in game
        justifications such as attribute buffs/debuffs.
    '''
    try:
        # list avail entities
        creatures_avail= Creature.objects.all()
        for creature in creatures_avail:
            print(creature.name)
        # ask for which creature to copy
        creature_to_copy= Creature.objects.get(
            name=input('Nom du modele de creature a copier: '))
        # copy the instance into a new object
        # dirtyyyyyyy
        new_creature= IgCreature()
        new_creature.name= input('Nom unique: ')
        new_creature.is_visible= True
        new_creature.location= Place.objects.get(
            name= input('Endroit où elle est: '))
        new_creature.img_id= creature_to_copy.img_id
        new_creature.img_src= creature_to_copy.img_src
        new_creature.description= creature_to_copy.description
        new_creature.more= input('Courte description: ')
        new_creature.puissance= creature_to_copy.puissance
        new_creature.vigueur= creature_to_copy.vigueur
        new_creature.dexterite= creature_to_copy.dexterite
        new_creature.perception= creature_to_copy.perception
        new_creature.charisme= creature_to_copy.charisme
        new_creature.astuce= creature_to_copy.astuce
        new_creature.volonte= creature_to_copy.volonte
        new_creature.intelligence= creature_to_copy.intelligence
        new_creature.essence= creature_to_copy.essence
        # ask for validation
        validation= input('Valider ? y/n : ')
        if validation in ['Y','y']:
            new_creature.save()
            # now that the uid has been generated, get it back
            saved_creature= IgCreature.objects.get(
                name=new_creature.name)
            # automatically create its items
            copied_creature_items = Item.objects.filter(
                owner_id= creature_to_copy.uid)
            # copy each item and give it to the new creature
            for item in copied_creature_items:
                new_item= copy.copy(item)
                new_item.owner_id= saved_creature.uid
                new_item.save()
            func_state= 'Créature unique et ses items créee.'
        else:
            func_state= 'Annulé.'
            pass
    # raise exceptions
    except (ValueError, TypeError, ObjectDoesNotExist,
        PermissionDenied, FieldError, ValidationError) as e:
        raise e
        func_state = 'fail'
    # end function
    return func_state

#####################################################################
def KillCrea():
    '''
        Kills a creature (changes its name to carcass of xxx)
    '''
    try:
        ig_creatures= IgCreature.objects.all()
        for creature in ig_creatures:
            print(creature.name)
        # ask for which creature to copy
        creature_to_kill= IgCreature.objects.get(
            name=input('Qui tuer: '))
        creature_to_kill.name= 'Carcasse de {}'.format(
            creature_to_kill.name)
        creature_to_kill.save()
        func_state= 'Créature tuée, prête à être lootée.'
    # raise exceptions
    except (ValueError, TypeError, ObjectDoesNotExist,
        PermissionDenied, FieldError, ValidationError) as e:
        raise e
        func_state = 'fail'
    return func_state

#####################################################################
def ShowEnt():
    '''
        Quick summary of an entity.
    '''
    entity_list= ['{} - {}'.format(i.uid, i.name) for i in GameEntity.objects.all()]
    for i in entity_list:
        print(i)
    ent_to_display= GameEntity.objects.get(uid= input('uid de l\'entité à afficher: '))
    print(ent_to_display)

    func_state = 'Done'
    # end function
    return func_state

#####################################################################
def Showgrp(entity_type):
    '''
        Show a type of game entities
    '''
    try:
        entity_list= ['{}\t| {}\t| {}\t| {}'.format(i.uid, i.owner, i.name, i.more[:30]+'...') for i in entity_type.objects.all()]
        for i in entity_list:
            print(i)
    except AttributeError:
        entity_list= ['{}\t| {}'.format(i.uid, i.name) for i in entity_type.objects.all()]
        for i in entity_list:
            print(i)

    func_state = 'Done'
    # end function
    return func_state

#####################################################################
def ItemBreakdown(item_uid):
    '''
        Allows a player to break down an item into its elementary
        pieces specified in its recipe.
    '''
    # import item to breakdown
    item_to_bd = Item.objects.get(pk= item_uid)
    # get its recipe for quick access
    item_recipe= item_to_bd.recipe
    # get the ingredients recipes for full new item building
    ing_recipes= [i for i in ItemRecipes.objects.filter(
        pk__in= [item_recipe.ia, item_recipe.ib, item_recipe.ic]
        )]

    # for each ingredient of the item to breakdown, create an item in
    # correct quantity
    for ingredient in ing_recipes:
        # if a similar ingredient is owned, just add quantity
        # if not, create a new item from the ingredient
        try:
            ingredient_existing= Item.objects.get(
                owner=item_to_bd.owner, recipe=ingredient)
            ingredient_existing.quantity += item_recipe.iaq
            ingredient_existing.save()
            func_state= 'Success'
        except ObjectDoesNotExist:
            try:
                # try and create the ia item
                item_resulting_dict= {}
                item_resulting_dict['recipe']= ingredient
                item_resulting_dict['name']= ingredient.__str__()
                item_resulting_dict['owner']= item_to_bd.owner
                item_resulting_dict['is_visible']= True
                item_resulting_dict['quantity']= item_recipe.iaq
                item_resulting_dict['ia_type']= item_recipe.ia_type
                item_resulting_dict['description']= item_recipe.description
                new_item= Item(**item_resulting_dict)
                new_item.save()
                func_state= 'Success'
            # raise exceptions
            except (ValueError, TypeError, ObjectDoesNotExist,
                PermissionDenied, FieldError, ValidationError) as e:
                raise e
                func_state = 'fail'
    # lower original item's quantity by one or delete it
    if item_to_bd.quantity == 1:
        item_to_bd.delete()
    else:
        item_to_bd.quantity-= 1
        item_to_bd.save()
    # end function
    return func_state

'''
from vsite.scripts.ingame_utils import *

'''