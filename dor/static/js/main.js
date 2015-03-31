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

    function endorse_repo(repo_id, jour_id){
        $.ajax({
            url:"/endorse_repo/",
            type: "POST",
            data:{
                'repo_id': repo_id,
                'jour_id': jour_id,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(result){
                console.log(result)
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
        content:'<a href="/submissions/"><div class="popover-custom">Submit Repositories</div></a><a href="/manage/"><div class="popover-custom">Manage Repositories</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });

    $('.taxonomy-dropdown').select2({
        placeholder: "Filter Taxonomies",
        allowClear: true,
        width: '100%'
    });

    $('.journal-dropdown').select2({
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
        var finalFilters = [];
        $(this).closest('.full-button').remove();
        var filterTags = $("#filter-button-area > div").find(".filter-button");
            $.each(filterTags, function(index, value){
                if ($(value).html() != ""){
                    var filterTuple = {};
                    filterTuple["type"] = (value.id);
                    filterTuple["tag"] = (value.innerHTML);
                    finalFilters.push(filterTuple);
                }
            });
            console.log(JSON.stringify(finalFilters));
            filter_query(JSON.stringify(finalFilters));
    });

    $('#search-form').on('submit', function(event){
        event.preventDefault();
        new_query = $("#search-query").val();
        search_query(new_query);
    });

    $(".dropdown").change(function(e){
        var finalFilters = [];
        var selText = $("."+e.target.className).val();
        if (selText!=""){
            $("#filter-button-area").append('<div class="full-button"><table><tr><td class="filter-button" id="'+e.target.className+'">'+selText+'</td><td class="x-button">x</td></tr></table></div>')
            var filterTags = $("#filter-button-area > div").find(".filter-button");
            $.each(filterTags, function(index, value){
                if ($(value).html() != ""){
                    var filterTuple = {};
                    filterTuple["type"] = (value.id);
                    filterTuple["tag"] = (value.innerHTML);
                    finalFilters.push(filterTuple);
                }
            });
            console.log(JSON.stringify(finalFilters));
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

    $("#results-view").on('click','.btn', function(){
        var ids = $(this).attr("name");
        var id_table = ids.split(" ");

        var repository_id = id_table[0];
        var journal_id = id_table[1];

        endorse_repo(repository_id, journal_id);
        
        if($(this).attr('id') == "button"){
            $(this).attr('id', "checked-button");
            $($(this).find('div')[0]).html('<i class="fa fa-check-square-o fa-lg"></i> Endorse')
        } else if($(this).attr('id') == "checked-button"){
            $(this).attr('id', "button");
            $($(this).find('div')[0]).html('<i class="fa fa-square-o fa-lg"></i> Endorse')
        }
    });


});