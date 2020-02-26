#****************************************************************************
#   Unidad: views.py
#   Descripción: Servicios de proceso y lógica de la aplicación. 
#   
#   Autor: Jojann De Vargas
#   Fecha: 20-02-2020
# 
#   Historial de modificaciones
#   Fecha           usuario         descripción
#   20-02-2020      jdevargas       Creación.
# 
# *************************************************************************** 
from django.shortcuts import render
from django.http      import JsonResponse, HttpResponse
from .forms           import PlayerForm
from django.shortcuts import redirect
from django.utils     import timezone
from .models          import Player, Game, Options, HierarchyOpt

#****************************************************************************
#   Procedimiento: index
#   Descripción: Servicio que despliega la pantalla inicial de la aplicación. 
#                En esta pantalla el usuario ingresa su nickname para poder 
#                ir a la pantalla de juego. Si el nickname ya existe, pregunta 
#                si desea continuar.
#                Cuando el nombre de usuario supera las validaciones se redirecciona 
#                a la vista 'game'.
#   
#   Autor: Jojann De Vargas
#   Fecha: 20-02-2020
#   
#   Parámetros: POST: player_name - Nombre del jugador
#   Retorno: error       - Mensaje de error cuando el usuario ya existe.
#            player_name - nickname del jugador.
#            player.id     - identificador del jugador.
#
# 
#   Historial de modificaciones
#   Fecha           usuario         descripción
#   20-02-2020      jdevargas       Creación.
# 
# *************************************************************************** 
def index(request):
    
    # Si el método es post es por que desea ser redirigido a la pantalla de juego.
    if request.method == "POST":
        form = PlayerForm(request.POST)
        # Crea el usuario si no existe y lo redirecciona.
        if form.is_valid():
            player = form.save(commit=False)
            player.create_date = timezone.now()
            player.save()
            return redirect(str(player.id)+'/game')
        else: # Si existe pregunta si desea continuar.
            player_name=request.POST['player_name']
            player =  Player.objects.get(player_name=player_name)
            form = PlayerForm()    
            return render(request, 'endgame/index.html', {'form': form,'error': 'Nickname ['+player_name+'] already exist. Try again!','player_id': player.id, 'player_name': player_name })
    else: # Si el método no es POST entonces solo ingreso a la pantalla inicial.
        form = PlayerForm()
        return render(request, 'endgame/index.html', {'form': form})

#****************************************************************************
#   Procedimiento: game
#   Descripción: Pantalla principal del juego.
#   
#   Autor: Jojann De Vargas
#   Fecha: 20-02-2020
#   
#   Parámetros: player_id - Identifiador del jugador.
#   Retorno: player_id    - Identificador del jugador.
#            playerNumber - Número del jugador (puede ser 1 o 2)
#            game.id      - Identificador del juego.
#            options      - Lista de opciones que puede elegir el jugador.
# 
#   Historial de modificaciones
#   Fecha           usuario         descripción
#   20-02-2020      jdevargas       Creación.
# 
# *************************************************************************** 
def game(request, player_id):    
    playerNumber=-1
    try:
        player =  Player.objects.get(id=player_id)
    except:
       return render(request, 'endgame/error.html', {'error': 'The player do not exists! '}) 
    else:
        # Obtenemos las opciones habilitadas para el juego
        options = Options.objects.filter(state='A')
        # Obtiene el jugador y determina si es el uno o el dos.
        player=Player.objects.get(id=player_id)
        try:
            game = Game.objects.filter(estate='E').order_by('create_date')[:1].get()
            game.player_id_two=player
            game.estate='J'            
            game.save()
            playerNumber=2
        except:
            game = Game()
            game.player_id_one=player
            game.create_date=timezone.now()
            game.estate='E'
            game.save()
            playerNumber=1
        return render(request, 'endgame/game.html',{'player_id': player_id,'player_number': playerNumber, 'game_id': game.id, 'options' :options})

def wait(request, player_id, player_number):
    
    player = Player.objects.get(id=player_id)
    
    if player_number == 1:
        try:
            game   = Game.objects.get(player_id_one=player, estate='E')
        except:
            game   = Game.objects.get(player_id_one=player, estate='J')
    else:
        try:
            game   = Game.objects.get(player_id_two=player, estate='E')
        except:
            game   = Game.objects.get(player_id_two=player, estate='J')
    
    if game.is_ready():
        response = HttpResponse("Y") 
    else:
        response = HttpResponse("N") 
    
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "*"  
    return response 

