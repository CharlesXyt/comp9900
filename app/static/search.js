//autocomplete
const ac = document.querySelector('.autocomplete');
// M = materialize library

console.log(availableTags)
M.Autocomplete.init(ac, {
    data:availableTags,
    minLength: 4
});
$(window).keydown(function(e){
    var curKey = e.which;
    if(curKey == 13){
        $('course_form').submit();
    }
})
