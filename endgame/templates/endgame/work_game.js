var i = 0;
var player_id=0;

function timedCount() 
{
  i = i + 1;
  
  blContinue=true;

  data={wait_message: "Wait the other player! Time: "+i+" player_id: "+player_id, blContinue: blContinue};
  postMessage(data);

  if(player_id != 0 && i%5==0)
  {
    var req = new XMLHttpRequest();
    req.open('GET', 'http://127.0.0.1:8000/endgame/'+player_id+'/'+player_number+'/wait', false); 
    req.send(null);
    if (req.status == 200)
    {
      if(req.responseText == 'Y')
      { 
        blContinue=false
        data={wait_message: "Ready! player_id: "+player_id, blContinue: blContinue};
        postMessage(data);

      }
      
      console.log(req.responseText);
    }    
  }

  setTimeout("timedCount()",1000);
}

onmessage = function(e)
{
  player_id=e.data.player_id;
  player_number=e.data.player_number;
  console.log('player_id: '+player_id+' player_number: '+player_number);
};

timedCount();