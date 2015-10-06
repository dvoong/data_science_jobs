$(document).ready(function(){
    $(".controller .btn").click(function(e){
	if($(this).hasClass("active")){
	    console.log("button already active");
	} else {
    	    var controller = $(this).parent();
	    var active_button = controller.find(".btn.active");
	    active_button.removeClass("active");
	    $(this).addClass("active");
	}
    });
});
