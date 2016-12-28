# temp script for transferring creatures to their own table.
# for now this script is meant to be copy pasted to the manage.py shell utility.

from vsite.models import Pnj, Creature
from random import randint


creatures_to_transfer = Pnj.objects.filter(is_creature = True)
new_creature = Creature()

for item in creatures_to_transfer:
    # Create new creature
    new_creature = Creature()
    # Fill in the attributes
    new_creature.uid = randint(1e16,1e17)
    new_creature.name = item.name
    new_creature.img_id = item.img_id
    new_creature.img_src = item.img_src
    new_creature.description = item.description
    new_creature.puissance = item.puissance
    new_creature.vigueur = item.vigueur
    new_creature.dexterite = item.dexterite
    new_creature.perception = item.perception
    new_creature.charisme = item.charisme
    new_creature.astuce = item.astuce
    new_creature.volonte = item.volonte
    new_creature.intelligence = item.intelligence
    new_creature.essence = item.essence
    new_creature.stuff = item.stuff
    new_creature.more = item.more
    # Save it
    new_creature.save()
