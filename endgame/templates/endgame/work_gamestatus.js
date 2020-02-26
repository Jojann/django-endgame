var i = 0;
var game_id=0;
var player_number=0;
blContinue=true;

function timedCount() 
{
  i = i + 1;
  
  if(game_id != 0 && i%5==0)
  {
    var req = new XMLHttpRequest();
    req.open('GET', 'http://127.0.0.1:8000/endgame/'+game_id+'/'+player_number+'/gamestatus', false); 
    req.responseType = 'json';
    req.send(null);
    if (req.status == 200)
    { 
      console.log(req.response);

      if(req.response.opponnet_response == 'Y')
      { 
        blContinue=false;
        data={answer_message: "Hurry up! your opponent responded.", blContinue: blContinue};
        postMessage(data);

      }else
      {
        data={answer_message: "Wait for answer the player ["+req.response.opponnet_name+"]", blContinue: blContinue};
        postMessage(data);
      }
    }    
  }

  setTimeout("timedCount()",1000);
}

onmessage = function(e)
{
  game_id=e.data.game_id;
  player_number=e.data.player_number;
  console.log('game_id: '+game_id+' player_number: '+player_number);
};

timedCount();