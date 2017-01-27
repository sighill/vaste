from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.gis.db import models as gismodels

#####################################################################
class Image(models.Model):
    '''
        Images are a large part of this site. This table keeps track
        of every game image to make their use easy and flexible.
    '''
    uid= models.AutoField(
        primary_key = True , db_index = True)
    name= models.CharField(
        max_length = 255)
    internal_link= models.CharField(
        max_length = 500, default= '#')
    external_link= models.CharField(
        max_length = 500, blank=True, null=True)
    legend= models.CharField(
        max_length = 500, blank=True, null=True)
    legend_alt= models.CharField(
        max_length = 500, blank=True, null=True)
    complete_file= models.CharField(
        max_length = 500, default= '#', blank=True, null=True)
    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class ItemRecipes(models.Model):
    '''
        Item blueprints for reference along with the instances.
    '''

    # Attributes
    uid = models.AutoField(
        primary_key = True , db_index = True)
    identifier = models.PositiveIntegerField()
    level = models.PositiveIntegerField()
    item_type = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    img_name = models.ForeignKey(
        Image, related_name='img_name_ir', blank=True)
    ia_type= models.CharField(
        max_length = 255, null = True, blank = True)
    ia = models.CharField(
        max_length = 255, null = True, blank = True)
    iaq = models.PositiveIntegerField(
        default= 0, null = True, blank = True,)
    ib_type= models.CharField(
        max_length = 255, null = True, blank = True)
    ib = models.CharField(
        max_length = 255, null = True, blank = True)
    ibq = models.PositiveIntegerField(
        default= 0, null = True, blank = True,)
    ic_type= models.CharField(
        max_length = 255, null = True, blank = True)
    ic = models.CharField(
        max_length = 255, null = True, blank = True)
    icq = models.PositiveIntegerField(
        default= 0, null = True, blank = True)
    is_container= models.BooleanField(default= False)
    description = models.CharField(
        max_length = 2048, null = True, blank = True)

    # Methods
    def __str__(self):
        return str('{}: {} en {}'.format(self.item_type, self.name, self.ia_type))

#####################################################################
class HomeItems(models.Model):
    '''
        Generates home link items to the different parts of the
        website.
    '''

    # Attributes
    uid = models.AutoField(primary_key = True , db_index = True)
    name = models.CharField(max_length = 255, blank=True, null=True)
    img_name = models.ManyToManyField(
        Image, related_name='img_name_hi', blank=True)
    order_position = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length = 255, blank=True, null=True)

    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class Skills(models.Model):
    '''
        Reference model for all the jobs in the game.
    '''

    # Attributes
    uid = models.AutoField(primary_key = True , db_index = True)
    name = models.CharField(max_length = 255)
    is_unique= models.BooleanField(default= False)
    description = models.TextField(blank=True, null=True)
    more = models.CharField(max_length = 2500 , blank = True, null = True)

    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class Jobs(models.Model):
    '''
        Reference model for all the jobs in the game.
    '''

    # Attributes
    uid = models.AutoField(primary_key = True , db_index = True)
    name = models.CharField(max_length = 255)
    job_description = models.TextField(blank=True, null=True)
    more = models.CharField(max_length = 2500 , blank = True, null = True)
    related_skills= models.ManyToManyField(
        Skills , related_name='related_skills')

    # Methodes
    def __str__(self):
        return str(self.name)

