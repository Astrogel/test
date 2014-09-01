$(document).ready(function() {

        // JQuery code to be added in here.
    
    
    $('#likes').click(function(){
    var notid;
    notid = $(this).attr("data-notid");
     $.get('/notebooks/like_notebook', {notebook_id: notid}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
           });
});

});
