#****************************************************************************
#   Unidad: urls.py
#   Descripción: Servicio de routing de la aplicación. 
#   
#   Autor: Jojann De Vargas
#   Fecha: 20-02-2020
# 
#   Historial de modificaciones
#   Fecha           usuario         descripción
#   20-02-2020      jdevargas       Creación.
# 
# *************************************************************************** 
from django.urls          import path
from django.views.generic import TemplateView
from .                    import views


app_name = 'endgame'
urlpatterns = [

    # Servicios principales
    # 1. Vista principal.
    path('', views.index, name='index'),
    
    # 2. Vista inicial del juego (donde se permite selecionar la opción o respuesta).
    path('<int:player_id>/game/', views.game, name='game'),
    
    # 3. Servicio que valida si ya se conectó otro jugador a la partida.
    path('<int:player_id>/<int:player_number>/wait/', views.wait, name='wait'),
    
    # 4. Servicio que guarda la respues de un jugador.
    path('<int:game_id>/<int:player_number>/<int:option_id>/answergame/', views.answergame, name='answergame'),
   
    # 5. Servicio que permite validar si el otro jugador ya respondió.
    path('<int:game_id>/<int:player_number>/gamestatus/', views.gamestatus, name='gamestatus'),
    
    # 6. Servicio para visualizar la pantalla de resultados de la partida.
    path('gameresults/', views.gameresults, name='gameresults'),

    # Servicios utilitarios
    # Servicio utilitario para obtener el código Javascript que permite ejecutar el servicio 3.
    path('<int:player_id>/game/work_game.js', (TemplateView.as_view(template_name="endgame/work_game.js", content_type='application/javascript', )), name='work_game.js'),
    
    # Servicio utilitario para obtener el código Javascript que permite ejecutar el servicio 5.
    path('<int:player_id>/game/work_gamestatus.js', (TemplateView.as_view(template_name="endgame/work_gamestatus.js", content_type='application/javascript', )), name='work_gamestatus.js'),
]