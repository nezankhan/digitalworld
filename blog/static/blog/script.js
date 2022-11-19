
function opacityheader(){
    $("#line1").addClass('opacity-100');
    $("#line2").addClass('opacity-50');
    $("#line3").addClass('opacity-50');
    $("#line4").addClass('opacity-50');
};


$(function() {
    opacityheader();
    $(".carousel").carousel( { interval: 2000 } );
    $("#carouselButton").click(function(){
        if ($("#carouselButton").children("i").hasClass("fa-pause")) {
            $(".carousel").carousel("pause");
            $("#carouselButton").children("i").removeClass("fa-pause");
            $("#carouselButton").children("i").addClass("fa-play");
        } else {
            $(".carousel").carousel("cycle");
            $("#carouselButton").children("i").removeClass("fa-play");
            $("#carouselButton").children("i").addClass("fa-pause"); 
        }
    });
});