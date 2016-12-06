from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


#####################################################################
class ItemRecipes(models.Model):
    '''
        Item blueprints for reference along with the instances.
    '''
    # TODO 

    # Variables pour les choix pré-remplis

    # Attributs
    uid = models.AutoField(primary_key = True , db_index = True)
    item_type = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    ia = models.ForeignKey('self', null = True, blank = True, related_name = 'self_ing_a')
    iaq = models.PositiveIntegerField(null = True, blank = True)
    ib = models.ForeignKey('self', null = True, blank = True, related_name = 'self_ing_b')
    ibq = models.PositiveIntegerField(null = True, blank = True)
    ic = models.ForeignKey('self', null = True, blank = True, related_name = 'self_ing_c')
    icq = models.PositiveIntegerField(null = True, blank = True)
    wood = models.NullBooleanField(blank = True, default = False)
    plastic = models.NullBooleanField(blank = True, default = False)
    metal = models.NullBooleanField(blank = True, default = False)
    rock = models.NullBooleanField(blank = True, default = False)
    fiber = models.NullBooleanField(blank = True, default = False)
    leather = models.NullBooleanField(blank = True, default = False)
    rarity = models.PositiveIntegerField(null = True, blank = True)
    description = models.CharField(max_length = 2048, null = True, blank = True,)

    # Methodes
    def __str__(self):
        return str(self.name)



#####################################################################
class HomeItems(models.Model):
    '''
        Generates navbar items.
    '''
    # TODO 

    # Variables pour les choix pré-remplis

    # Attributs
    uid = models.AutoField(primary_key = True , db_index = True)
    name = models.CharField(max_length = 255, blank=True, null=True)
    img_id = models.CharField(max_length = 255, blank=True, null=True)
    order_position = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.CharField(max_length = 255, blank=True, null=True)

    # Methodes
    def __str__(self):
        return str(self.name)

#####################################################################
class Jobs(models.Model):
    '''
        Reference model for all the jobs in the game.
    '''
    # TODO 

    # Variables pour les choix pré-remplis
    job_type_choices = (
        ('Métier principal', 'Métier principal'),
        ('Métier secondaire', 'Métier secondaire'))
    # Attributes
    uid = models.AutoField(primary_key = True , db_index = True)
    name = models.CharField(max_length = 255)
    job_type = models.CharField(max_length = 255, choices= job_type_choices)
    job_description = models.TextField(blank=True, null=True)
    more = models.CharField(max_length = 2500 , blank = True, null = True)

    # Methodes
    def __str__(self):
        return str(self.name)

#####################################################################
class Skills(models.Model):
    '''
        Reference model for all the jobs in the game.
    '''
    # TODO 

    # Variables pour les choix pré-remplis
 
    # Attributes
    uid = models.AutoField(primary_key = True , db_index = True)
    name = models.CharField(max_length = 255)
    related_job = models.ForeignKey(Jobs , related_name='related_job', blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    more = models.CharField(max_length = 2500 , blank = True, null = True)

    # Methodes
    def __str__(self):
        return str(self.name)


#####################################################################
class PjCharacter(models.Model):
    '''
        Permet de générer le contenu des vues du site de manière
        pratique
    '''
    # TODO 

    # Variables pour les choix pré-remplis

    # Attributs
    uid = models.AutoField(primary_key = True , db_index = True)
    owner = models.ForeignKey(User , related_name='pj_owner')
    name = models.CharField(max_length = 255, blank=True, null=True)
    img_id = models.CharField(max_length = 255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
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
    stuff = models.CharField(blank = True, max_length = 1200)
    more = models.CharField(max_length = 2500 , blank = True, null = True)
    
    # Methodes
    def __str__(self):
        return str(self.name)

#####################################################################
class Pnj(models.Model):
    '''
        Les PNJ sont des personnages figurants dans la 
        partie de jeu de rôles.

        Les attributes sont des intégrales séparées de virgules
            Il y en a toujours 9
        Les compétences sont des couples de valeur (nom:valeur)
            Séparés par une virgule
        Les stuff sont des strings séparés par une virgule
    '''
    # TODO 

    # Variables pour les choix pré-remplis

    # Attributs
    uid = models.AutoField(primary_key = True , db_index = True)
    owner = models.ForeignKey(User , related_name='pnj_owner', blank=True, null=True)
    is_creature = models.BooleanField(default= False)
    is_visible = models.BooleanField(default= False)
    name = models.CharField(max_length = 255, blank=True, null=True)
    img_id = models.CharField(max_length = 255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
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
    stuff = models.CharField(blank = True, max_length = 1200)
    more = models.CharField(max_length = 2500 , blank = True, null = True)
    
    # Methodes
    def __str__(self):
        return str(self.name)

#####################################################################
class PjNote(models.Model):
    '''
        Les utilisateurs du site peuvent poster des notes de jeu 
        sur un PNJ. Ils peuvent consulter cette note de jeu sur 
        le profil du pnj et aussisur un tableau de bord sur une vue 
        à part.
    '''
    # TODO 

    # Variables pour les choix pré-remplis

    # Attributs
    uid = models.AutoField(primary_key=True, db_index= True)
    poster = models.ForeignKey(
        PjCharacter, related_name='char_id', blank=True, null=True)
    pnj = models.ForeignKey(
        Pnj , related_name='pnj_id', blank=True, null=True)
    note = models.TextField(blank = True, null = True)
    created_date = models.DateTimeField(
            default=timezone.now)
    is_public = models.BooleanField(default= False)

    # Methodes
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
    img_id = models.CharField(max_length = 255, blank=True, null=True)
    img_legend = models.CharField(max_length = 255, blank=True, null=True)
    img_link = models.CharField(max_length = 255, blank=True, null=True)
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
    owner = models.ForeignKey(PjCharacter , related_name = 'pj_id', blank=True, null=True)
    ia_type = models.CharField(max_length = 100, null = True, blank = True)
    ib_type = models.CharField(max_length = 100, null = True, blank = True)
    ic_type = models.CharField(max_length = 100, null = True, blank = True)
    description = models.CharField(max_length = 2048)
    created_date = models.DateTimeField(
            default=timezone.now) 

    # Methodes
    def __str__(self):
        return str(self.name)