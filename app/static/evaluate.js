$(document).ready(function(){
    $("#detail_list").empty();
    for(var i=0;i<learning_outcomes.length;i++){
        if(result[i] == 1){
            $("#detail_list").append("<tr><td>"+learning_outcomes[i]+"</td><td><img src='static/smile.png' height='50' width='50'></img></td></tr>");
        }else{
            $("#detail_list").append("<tr><td>"+learning_outcomes[i]+"</td><td><img src='static/sad.png' height='50' width='50'></img></td></tr>");
        }

    }
});