#####################################################################
class GameEntity(models.Model):
    '''
        Abstract class to federate all entities into a single table,
        making easy any FK relation.
    '''

    # Attributes
    uid = models.BigAutoField(primary_key = True , db_index = True)
    name = models.CharField(max_length = 255, blank=True, null=True)
    is_visible = models.BooleanField(default= True)
    img_name = models.ManyToManyField(
        Image, related_name='img_name', blank=True)
    description = models.TextField(blank=True, null=True)
    more = models.CharField(max_length = 2500 , blank = True, null = True)

    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class PjCharacter(GameEntity):
    '''
        Permet de générer le contenu des vues du site de manière
        pratique
    '''
    
    # Attributes
    owner = models.ForeignKey(User , related_name='pj_owner')
    first_job = models.ForeignKey(Jobs, related_name='pj_fjob', blank=True, null=True)
    second_job = models.ForeignKey(Jobs, related_name='pj_sjob', blank=True, null=True)
    puissance = models.PositiveIntegerField()
    vigueur = models.PositiveIntegerField()
    dexterite = models.PositiveIntegerField()
    perception = models.PositiveIntegerField()
    charisme = models.PositiveIntegerField()
    astuce = models.PositiveIntegerField()
    volonte = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    essence = models.PositiveIntegerField()
    current_body= models.PositiveIntegerField()
    current_instinct= models.PositiveIntegerField()
    current_spirit= models.PositiveIntegerField()
    
    # Methods
    def __str__(self):
        return str(self.name)

    def max_body(self):
        return self.puissance+ self.vigueur+ self.dexterite

    def max_instinct(self):
        return self.perception + self.charisme + self.astuce

    def max_spirit(self):
        return self.volonte + self.intelligence + self.essence

#####################################################################
class Pnj(GameEntity):
    '''
        PNJ is french for NPC, non player characters. This is for 
        thinking creatures, not beasts. They are friends or foes.
    '''

    # Attributes
    location= models.ForeignKey(
        'Place' , related_name = 'pnj_location')
    first_job = models.ForeignKey(Jobs, related_name='pnj_fjob', blank=True, null=True)
    second_job = models.ForeignKey(Jobs, related_name='pnj_sjob', blank=True, null=True)
    puissance = models.PositiveIntegerField()
    vigueur = models.PositiveIntegerField()
    dexterite = models.PositiveIntegerField()
    perception = models.PositiveIntegerField()
    charisme = models.PositiveIntegerField()
    astuce = models.PositiveIntegerField()
    volonte = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    essence = models.PositiveIntegerField()
    current_body= models.PositiveIntegerField()
    current_instinct= models.PositiveIntegerField()
    current_spirit= models.PositiveIntegerField()
    
    # Methods
    def __str__(self):
        return str(self.name)

    def max_body(self):
        return self.puissance+ self.vigueur+ self.dexterite

    def max_instinct(self):
        return self.perception + self.charisme + self.astuce

    def max_spirit(self):
        return self.volonte + self.intelligence + self.essence
    
    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class Creature(GameEntity):
    '''
        Creatures are non thinking NPC (beasts, monsters)
        Some can be tamed as familiars.
    '''

    # Attributes
    puissance = models.PositiveIntegerField()
    vigueur = models.PositiveIntegerField()
    dexterite = models.PositiveIntegerField()
    perception = models.PositiveIntegerField()
    charisme = models.PositiveIntegerField()
    astuce = models.PositiveIntegerField()
    volonte = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    essence = models.PositiveIntegerField()
    
    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class PjNote(models.Model):
    '''
        Personal or public notes made on game entities.
    '''

    # Attributes
    uid = models.AutoField(primary_key=True, db_index= True)
    poster = models.ForeignKey(
        PjCharacter, related_name='char_id', blank=True, null=True)
    note_target = models.ForeignKey(
        GameEntity, related_name='entity_id')
    note = models.TextField(blank = True, null = True)
    created_date = models.DateTimeField(
            default=timezone.now)
    is_public = models.BooleanField(default= False)

    # Methods
    def __str__(self):
        return str(self.uid)

#####################################################################
class GameLog(models.Model):
    '''
        Displays chapters of each story lived by players.
    '''
    # TODO 

    # Variables pour les choix pré-remplis

    # Attributes
    uid = models.AutoField(primary_key = True, db_index = True)
    campaign = models.CharField(max_length = 255, blank=True, null=True)
    chapter_date = models.CharField(max_length = 255, blank=True, null=True)
    img_name = models.ForeignKey(
        Image, related_name='img_name_gl', blank=True, null=True)
    corpus = models.TextField(blank = True, null = True, db_index = True)
    order_position = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    # Methodes
    def __str__(self):
        return str(self.uid)

