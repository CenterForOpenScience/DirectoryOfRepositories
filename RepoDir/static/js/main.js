$(document).ready(function() {

    function hoverBarResize(){
        $(".hover-bar").css("top", function(){
                var fullheight =  $("#landing-image").css("height");
                var finalheight = parseInt(fullheight) + 30;
                return finalheight + "px"
            });
    }

    function search_query(new_query){
        filters = [];
        if ($("#r_name").prop('checked')) {
            filters.push('r_name');
        }
        if ($("#r_tax").prop('checked')) {
            filters.push('r_tax');
        }
        if ($("#r_content").prop('checked')) {
            filters.push('r_content');
        }
        if ($("#r_desc").prop('checked')) {
            filters.push('r_desc');
        }
        if ($("#r_remarks").prop('checked')) {
            filters.push('r_remarks');
        }
        if ($("#r_certs").prop('checked')) {
            filters.push('r_certs');
        }
        if ($("#j_name").prop('checked')) {
            filters.push('j_name');
        }
        if ($("#j_endorsed").prop('checked')) {
            filters.push('j_endorsed');
        }
        $.ajax({
            url: "/ajax_search/",
            type: "POST",
            data: {
                'search_text' : new_query,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
                'filters': filters
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

    function approve_embargo_repo(repo_id_list){
        $.ajax({
            url:"/approve_embargo_repo/",
            type: "POST",
            data:{
                'repo_id_list': repo_id_list,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(result){
                console.log(result)
            }
        });
    }

    function delete_item(selected_group, deleted_group_list){
        $.ajax({
            url:"/delete_item/",
            type: "POST",
            data:{
                'selected_group': selected_group,
                'deleted_group_list': deleted_group_list,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(result){
                console.log(result)
            }
        });
    }

    function add_data_type(data_type_value){
        $.ajax({
            url:"/add_data_type/",
            type: "POST",
            data:{
                'data_type_value': data_type_value,
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(result){
                $("#data-scroll").prepend('<div class="row"> <div class="col-md-12"><label><input name="accepted_content" type="checkbox" value="'+result.id+'"> '+result.name+'</label></div></div>');
                $("#dataTypeEntry").val("");
            }
        });
    }

    hoverBarResize();
    $(window).resize(function(){
            hoverBarResize();
        });

    if (document.URL.endsWith("/search/")){
        search_query('');
    }

    $('#user-icon').popover({
        html:true,
        content:'<a href="/login/"><div class="popover-custom">Login</div></a><a href="/register/"><div class="popover-custom">Register</div></a><a href="/submit/Repositories"><div class="popover-custom">Submit Repositories</div></a>',
        title: 'Welcome!'
    });

    $('#user-icon-staff').popover({
        html:true,
        content:'<a href="/admin/"><div class="popover-custom">Site Administration</div></a><a href="/manage/"><div class="popover-custom">Site Management</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });

    $('#user-icon-auth').popover({
        html:true,
        content:'<a href="/submit/Repositories"><div class="popover-custom">Submit Repositories</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });

    $('#user-icon-auth-j').popover({
        html:true,
        content:'<a href="/manage/"><div class="popover-custom">Journal Management</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });

    $('#user-icon-sub-j').popover({
        html:true,
        content:'<a href="/submit/Jounrals"><div class="popover-custom">Submit A Journal</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });

    $('#user-icon-auth-r').popover({
        html:true,
        content:'<a href="/manage/"><div class="popover-custom">Repository Management</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });

    $('#user-icon-sub-r').popover({
        html:true,
        content:'<a href="/submit/Repositories"><div class="popover-custom">Submit A Repository</div></a><a href="/logout/"><div class="popover-custom">Logout</div></a>'
    });


    $('.taxonomy-dropdown').select2({
        placeholder: "Filter Taxonomies",
        allowClear: true,
        width: '100%'
    });

    $('.journal-dropdown').select2({
        placeholder: "Filter Journals",
        allowClear: true,
        width: '100%'
    });

    $('.content-dropdown').select2({
        placeholder: "Filter Accepted Data-Types",
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
            filter_query(JSON.stringify(finalFilters));
    });

    $('#search-button').on('click', function(event){
        event.preventDefault();
        new_query = $("#search-query").val();
        search_query(new_query);
    });

    $('#adv-search-button').on('click', function(event){
        event.preventDefault();
        $("#adv-search-options").toggle();
    });

    $(".dropdown").change(function(e){
        var finalFilters = [];
        var selText = $("."+e.target.className.split(' ')[0]).val();
        if (selText!=""){
            $("#filter-button-area").append('<div class="full-button"><table><tr><td class="filter-button" id="'+e.target.className+'">'+selText+'</td><td class="x-button">x</td></tr></table></div>')
            var filterTags = $("#filter-button-area > div").find(".filter-button");
            for (var i = 0; i < $('td.filter-button').length; i++) {
                console.log($($('td.filter-button')[i]).text());
                var filterTuple = {};
                filterTuple["type"] = e.target.className.split(' ')[0];
                filterTuple["tag"] = ($($('td.filter-button')[i]).text());
                finalFilters.push(filterTuple)
            }

            filter_query(JSON.stringify(finalFilters));
        }
    });

    $("#results-view").on('click','.toggle', function () {
        $toggleBar = $(this);
        $content = $toggleBar.parent().find(".repo-bottom");
        $content.slideToggle(500, function () {
            $toggleBar.children().attr('class', function () {
                return $content.is(":visible") ? "toggle-button fa fa-chevron-up" : "toggle-button fa fa-chevron-down";
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
            $($(this).find('div')[0]).html('<i class="fa fa-check-square-o fa-lg"></i> Endorsed')
        } else if($(this).attr('id') == "checked-button"){
            $(this).attr('id', "button");
            $($(this).find('div')[0]).html('<i class="fa fa-square-o fa-lg"></i> Endorse')
        }
    });

    $("#manage-wrapper").on('click','.approve-button', function(){
        var id = [$(this).attr("name")];

        approve_embargo_repo(JSON.stringify(id));

        if($(this).attr('id') == "button"){
            $(this).attr('id', "checked-button");
            $($(this).find('div')[0]).html('<i class="fa fa-check-square-o fa-lg"></i> Approved')
        } else if($(this).attr('id') == "checked-button"){
            $(this).attr('id', "button");
            $($(this).find('div')[0]).html('<i class="fa fa-square-o fa-lg"></i> Approve')
        }
    });

    $("#repo-table").on('click', '#trash-button', function(){
        var trash_id = [$(this).closest("tr").find("input").attr("class")];
        var trash_group = $(this).closest("tr").find("input").attr("id");

        $(this).closest('tr').remove();
        delete_item(trash_group, JSON.stringify(trash_id));
    });

    var selected = [];
    var selected_group = "";

    $("#button-apply").on('click', function(){
        if ($("#button-apply").prev().val() == "delete"){
            $('input:checkbox').each(function() {
                selected_group = $(this).attr('id');
                if (this.checked){
                    selected.push($(this).attr('class'));
                    $(this).closest('tr').remove();
                }
            });

            delete_item(selected_group, JSON.stringify(selected));
            selected = [];
        }

        else if($("#button-apply").prev().val() == "toggle-approval"){
            $('input:checkbox').each(function() {
                selected_group = $(this).attr('id');
                if (this.checked){
                    selected.push($(this).attr('class'));

                    var closest_btn = $(this).closest("tr").find(".btn")
                    if(closest_btn.attr('id') == "button"){
                        closest_btn.attr('id', "checked-button");
                        $(closest_btn.find('div')[0]).html('<i class="fa fa-check-square-o fa-lg"></i> Approved')
                    } else if(closest_btn.attr('id') == "checked-button"){
                        closest_btn.attr('id', "button");
                        $(closest_btn.find('div')[0]).html('<i class="fa fa-square-o fa-lg"></i> Approve')
                    }
                }
            });
            approve_embargo_repo(JSON.stringify(selected));
            selected = [];
        }
    });

    $(".checkbox").each(function(){
        var node_tab = $(this).attr('id');
        $(this).css("padding-left", node_tab * 25 + "px");
    });

    $("#data-input-button").on('click', function(){
       add_data_type($("#dataTypeEntry").val());
    });

});