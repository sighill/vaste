from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

#####################################################################
class pnj(models.Model):
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
    cast_choice = (
        ( 1 , 'Fongeux' ) ,
        ( 2 , 'Monteurs') ,
        ( 3 , 'Rapiats' ) ,
        ( 4 , 'Pisteurs') )

    # Attributs
    uid = models.AutoField(primary_key = True , db_index = True)
    visible = models.BooleanField()
    img_id = models.CharField(
        max_length = 2500 , blank = True, null = True)
    name = models.CharField(max_length = 255)
    family = models.CharField(max_length = 255)
    age = models.PositiveIntegerField(default = 20)
    cast = models.PositiveIntegerField(choices = cast_choice) 
    attributes = models.CharField(
        default = '0,0,0,0,0,0,0,0,0', max_length = 100)
    skills  = models.CharField(blank = True , max_length = 1200)
    description = models.TextField(
        max_length = 2000 , blank = True, null = True)
    stuff = models.CharField(blank = True, max_length = 1200)
    more = models.CharField(
        max_length = 2500 , blank = True, null = True)
    
    # Methodes
    def __str__(self):
        return str(self.name)

        
#####################################################################
class pj_note(models.Model):
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
    poster_id = models.ForeignKey(
        User , related_name='user_id', blank=True,null=True)
    pnj_id = models.ForeignKey(
        pnj , related_name='pnj_id', blank=True,null=True)
    note = models.TextField(blank = True, null = True)
    created_date = models.DateTimeField(
            default=timezone.now)

    # Methodes
    def __str__(self):
        return str(self.uid)