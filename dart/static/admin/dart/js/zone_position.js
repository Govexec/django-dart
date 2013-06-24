(function($){
     $(function(){
		toggle_date_published = function() {
			if ($("#id_enabled:selected").val() == 2){
				$(".date_published").show();
			}else {
				$(".date_published").hide();
			}
		}
		
		$("#id_enabled").change(toggle_date_published);
		$(document).ready(toggle_date_published);
		
     });
}(django.jQuery));