function delete_question(id){
    if (confirm("Etes vous sur de vouloir supprimer cette question?"))
    {postdeleteq(id);}
    return false;}

function add_mode(id){  
    $("#tt" + id).show();
    $("#at" + id).hide();
    $("#mt" + id).show();
    return false;}

function normal_mode(id){
    $("#mt" + id).hide()
    $("#at" + id).show()
    addtag(id);
    $("#tt" + id).hide();
    return false;}

function modifier_symptome(id){  
    $("#ts" + id).show();
    $("#ss" + id).show()
    $("#ms" + id).hide()
    return false;}

function sauver_symptome(id){
    $("#ms" + id).show()
    $("#ss" + id).hide()
    $("#ts" + id).hide();
    postsymptome(id);
    return false;}

function modifier(id){  
    $("#qt" + id).show();
    $("#s" + id).show()
    $("#m" + id).hide()
    return false;}

function sauver(id){
    $("#m" + id).show()
    $("#s" + id).hide()
    $("#qt" + id).hide();
    postqtext(id);
    return false;}

function sauver_priority(id){
    var data = {
        q_id:  id,
        priority: $("#pri" + id).val()};
    $.post("update_priority_question", data, 
        (function(data, status){}))
    return false;}

var machin = 0;
    
function postdeleteq(id){
    var data = {
        q_id:  id}
        $.post("delquestion", data, 
        (function(data, status){
        $("#q" + id).remove();
        }));}


function postsymptome(id){
    var data = {
        q_id:  id,
        symptometext: $("#ts" + id).val()};
        $.post("findandmodifysymp", data, 
        (function(data, status){
            $("#lbs" + id).text(
            $.parseJSON(data).symptome)
            })
        );}


function postqtext(id){
    var data = {
        q_id:  id,
        qtext: $("#qt" + id).val()};
    $.post("findandmodify", data, 
        (function(data, status){
            $("#lb" + id).text(
            $.parseJSON(data).question_text)
            })
        );}

function update_question(data, status, id){
    // update question_text
    response = $.parseJSON(data) ;
    $("#lb" + id).text(
        response.question.question_text);
    
    var code = "";
    
    for (var i =0; i< response.question.tags_ids.length; i++ )
    {
        code += " <mark class='tags'>";
        code += response.tags[i]+ " </mark>";
        code += "<button class='del'> X </button>"
    }

    $("#tg" + id).html(code);
    $("#tg" + id).children(".del").each(function(i){
        $( this ).click(function(){deltag(id, i)})});

}

function addtag(id){
    var data = {
        q_id:  id,
        tag_text: $("#tt" + id).val()};
    $.post("addtag", data,(function(data, status){
        update_question(data, status, id)}) );
    }

function deltag(q_id, tag_id){
    var data = {
        q_id: q_id,
        tag_id : tag_id}
    $.post("deltag", data,(function(data, status){
        update_question(data, status, q_id)}) );
    }

function delete_answer(q_id, ans_id){
    var data = {
        q_id: q_id,
        ans_id : ans_id};
    $.post("delete_answer_from_question", data,(function(data, status){
       }) );
    return false;
    }

function modify_answer(q_id, ans_id){
    var data = {
        q_id: q_id,
        ans_id : ans_id,
        ans_text: $("#ans" + q_id + ans_id).val() }
    $.post("modify_answer_from_question", data,(function(data, status){
       }) );
    return false;
    }

function delete_tag_inference_in_answer(q_id, ans_id, tag_num){
    alert('coucou');
    var data = {
        q_id: q_id,
        ans_id : ans_id,
        tag_num : tag_num}
    $.post("delete_tag_inference_in_answer", data,(function(data, status){
       }) );
    return false;
    }

function add_tag_inference_in_answer(q_id, ans_id){
    var data = {
        q_id: q_id,
        ans_id : ans_id,
        ans_tag_text : $("#ans_tag"+ q_id + ans_id).val()}
    $.post("add_tag_inference_in_answer", data,(function(data, status){
       }) );
    return false;
    }

function add_answer(q_id){
    var data = {
        q_id: q_id,
        ans_text : $("#new_ans"+ q_id).val()}
    alert($("#new_ans"+ q_id).val());
    $.post("add_answer", data,(function(data, status){
       }) );
    return false;
    }


$(function() {
    $( ".searchtags" ).autocomplete({
        source: function(request, response){
                
                var data = {
                    key:  request.term};
                $.get("search_tags", data, 
                (function(data, status){
                    response($.parseJSON(data).tags);
            }));
        }

            
    });
    });
