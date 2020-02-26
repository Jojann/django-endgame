from django.db import models
from django.utils import timezone

# Modelo que define el comportamiento del juego.
# Define los objetos (Piedra, papel, tijera etc.)
class Options(models.Model):
    description = models.CharField(verbose_name='Object name', max_length=200)
    state       = models.CharField(verbose_name='Option status',max_length=2, default='A') # Habilitada, deshabilitada.
    create_date = models.DateTimeField('Create date', default=timezone.now)

# Define que objeto 'mata' a otro objeto.
class HierarchyOpt(models.Model):
    father_id = models.ForeignKey(Options, unique= True, verbose_name='Dominant option',  related_name='REL_OPC1_HIERARCHI', on_delete=models.CASCADE)
    child_id  = models.ForeignKey(Options, unique= True, verbose_name='Recessive option', related_name='REL_OPC2_HIERARCHI', on_delete=models.CASCADE)

# Modelo para el jugador.
class Player(models.Model):
    player_name = models.CharField(verbose_name='Enter your nickname',max_length=200,unique=True)
    create_date = models.DateTimeField('date published', default=timezone.now)

# Modelo para el juego y el estado del mismo.
class Game(models.Model):
    player_id_one = models.ForeignKey(Player, null=True, verbose_name='Player one', related_name='REL_PLAYER1_GAME', on_delete=models.CASCADE)
    player_id_two = models.ForeignKey(Player, null=True, verbose_name='Player two', related_name='REL_PLAYER2_GAME', on_delete=models.CASCADE)
    
    player_one_opc = models.ForeignKey(Options, null=True, verbose_name='Player one option', related_name='REL_OPC1_GAME', on_delete=models.CASCADE)
    player_two_opc = models.ForeignKey(Options, null=True, verbose_name='Player two option', related_name='REL_OPC2_GAME', on_delete=models.CASCADE) 

    player_win     = models.ForeignKey(Player, null=True, verbose_name='Winning player', related_name='REL_PLAYER3_GAME', on_delete=models.CASCADE)

    create_date   = models.DateTimeField('Create date', default=timezone.now)
    estate        = models.CharField(verbose_name='Game status',max_length=2, default='E') # En Espera de jugador, Jugando, Terminado
    def is_ready(self):
        try:
            if self.player_id_one.id and self.player_id_two.id:
                return True                
        except:
            return False
    def is_finish(self):
        try:
            if self.player_one_opc.id and self.player_two_opc.id:
                return True                
        except:
            return False

