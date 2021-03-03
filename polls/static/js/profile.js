function submitNEWPOST(button){

    item ='<p style="margin-top:50px;width:500px;font-size:24px">STO ANALIZZANDO ALTRI POST!<br> Dammi il tempo di frugare su Instagram 📷<br>Tra poco sarò subito da te😊</p>'
    $(".jumper").append(item)
    preladerAnimate()
    $("#form-submit").submit();

}

function submitPrivate(button){

    item ='<p style="margin-top:50px;width:500px;font-size:24px">Speriamo che non sia più privato! 😭<br> Dammi un secondo! 🤞'
    $(".jumper").append(item)
    preladerAnimate()

}

function submitGOTOPOST(button){

    item ='<p style="margin-top:50px;width:500px;font-size:24px">Sto analizzando i commenti del post, ci vorrà un pò di tempo! 💬<br> Nel frattempo mi collego al Cognitive Service di Azure per conoscere la Lingua e il Sentiment dei commenti analizzati! 🤩🤞'
    $(".jumper").append(item)
    preladerAnimate()

}

function preladerAnimate(){
    $("#preloader").animate({
        'opacity': '100'
    }, 100, function(){
        $("#preloader").css({'visibility': 'visible'}).fadeIn();
    
    });
}
