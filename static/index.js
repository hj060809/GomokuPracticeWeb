fetch('/setup')
      .then(function (response) {
        return response.json();
      }).then(function (infos) {
        console.log(infos.w);
        makeBoard(infos.w, infos.h);
      });

 var listboard = [];
 for(let i=0;i<20;i++){
    var row = [];
    for(let j=0;j<20;j++){
        row.push(0);
    }
    listboard.push(row);
 }


function makeBoard(w, h){
    var board = document.getElementById("board");
    for(let i = 0;i<=w;i++){
        var new_row = document.createElement('div');
        new_row.className = "row"
        new_row.id = "row"+i;

        board.appendChild(new_row);

        for(let j = 0;j<=h;j++){
            var new_block = document.createElement('div');
            new_block.className = "block"
            new_block.id = "block"+i+"_"+j;

            if(i != 0 && j != 0 ){
                var new_point = document.createElement('div');
                new_point.className = "point";
                new_point.classList.add("blank_point");
                var event = function(){
                    console.log(i+", "+j);
                    var userPlacedPoint = document.getElementById("point_"+i+"_"+j);
                    if(userPlacedPoint.classList.contains("blank_point")){
                        listboard[j-1][i-1] = -1;
                        userPlacedPoint.classList.remove("blank_point");
                        userPlacedPoint.style.backgroundColor = "black";
                        sendPlacedPoint();
                    }else{
                        alert("Already Placed");
                    }
                }
                new_point.addEventListener("click", event, false);
                new_point.id = "point_"+i+"_"+j;

                new_block.appendChild(new_point);
            }

            new_row.appendChild(new_block);
        }
    }
}

function drawPlacementByAI(x, y){
    var aiPlacedPoint = document.getElementById("point_"+x+"_"+y);
    listboard[y-1][x-1] = 1;
    aiPlacedPoint.classList.remove("blank_point");
    aiPlacedPoint.style.backgroundColor = "white";
}

function drawRecommendPoint(x, y){
    var recommendPoint = document.getElementById("point_"+x+"_"+y);
    recommendPoint.style.backgroundColor = "rgba(255, 100, 100, 0.5);";
}

function sendPlacedPoint(){
    fetch('/placedByUser',{
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "board":listboard
        })
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (isWin) {
            console.log(isWin.isWin);
            if(isWin.isWin){
                alert("You Win");
            }else{
                getAIPlacedPoint();
            }
        });
}

function getAIPlacedPoint(){
    fetch('/placedByAI')
        .then(function (response) {
            return response.json();
        })
        .then(function (AIPlacementPoint) {
            console.log(AIPlacementPoint.x, AIPlacementPoint.y, AIPlacementPoint.isWin);
            drawPlacementByAI(AIPlacementPoint.x, AIPlacementPoint.y);
            AIPlacementPoint.recommend_point
            if(AIPlacementPoint.isWin){
                alert("AI Win");
            }
        })
}