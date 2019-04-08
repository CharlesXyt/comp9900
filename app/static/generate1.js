$(document).ready(function(){
//      $("#location_phrases").append("<br><br>");
      var temp = $("#location_phrases");
      for(var i=0; i<key_phrases.length; i++){
            temp.append("<div class='chip'>"+key_phrases[i]+"<i class='close material-icons'> close</i></div>");
      }
    });
    $( "#getstarted-button" ).click(function() {
      var verbs = ["Create", "Evaluate", "Analyse", "Apply", "Understand", "Remember"];
      var selectedVerbs = [];
      var selectedKeyPhrases = [];
      for (var i=0; i < verbs.length; i++){
          $.each($("#"+verbs[i]+" option:selected"), function(){
             selectedVerbs.push($(this).val());
        });
      }
      $("div.chip").each(function(){
        selectedKeyPhrases.push($(this).text());
      });

      $.ajax({
　　　　type:'post',
　　　　url:"/generate2",
　　　　data:JSON.stringify({Verbs: JSON.stringify(selectedVerbs),
                           Key_phrases: JSON.stringify(selectedKeyPhrases)}),
　　　　contentType : 'application/json',
　　　　success:function(data){
          window.location.href = "/generate2";
　　　　},
　　　　error: function (XMLHttpRequest, textStatus, errorThrown){
　　　　　　alert("error");
　　　　}
    });
 });