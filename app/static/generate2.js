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
   for (var i=6-length; i<=6; i++){
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
});
