(function($){
  $(function(){

    $('.sidenav').sidenav();

  }); // end of document ready
  $(document).ready(function(){
    $('.modal').modal();
  });
          
})(jQuery); // end of jQuery name space
$(document).ready(function(){
    $("#outcome_list").empty();
    var outcome = "Course Name: " + course_info[1] +"\n"+"Course Code: "+course_info[0]+"\n\n"+"===================Learning Outcomes===================\n"
    for(var i=0;i<outcome_list.length;i++){
        $("#outcome_list").append("<li>"+outcome_list[i]+"</li>");
        outcome = outcome +(i+1)+". "+outcome_list[i] +"\n";
    }
    outcome = outcome + "\n===============Assessments Recommendation===============\n" +
        "For different abilities, we recommend the following assessments:\n\n";
    var count = 0;
    for (var key in assess_rec){
        count += 1;
        outcome += count+". "+key+": "+assess_rec[key].join(", ")+";\n";
    }
    $("#outcome_download").click(function(){
        console.log(outcome);
        var blob = new Blob(['\ufeff' +outcome], {type: 'text/txt,charset=UTF-8'});
        var href = window.URL.createObjectURL(blob);
        const aLink = document.createElement('a');
        aLink.href = href
        aLink.download = course_info[0]+"_outcomes.txt";
        aLink.click();
        window.URL.revokeObjectURL(href);
    });
});
