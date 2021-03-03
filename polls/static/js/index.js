var myChart=""
var ChartLikes=startNewChart("ChartLikes")
var ChartComments=startNewChart("ChartComments")
var ChartSentiment=startSentimentChart("ChartSentiment")
//var ChartLanguage=startNewChart("ChartLanguage")

typeGraph=["Likes"]
listGraph = [ChartLikes, ChartComments, ChartSentiment]
startNewChart("ChartLikes")

$(document).ready(function(){

    var allCheck = $(".year :checkbox");
    var allLabel = $(".year").find("label")
    var allLenght = $(".year :checkbox").length;
    var d = new Date();
    var lastYear = d.getFullYear();

    i=0
    $(".year").find("label").each(function(){
        if(i == 0) {
            $(this).html('<input type="checkbox" id="ALL" name="checkYear" value="ALL" style="margin-left:10px;"><small style="margin-left:5px;margin-right:10px; color:#fff">ALL</small>')
            i=1
        } else {

            $(this).html('<input type="checkbox" id="'+lastYear+'" name="checkYear" value="'+lastYear+'" style="margin-left:10px;"><small style="margin-left:5px;margin-right:10px; color:#fff">'+lastYear+'</small>')
            lastYear = lastYear-1
        }
    });

        
    

    $("#ALL").change(function(){
        uncheckALL()
    });

    $("#2021").change(function(){
        uncheckYear()
    });
    $("#2020").change(function(){
        uncheckYear()
    });
    $("#2019").change(function(){
        uncheckYear()
    });
    $("#2018").change(function(){
        uncheckYear()
    });
    $("#2017").change(function(){
        uncheckYear()
    });
    $("#2016").change(function(){
        uncheckYear()
    });


});

/*$("#username").keypress(function () {
    var username = $(this).val();

    $.ajax({
      url: 'ajax/validate_username/',
      data: {
        'username': username
      },
      dataType: 'json',
      success: function (data) {
        console.log(data)

      }
    });

  });
*/


function getTypeGraph(type){
    if(typeGraph.includes(type.value)){

        var profileIndex = typeGraph.indexOf(type.value);
        typeGraph.splice(profileIndex, 1);
        $("#Chart"+type.value).css("visibility", "hidden");
        
    } else {

        typeGraph.push(type.value)

        $("#Chart"+type.value).css("visibility", "visible");
        /*if("#Chart"+type.value != "#ChartSentiment")
            x = startNewChart("Chart"+type.value)
        else 
            x = startSentimentChart("Chart"+type.value)
        */
        listGraph.push(x)

    }

    
}

function startNewChart(chart){
    var ctx = document.getElementById(chart).getContext('2d');
    chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: "",
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 200, 32, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 200, 32, 1)'

            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        title: {
            display: true,
            text: 'Chart Averange ' + chart.substring(5) 
        }
    }
});

return chart

}


function uncheckALL()
  {
  allChk = $("input:checkbox");
       for (i = 0; i < allChk.length; i++)
          {
              if(allChk[i].value == "ALL"){}
              else          
              allChk[i].checked = false;

          }
  }

function uncheckYear()
{
  allChk = $("input:checkbox");
       for (i = 0; i < allChk.length; i++)
        {
              if(allChk[i].value == "ALL") allChk[i].checked = false;
              else {}      
        }
}

labelChart = []
dataL=[]
dataC=[]
dataS=[]
dataLen=[]
dataPos=[]
dataNeutral=[]
dataNegative=[]

function makeLabelChart(ciao, likes, nPost, comments, positive, neutral, negative){

    if(labelChart.includes(ciao.value)){
        var profileIndex = labelChart.indexOf(ciao.value);
        labelChart.splice(profileIndex, 1);
        dataL.splice(profileIndex, 1)
        dataC.splice(profileIndex, 1)
        dataPos.splice(profileIndex,1 )
        dataNeutral.splice(profileIndex, 1)
        dataNegative.splice(profileIndex, 1)

        for(i in listGraph){
            if(listGraph[i].canvas.id == "ChartLikes")
            addOrRemoveData(listGraph[i], labelChart, dataL)

            if(listGraph[i].canvas.id == "ChartComments")
            addOrRemoveData(listGraph[i], labelChart, dataC)

            if(listGraph[i].canvas.id == "ChartSentiment")
            addOrRemoveDataSent(listGraph[i], labelChart, dataPos,dataNeutral, dataNegative )
        }

        
    } else {

        labelChart.push(ciao.value)
        dataL.push((likes/nPost).toFixed(2))
        dataC.push((comments/nPost).toFixed(2))
        dataPos.push(positive)
        dataNeutral.push(neutral)
        dataNegative.push(negative)
 
        for(i in listGraph){
            if(listGraph[i].canvas.id == "ChartLikes")
            addOrRemoveData(listGraph[i], labelChart, dataL)

            if(listGraph[i].canvas.id == "ChartComments")
            addOrRemoveData(listGraph[i], labelChart, dataC)

            if(listGraph[i].canvas.id == "ChartSentiment")
            addOrRemoveDataSent(listGraph[i], labelChart, dataPos,dataNeutral, dataNegative )

            
            

        }
    }

}


data=""
firstMove=true
function addOrRemoveData(chart, label, data) {


    chart.data.labels=label
    chart.data.datasets[0].data=data
    chart.update();

}

function addOrRemoveDataSent(chart, label, data, data2, data3) {

    chart.data.labels=label
    chart.data.datasets[0].data = data
    chart.data.datasets[1].data=data2
    chart.data.datasets[2].data=data3

    chart.update();

}


function startSentimentChart(id){
var ctx = document.getElementById(id).getContext("2d");

var data = {
  labels: [],
  datasets: [{
    label: "Positive",
    backgroundColor: "green",
    data: []
  }, {
    label: "Neutral",
    backgroundColor: "grey",
    data: []
  }, {
    label: "Negative",
    backgroundColor: "red",
    data: []
  }]
};

var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: {
    barValueSpacing: 20,
    scales: {
      yAxes: [{
        ticks: {
          min: 0,
        }
      }]
    }
  }
});

return myBarChart
}

function submitFunction(button){

    item ='<p style="margin-top:50px;width:500px;font-size:24px">STO ANALIZZANDO IL PROFILO!<br>Insieme ad esso i suoi post! Tra poco avrai una stima di tutti i dati analizzati 😊</p>'

    $(".jumper").append(item)
    console.log("Dovrebbe andare il preloader prima")
    $("#preloader").animate({
        'opacity': '100'
    }, 100, function(){
        $("#preloader").css({'visibility': 'visible'}).fadeIn();
    
    });
    

    $("#form-submit").submit();

}