# python3 
'''
one shot script to transfer every data related to images
scattered in several models into a single table, Image.
attrs for quick reference :
name
internal_link
external_link
legend
legend_alt
complete_file
models done : Pnj
'''

from vsite.models import *

for ent in Creature.objects.all():
    img_to_create= Image()
    img_to_create.name= ent.img_id
    img_to_create.internal_link= '/creatures/view/{}'.format(ent.uid)
    img_to_create.external_link= ent.img_src
    img_to_create.save()