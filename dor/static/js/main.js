$(document).ready(function() {

    function hoverBarResize(){
        $(".hover-bar").css("top", function(){
                console.log($("#landing-image").css("height"));
                var fullheight =  $("#landing-image").css("height");
                var finalheight = parseInt(fullheight) + 30;
                return finalheight + "px"
            });
    }

    hoverBarResize();
    $(window).resize(function(){
            hoverBarResize();
        });
});