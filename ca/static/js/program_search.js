$(document).ready(function() {
    var query_name = $("#id_q").val();
    if (query_name != null) {
            $.get('/ca/program_search/', {search_name: query_name}, function(data) {
                $("#id_q_result").html(data);
            });
    }

    $("#id_q").keyup(function() {
        var query_name = $(this).val();
            $.get('/ca/program_search/', {search_name: query_name}, function(data) {
                $("#id_q_result").html(data);
            });
    });


    // Click to add to favorite program
    $(".fav_program_btn").click(function() {
        var program_id = $(this).attr("program-id");
        var this_btn = $(this);
        if (this_btn.html() == "Like") {
        $.get('/ca/add_fav_program', {program_id: program_id}, function(data) {
            if (data) {
                this_btn.html("Unlike");
            }
        });
        } else { // Unlike a program
        $.get('/ca/rm_fav_program', {program_id: program_id}, function(data) {
            if (data) {
                this_btn.html("Like");
            }
        });
        }
    });
});

