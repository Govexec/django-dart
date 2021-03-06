function parse_url( url ) {
    var a = document.createElement('a');
    a.href = url;
    return a;
}

function ad_focus(id){
	$(".ad-debug-layer").removeClass("highlighted-ad");
	var debug_object = $("#" + id + "_debug_layer");
	$(debug_object).addClass("highlighted-ad");
}

function ad_debug_close_layer(obj){
	$(obj).parent().hide();
}

$(document).ready(function(){
	$("body").keypress(function(event){
		//Toggled by cntrl-F10 or cntrl-b
		if ((event.which == 63245) || (event.which == 2)){
			
			$("body").append("\
<style type=\"text/css\">\
.ad-debug-layer {\
	position:absolute;\
	border:1px solid #000000;\
	background-color: rgb(247, 248, 224);\
	z-index:10000;\
}\
.highlighted-ad {\
	border:2px solid #990000;\
}\
.ad-debug-panel {\
	position:fixed;\
	bottom:0px;\
	width:99%;\
	border-top: 5px solid #333333;\
	background-color:#cccccc;\
	height:400px;\
	overflow:scroll;\
	z-index: 100000;\
	padding: 5px;\
	background-color: #eeeeee;\
}\
.ad-debug-panel-pane{\
	border: 1px solid #333333;\
	margin-bottom:10px;\
	padding: 5px;\
	backgorund-color:#eeeeee;\
}\
.ad-debug-layer-close {\
	display:block;\
	float: right;\
	width:10px;\
	border-left:1px solid #000000;\
	border-bottom:1px solid #000000;\
	padding:0 3px;\
}\
</style>\
");
			
			
			if (window.ad_debug){
				window.ad_debug = false;
				$(".ad-debug-layer").remove();
				$(".ad-debug-panel").remove();
			}else {
			
			
				window.ad_debug = true;
				
				$("body").append("<div class=\"ad-debug-panel\"></div>");
				
				$(".ad").each(function(){
					
					//give the ad an id if it doesnt have one
					if ($(this).attr("id") == ""){
						$(this).attr("id", "ad_debug_" + Math.rand());
						
					}
					
					if (! $(this).is(":visible")){
						$(this).show();
					}
					
					//Check for unloaded ads, give them a minimum value
					if ($(this).height() == 0){
						var ad_loaded = false
						$(this).height("100px");
						$(this).css("min-width", "100px");
						var height = 100;
						var width = 100;
					}else{
						var ad_loaded = true;
						var height = $(this).height();
						var width = $(this).width();
					}
					
					var position = $(this).offset();
					var top = position.top;
					var left = position.left;
					
					
					
					var url = $(this).find("script").eq(1).attr("src");
					
					var domain = parse_url(url).host;
					var pathname = parse_url(url).pathname;
					var path_sections = pathname.split("/");
					if (path_sections[0] != "adj") {
						var network = path_sections[1];
						var site = path_sections[3];
						var params = path_sections[4];
					}else { 
						var network = "";
						var site = path_sections[2];
						var params = path_sections[3];
					}
					
					var param_sections = params.split(";");
					var zone = param_sections[0];
					var param_dict = []
					for (i=1;i < param_sections.length;i++){
					
						var pair = param_sections[i].split("=");
						param_dict[pair[0]] = pair[1];
					}
					var position = param_dict["pos"];
					
					$("body").append("<div class=\"ad-debug-layer\" id=\"" + $(this).attr("id") + "_debug_layer\" style=\"top:" + top + "px;left:" + left + "px;width:" + width + "px;height:" + height + "px;\"><a href=\"#\" class=\"ad-debug-layer-close\" onclick=\"ad_debug_close_layer(this);\">X</a><b>" + zone + ": " + param_dict["pos"] + "</b><br />" + param_dict["sz"] + "<\/div>");
					
					$(".ad-debug-panel").append("<ul class=\"ad-debug-panel-pane\">\
					<li><b>Zone/Position:</b> " + zone + " - " + position  + "</li>\
					<li><b>Ad loaded:</b> " + ad_loaded + "</li>\
					<li><b>Site:</b> " + site  + "</li>\
					<li><b>Domain:</b> " + domain + "</li>\
					<li><b>Network:</b> " + network  + "</li>\
					<li><b>Params:</b> " + params + "</li>\
					<li><b>URL:</b> " + url + "</li>\
					<li><a href=\"#" + $(this).attr("id") + "\" onclick=\"ad_focus('" + $(this).attr("id") + "')\">Highlight</a></li>\
					</ul>");
					
					
				});
			
				
			}			
		
		}
	
	});
});