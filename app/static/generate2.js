$(document).ready(function(){
//<!--dynamically generate verb options-->
    var length = 6;
    if (verb_list.length < length){
      length = verb_list.length;
    }
    for(var i=1; i<=length; i++){
        $("#outcome_verb_"+i).append("<option value=''>"+verb_list[i-1]+"</option>");
        for (var j=0; j<verb_list.length; j++){
          $("#outcome_verb_"+i).append("<option value='"+verb_list[j]+"'>"+verb_list[j]+"</option>");
        }
    }
    if (length < 6){
       for (var i=length+1; i<=6; i++){
          $("#outcome_verb_"+i).append("<option value=''>Choose the key verb</option>");
          for (var j=0; j<verb_list.length; j++){
            $("#outcome_verb_"+i).append("<option value='"+verb_list[j]+"'>"+verb_list[j]+"</option>");
          }
        }
    }

    //<!--dynamically generate key phrases options-->
    for (var i=1; i<=6; i++){
        $("#outcome_key_phrases_"+i).append("<option value=''>Choose the key phrase</option>");
        for (var j=0; j<key_phrases_list.length; j++){
            $("#outcome_key_phrases_"+i).append("<option value='"+key_phrases_list[j]+"'>"+key_phrases_list[j]+"</option>");
        }
    }
    $('select').material_select();


  $("#submit-button").click(function(){
    var outcome_list=[];
    var verb;
    var key_phrase;
    var context;
    for (var j=1;j<7;j++){
        verb = $("#outcome_verb_"+j+" :selected").text();
        key_phrase = $("#outcome_key_phrases_"+j+" :selected").text();
        context = $("#input_text_"+j).val();
        if(verb == "Choose the key verb" ||  key_phrase == "Choose the key phrase"){
          continue;
        }
        console.log(verb+" "+key_phrase+" "+context);
        outcome_list.push(verb+" "+key_phrase+" "+context);
    }
    for(var j=7;j<10;j++){
      verb = $("#input_text_"+j+"_1").val();
      key_phrase = $("#input_text_"+j+"_2").val();
      context = $("#input_text_"+j+"_3").val();
      if(verb == "" ||  key_phrase == ""){
        continue;
      }
      outcome_list.push(verb+" "+key_phrase+" "+context);
    }
    $.ajax({
　　　　type:'post',
　　　　url:"/generate3",
　　　　data:JSON.stringify({outcome_list: JSON.stringify(outcome_list),
                           }),
　　　　contentType : 'application/json',
　　　　success:function(data){
          window.location.href = "/generate3";
　　　　},
　　　　error: function (XMLHttpRequest, textStatus, errorThrown){
　　　　　　alert("error");
　　　　}
    });
  });
});

