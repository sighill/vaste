from django.db import models

# Create your models here.
class pnj(models.Model):
    '''
        Les PNJ sont des personnages figurants dans la partie de jeu de rôles.

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
    img_id = models.CharField(max_length = 2500 , blank = True, null = True)
    name = models.CharField(max_length = 255)
    family = models.CharField(max_length = 255)
    age = models.PositiveIntegerField(default = 20)
    cast = models.PositiveIntegerField(choices = cast_choice) 
    attributes = models.CharField(default = '0,0,0,0,0,0,0,0,0', max_length = 100)
    skills  = models.CharField(blank = True , max_length = 1200)
    description = models.CharField(max_length = 2000 , blank = True, null = True)
    stuff = models.CharField(blank = True, max_length = 1200)
    more = models.CharField(max_length = 2500 , blank = True, null = True)
    
    # Methodes
    def __str__(self):
        return str(self.name)