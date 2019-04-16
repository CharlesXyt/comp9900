(function($){
    $(document).ready(function(){
      $('.modal').modal();
    });
            
  })(jQuery); // end of jQuery name space


$(document).ready(function(){
    $("#detail_list").empty();
    $("#course_info").html(course_info);
    for(var i=0;i<learning_outcomes.length;i++){
        if(result[i] == 1){
            $("#detail_list").append("<tr><td>"+learning_outcomes[i]+"</td><td><img src='static/smile.png' height='50' width='50'></img></td></tr>");
        }else{
            $("#detail_list").append("<tr><td>"+learning_outcomes[i]+"</td><td><img src='static/sad.png' height='50' width='50'></img></td></tr>");
        }

    }
    $(".outline").append("<p class='orange-text' style='font-size:20px;'>These learning outcomes cover "+count_cate+"/6 of Revised Bloom's Taxonomy cognitive process dimension.</p>")

});