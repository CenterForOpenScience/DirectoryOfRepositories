$(document).ready(function() {

    function hoverBarResize(){
        $(".hover-bar").css("top", function(){
                console.log($("#landing-image").css("height"));
                var fullheight =  $("#landing-image").css("height");
                var finalheight = parseInt(fullheight) + 30;
                return finalheight + "px"
            });
    }

    function search_query(new_query){
        $.ajax({
            url: "/ajax_search/",
            type: "POST",
            data: {
                'search_text' : new_query,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(result){
                $("#search-query").val('');
                $("#results-view").html(result);
            }
        });
    }

    function filter_query(new_query){
        console.log(new_query);
        $.ajax({
            url: "/ajax_filter/",
            type: "POST",
            data: {
                'filter_text' : new_query,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(result){
                $("#results-view").html(result);
            }
        });
    }

    hoverBarResize();
    $(window).resize(function(){
            hoverBarResize();
        });

    search_query('');

    $('#user-icon').popover({
        html:true,
        content:'<a href="/login/"><div class="popover-custom">Login</div></a>',
        title: 'Welcome!'
    });

    $('#user-icon-auth').popover({
        html:true,
        content:'<a href="/manage/"><div class="popover-custom">Manage Repositories</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });

    $('.taxonomy-dropdown').select2({
        placeholder: "Filter Taxonomies",
        allowClear: true,
        width: '100%'
    });

    $('.standard-dropdown').select2({
        placeholder: "Filter Standards",
        allowClear: true,
        width: '100%'
    });

    $('.content-dropdown').select2({
        placeholder: "Filter Content-Types",
        allowClear: true,
        width: '100%'
    });

    $("#filter-button-area").on('click', 'td.x-button', function(){
        var finalFilters = {};
        var filterList = [];
        $(this).closest('.full-button').remove();
        var filterTags = $("#filter-button-area > div").text().split("x");
            for (var i = 0; i < filterTags.length; i++){
                if (filterTags[i] != ""){
                    filterList.push(filterTags[i]);
                }
            }
            finalFilters["tags"] = filterList;
            filter_query(JSON.stringify(finalFilters));
    });
    $('#search-form').on('submit', function(event){
        event.preventDefault();
        new_query = $("#search-query").val();
        search_query(new_query);
    });

    $(".dropdown").change(function(e){
        var finalFilters = {};
        var filterList = [];
        var selText = $("."+e.target.className).val();
        if (selText!=""){
            $("#filter-button-area").append('<div class="full-button"><table><tr><td class="filter-button">'+selText+'</td><td class="x-button">x</td></tr></table></div>')
            var filterTags = $("#filter-button-area > div").find(".filter-button");
            for (var i = 0; i < filterTags.length; i++){
                if (filterTags[i] != ""){
                    filterList.push(filterTags[i].innerHTML);
                }
            }
            finalFilters["tags"] = filterList;
            filter_query(JSON.stringify(finalFilters));
        }
    });

    $("#results-view").on('click','.toggle', function () {
        $toggleBar = $(this);
        $content = $toggleBar.parent().find(".repo-bottom");
        $content.slideToggle(500, function () {
            $toggleBar.children().attr('class', function () {
                return $content.is(":visible") ? "fa fa-chevron-up" : "fa fa-chevron-down";
            });
        });

    });
});