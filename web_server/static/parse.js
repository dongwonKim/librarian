"use strict"

$(document).ready(function() {
	$.ajaxSetup({cache:false});
	setInterval(function() {
		$.ajax({
			type:"GET",
			url:"static/seats.xml",
			dataType:"xml",
			success:function(xml){
				$(xml).find("seat").each(function() {
					var name = $(this).attr("name");
					var type = $(this).find("type").text();
					var element = document.getElementById(name);
					if(type === "free"){
						element.setAttribute("style","background-color:#448AFF;");
					}
					else if(type === "use"){
						element.setAttribute("style","background-color:#FF5252;");
					}
					else if(type === "occupy"){
						element.setAttribute("style","background-color:#FFEB3B;");
					}
				});
			}

		});
	}, 1000);
});