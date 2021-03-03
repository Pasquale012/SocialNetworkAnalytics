function submitNEWCOMMENT(button){

    item ='<p style="margin-top:50px;width:500px;font-size:24px">STO ANALIZZANDO DEI NUOVI COMMENTI!<br>Potrebbe volerci un pò di tempo!<br>Ma non ti preoccupare alla fine avrai tutti i commenti analizzati 😊</p>'
    $(".jumper").append(item)
    $("#preloader").animate({
        'opacity': '100'
    }, 100, function(){
        $("#preloader").css({'visibility': 'visible'}).fadeIn();
    
    });
    

}