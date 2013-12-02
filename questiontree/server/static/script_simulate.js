function answer(id, i){
    var data = {
        id: id,
        answer_choice: i}
    $.post("answer_simulation", data,(function(data, status){
        change_question(data)}) );
    return false;
    }

function change_question(html)
{
    $("#question_simu").html(html)
}


