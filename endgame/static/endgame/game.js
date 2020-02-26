var w;

function startWorkerEnableResponse()
{
  if(typeof(Worker) !== "undefined") 
  {
    if(typeof(w) == "undefined") 
    {
      w = new Worker("work_gamestatus.js");
    }

    data= {
            game_id: document.getElementById("game_id").value,
            player_number: document.getElementById("player_number").value
          };

    w.postMessage(data);
    
    w.onmessage = function(event) 
    {
      document.getElementById("msj_wait").innerHTML = event.data.answer_message;
      
      if(!event.data.blContinue)
      {
        stopWorker()
        document.getElementById("answer").disabled=false;
      }
    };
  } else 
  {
    document.getElementById("state").innerHTML = "Sorry, your browser does not support Web Workers...";
  }
}

function startWorker() 
{
  if(typeof(Worker) !== "undefined") 
  {
    if(typeof(w) == "undefined") 
    {
      w = new Worker("work_game.js");
    }

    data= {
            player_id: document.getElementById("player_id").value, 
            player_number: document.getElementById("player_number").value
          };

    w.postMessage(data);
    
    w.onmessage = function(event) 
    {
      document.getElementById("state").innerHTML = event.data.wait_message;
      
      if(!event.data.blContinue)
      {
        stopWorker()
        startWorkerEnableResponse()
      }
    };
  } else 
  {
    document.getElementById("state").innerHTML = "Sorry, your browser does not support Web Workers...";
  }
}

function handler() 
{
  if(this.status == 200) 
    {
      console.log(this.response);
    }
}

function updateAnswer()
{
  game_id=document.getElementById("game_id").value;
  player_number=document.getElementById("player_number").value;
  option_id=document.querySelector('input[name="option_id"]:checked').value;

  var req = new XMLHttpRequest();
  req.onload = handler;
  req.open('GET', 'http://127.0.0.1:8000/endgame/'+game_id+'/'+player_number+'/'+option_id+'/answergame');
  req.send();
  
  var radioButtons = document.getElementsByName("option_id");
  
  for (var i = 0; i < radioButtons.length; i++) 
  {
    console.log(radioButtons[i].id);
    document.getElementById(radioButtons[i].id).disabled=true;
  }
}

function stopWorker() 
{ 
  w.terminate();
  w = undefined;
}