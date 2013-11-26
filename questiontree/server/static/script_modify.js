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
        id:  id,
        priority: $("#pri" + id).val()};
    $.post("update_priority_question", data, 
        (function(data, status){}))
    return false;}

var machin = 0;
    
function postdeleteq(id){
    var data = {
        id:  id}
        $.post("delquestion", data, 
        (function(data, status){
        $("#q" + id).remove();
        }));}


function postsymptome(id){
    var data = {
        id:  id,
        symptometext: $("#ts" + id).val()};
    $.post("findandmodifysymp", data, (function(data, status){
            change_question_div_with_html(id, data)}) );
    }


function postqtext(id){
    var data = {
        id:  id,
        qtext: $("#qt" + id).val()};
    $.post("findandmodify", data, (function(data, status){
        change_question_div_with_html(id, data)}) );
    }

function addtag(id){
    var data = {
        id:  id,
        tag_text: $("#tt" + id).val()};
    $.post("addtag", data,(function(data, status){
        change_question_div_with_html(id, data)}) );
    }

function deltag(id, tag_id){
    var data = {
        id: id,
        tag_id : tag_id}
    $.post("deltag", data,(function(data, status){
        change_question_div_with_html(id, data)}) );
    }

function delete_answer(id, ans_id){
    var data = {
        id: id,
        ans_id : ans_id};
    $.post("delete_answer_from_question", data,(function(data, status){
        change_question_div_with_html(id, data)}) );
    return false;
    }

function modify_answer(id, ans_id){
    var data = {
        id: id,
        ans_id : ans_id,
        ans_text: $("#ans" + id + ans_id).val() }
    $.post("modify_answer_from_question", data,(function(data, status){
        change_question_div_with_html(id, data)}) );
    return false;
    }

function delete_tag_inference_in_answer(id, ans_id, tag_num){
    var data = {
        id: id,
        ans_id : ans_id,
        tag_num : tag_num}
    $.post("delete_tag_inference_in_answer", data,(function(data, status){
        change_question_div_with_html(id, data)}) );
    return false;
    }

function add_tag_inference_in_answer(id, ans_id){
    var data = {
        id: id,
        ans_id : ans_id,
        ans_tag_text : $("#ans_tag"+ id + ans_id).val()}
    $.post("add_tag_inference_in_answer", data,(function(data, status){
        change_question_div_with_html(id, data)}) );
    return false;
    }

function add_answer(id){
    var data = {
        id: id,
        ans_text : $("#new_ans" + id).val()}
    $.post("add_answer", data,(function(data, status){
        change_question_div_with_html(id, data)}) );
    return false;
    }

    
function add_question(id){
    var data = {}
    $.post("add_question", data,(function(data, status){
        id = $.parseJSON(data)._id.$oid ;
        window.location.replace('/modifyone?id=' + id);
        }));
    return false;
    }




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

function change_question_div_with_html(question_id, html)
{
    $("#q" + question_id).html(html)
}