#####################################################################
class Item(models.Model):
    '''
        Item instances
    '''
    # TODO 

    # Variables pour les choix pré-remplis

    # Attributs
    uid = models.AutoField(primary_key = True , db_index = True)
    recipe = models.ForeignKey(
        ItemRecipes , related_name = 'recipe_uid', blank=True, null=True)
    name = models.CharField(max_length = 255)
    owner = models.ForeignKey(
        GameEntity , related_name = 'entity_uid', blank=True, null=True)
    is_visible = models.BooleanField(default= True)
    contained_by= models.ForeignKey(
        "self" , related_name = 'is_contained_by', blank=True, null=True)
    is_container= models.BooleanField(default= False)
    quantity = models.PositiveIntegerField(default= 1)
    ia_type = models.CharField(max_length = 100, null = True, blank = True)
    img_name = models.ForeignKey(
        Image, related_name='img_name_igi', blank=True)
    description = models.CharField(max_length = 2048, blank=True, null=True)
    created_date = models.DateTimeField(
            default=timezone.now) 

    # Methodes
    def __str__(self):
        return str(self.name)

#####################################################################
class Place(GameEntity):
    '''
        Data for the several places of Vaste. These are supposed to
        be located in a GIS sytem later, hence the GID
    '''

    # Variables pour field option choices
    place_category_choices = (
        ('Havre', 'Havre'),
        ('Ruine', 'Ruine'),
        ('Bunker','Bunker'),
        ('Cache', 'Cache'),
        ('Abri', 'Abri'),
    )
    
    # Attributes
    category = models.CharField(
        max_length = 255, 
        choices = place_category_choices)
    created_date = models.DateTimeField(
            default=timezone.now)
    modified_date = models.DateTimeField(
            auto_now=True)
    close_to= models.ManyToManyField(
        'self' , related_name = 'is_close_to', blank=True)

    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class Phenomenon(GameEntity):
    '''
        Data for the several places of Vaste. These are supposed to
        be located in a GIS sytem later, hence the GID
    '''

    # Attributes
    created_date = models.DateTimeField(
            default=timezone.now)
    modified_date = models.DateTimeField(
            auto_now=True)
    # geometry
    geom = gismodels.PolygonField(blank=True, null=True)

    # Methods
    def __str__(self):
        return str(self.name)

#####################################################################
class IgCreature(GameEntity):
    '''
        Active and living creatures in the world. The Creature model
        acts like a blueprint for these entities that are unique.
    '''

    # Attributes
    location= models.ForeignKey(
        Place , related_name = 'Place_uid')
    puissance = models.PositiveIntegerField()
    vigueur = models.PositiveIntegerField()
    dexterite = models.PositiveIntegerField()
    perception = models.PositiveIntegerField()
    charisme = models.PositiveIntegerField()
    astuce = models.PositiveIntegerField()
    volonte = models.PositiveIntegerField()
    intelligence = models.PositiveIntegerField()
    essence = models.PositiveIntegerField()
    current_body= models.PositiveIntegerField()
    current_instinct= models.PositiveIntegerField()
    current_spirit= models.PositiveIntegerField()
    
    # Methods
    def __str__(self):
        return str(self.name)

    def max_body(self):
        return self.puissance+ self.vigueur+ self.dexterite

    def max_instinct(self):
        return self.perception + self.charisme + self.astuce

    def max_spirit(self):
        return self.volonte + self.intelligence + self.essence

#####################################################################
class Changelog(models.Model):
    '''
        Logging changes to the app and blog posts.
    '''
    # attributes
    uid= models.AutoField(
        primary_key = True , db_index = True)
    title= models.CharField(
        max_length = 100, null = True, blank = True)
    corpus= models.CharField(
        max_length = 400)
    created_date = models.DateTimeField(
            default= timezone.now)
    reverted= models.BooleanField(default= False)
    is_announce= models.BooleanField(default= False)
    # Methods
    def __str__(self):
        return str(self.title)

#####################################################################
class TableLog(models.Model):
    '''
        Log of the actions of the game table for display on view
        gametable.
        Field source_entity is the entity who fired the event of 
        creating a new entry.
    '''
    # attributes
    uid= models.AutoField(
        primary_key = True , db_index = True)
    title= models.CharField(
        max_length = 100, null = True, blank = True)
    source_entity= models.ForeignKey(
        GameEntity, related_name='source_entity', blank=True, null=True )
    created_date = models.DateTimeField(
            default= timezone.now)
    # Methods
    def __str__(self):
        return str(self.title)
