# python 3.5

from vsite.models import Item, PjCharacter
from django.core.exceptions import ObjectDoesNotExist


#####################################################################
def CopyItem(obj_pk, new_owner_pk):
    '''
        Allows admin to copy an item and give it 
        to another character. Works same as "save as new...
    '''
    # Get the object
    obj = Item.objects.get(pk= obj_pk)
    # Be sure that the character recipient exists
    new_owner = PjCharacter.objects.get(pk= new_owner_pk)
    # Change the owner id
    obj.owner = new_owner
    obj.pk = None
    # Save the copy with the new owner_id
    obj.save()
    # return var is declared
    copy_status = '{} successfully copied to {}.'.format(obj.name, obj.owner.name)
    return copy_status

