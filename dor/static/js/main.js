$(document).ready(function() {

    function hoverBarResize(){
        $(".hover-bar").css("top", function(){
                console.log($("#landing-image").css("height"));
                var fullheight =  $("#landing-image").css("height");
                var finalheight = parseInt(fullheight) + 30;
                return finalheight + "px"
            });
    }

    //IMPLEMENT REST API FIRST
    function update_query(new_query){
        console.log(new_query);
        $.ajax({
            url: "/routes/taxonomy/?format=json",
            type: "POST",
            data: {q : new_query},

            success: function(result){
                $("#search-query").val('');
                console.log(result);
                console.log("success");
            }
        });
    }

    function search_query(new_query){
        var str = $("#results-view").text();
        var newstr = $.trim(str.replace(/[\t\n]+/g,' '));
        var strArray = newstr.split("  ");
        var newArray = [];
        for (var i = 0; i < strArray.length; i++){
            if (strArray[i] != ""){
                newArray.push(strArray[i])
            }
        }

        filteredArray = $.grep(newArray, function(n, i){
            return (n.indexOf(new_query) > -1);
        });

        for (var j = 0; j< $("#results-view").find("div").length; j++){
            $($("#results-view").find("div")[j]).css("display","none");
        }
        for (var k = 0; k<filteredArray.length; k++){
            $("#results-view").find(":contains('"+filteredArray[k]+"')").css("display","block")
        }
    }

    hoverBarResize();
    $(window).resize(function(){
            hoverBarResize();
        });

    $('#search-form').on('submit', function(event){
        event.preventDefault();
        new_query = $("#search-query").val();
        search_query(new_query);
    });

    $(".dropdown-menu li a").click(function(){
        var selText = $(this).text();
        $("#filter-button-area").append('<div class="full-button"><table><tr><td class="filter-button">'+selText+'</td><td class="x-button">x</td></tr></table></div>')
    });

    $("#filter-button-area").on('click', 'td.x-button', function(){
        $(this).closest('.full-button').remove();
        search_query($("#search-query").val());
    });

    $(".dropdown-menu li a").click(function(){
      var selText = $(this).text();
      search_query(selText);
    });

});