def answergame(request, game_id, player_number, option_id):
    sbStatus='E'
    sbMessage='Update ok'
    try: 
        game = Game.objects.get(id=game_id)
        if player_number == 1:
            game.player_one_opc=Options.objects.get(id=option_id)
        else:
            game.player_two_opc=Options.objects.get(id=option_id)
        game.save()
    except Exception as e:
        sbStatus='F'
        sbMessage='No update. Failed. '
    data = {'sbStatus': sbStatus,
            'sbMessage': sbMessage
            }
    response = JsonResponse(data)
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "*" 
    return response

def gamestatus(request, game_id, player_number):
    game = Game.objects.get(id=game_id)
    opponnet_response='N'
    opponnet_name=''
    
    if player_number == 1:
        if game.player_two_opc:
            opponnet_response='Y'
            opponnet_name=game.player_id_two.player_name
        else:
            opponnet_name=game.player_id_two.player_name
    else:
        if game.player_one_opc:
            opponnet_response='Y'
            opponnet_name=game.player_id_one.player_name
        else:
            opponnet_name=game.player_id_one.player_name
    data = {
        'opponnet_response': opponnet_response,
        'opponnet_name': opponnet_name
    }
    return JsonResponse(data)

def gameresults(request):
    options     = Options.objects.filter(state='A')
    blSame      = False # Si hubo empate.
    
    # Se obtiene la información de entrada.
    game_id     = request.POST['game_id']
    player_id   = request.POST['player_id']
    playerNumber= request.POST['player_number']

    # Se determina el ganador
    game = Game.objects.get(id=game_id) # Se obtiene el juego
    opt_player1=game.player_one_opc.id  # Opción del jugador 1
    opt_player2=game.player_two_opc.id  # Opción del jugador 2

    #Empate
    if opt_player1 == opt_player2:
        blSame=True
    else:
        try:
            # Si la opción del jugador 1 es padre de la opción del jugador 2
            hierarchyOpt = HierarchyOpt.objects.get(father_id=opt_player1, child_id=opt_player2)
            # Win player 1
            game.player_win=game.player_id_one
            # Descripción de las opciones de los jugadores.
            opt_player1_desc=hierarchyOpt.father_id.description
            opt_player2_desc=hierarchyOpt.child_id.description
        except:
            # Si la opción del jugador 2 es padre de la opción del jugador 1
            hierarchyOpt = HierarchyOpt.objects.get(father_id=opt_player2, child_id=opt_player1)
            # Win player 2
            game.player_win=game.player_id_two
            # Descripción de las opciones de los jugadores.
            opt_player1_desc=hierarchyOpt.child_id.description
            opt_player2_desc=hierarchyOpt.father_id.description
    
    # Actualización de estado del juego y se determina la información de salida.
    game.estate='T'
    player_name1=game.player_id_one.player_name
    player_name2=game.player_id_two.player_name

    if blSame:
        results_msj='Both selected the same answer...'
    else:
        if int(player_id) == int(game.player_win.id):

            if int(playerNumber) == 1:
                results_msj='You Win! the ['+opt_player1_desc+'] is dominant over ['+opt_player2_desc+'].'
            else:
                results_msj='You Win! the ['+opt_player2_desc+'] is dominant over ['+opt_player1_desc+'].'
        else:
            if int(playerNumber) == 1:
                results_msj='You Lose! the ['+opt_player1_desc+'] is recessive over ['+opt_player2_desc+'].'
            else:
                results_msj='You Lose! the ['+opt_player2_desc+'] is recessive over ['+opt_player1_desc+'].'
    game.save()

    # Respuesta
    return render(request, 'endgame/gameresults.html',{
                                                        'options' :options,
                                                        'player_name1': player_name1, 
                                                        'player_name2': player_name2,
                                                        'player_number' : playerNumber, 
                                                        'opt_player1' :opt_player1, 
                                                        'opt_player2' :opt_player2, 
                                                        'results_msj' : results_msj })