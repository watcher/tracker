/*	
	Primo Admin
	Stefano Giliberti, kompulsive@gmail.com - lessbit.com	
*/

$(document).ready(function(){
	
	/* Tabs */
	$("ul.tabs").idTabs();

	/* Side Subsections Accordion */
	$("#sub-menu ul").hide();
	$("#sub-menu h3.selected").next("ul").show();
	$("#sub-menu h3").click(function() {
		$(this).next("ul")
		.slideToggle(500)
		.siblings("ul:visible").slideUp({ duration: 1000, easing: 'easeOutExpo' });
		$(this).toggleClass("selected");
		$(this).siblings("h3").removeClass("selected");
	});

	/*** Alternates row colors! ***/
	$("tr:even:not(.table-header)").css("background-color", "#f9f9f9");

	/* Elements closing system */
	$(".canhide").append("<div class='close'></div>").css("position", "relative");
	$(".close").click(function() {
		$(this).hide();
		$(this).parent().slideUp(300);
	});

//
//	Close button on mouseover
//
//	$(".close").css("display", "none");
//  	$(".canhide").hover(
//      function () {
//        $(this).find(".close").show();
//      }, 
//      function () {
//        $(this).find(".close").fadeTo(2000, 1, function(){
//    		$(this).hide();
//  		});
//      }
//    ).dblclick(function() {
//    	$(this).slideUp(300);
//    });
	
	/* Tables controls */
	$("td.controls a").hide();
  	$("tr").hover(
      function () {
        $(this).find("td.controls a").show();
      }, 
      function () {
        $(this).find("td.controls a").hide();
      }
    );
	
	/* Active tab style fix */
	$("ul.tabs li a.selected").parent("li").addClass("selected");
	$("ul.tabs li a").click(function() {
		$("ul.tabs li").removeClass("selected");
		$(this).parent("li").addClass("selected");
	});
	
});