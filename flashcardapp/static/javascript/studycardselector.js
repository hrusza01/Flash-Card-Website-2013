$(function() {
	$(".displayclass").button();
	
	$("#startstudying").click(function() {
		var boxesChecked = false;
		$(":checked").each(function() {
			alert($(this).val());
			boxesChecked = true;
		});
		if (boxesChecked) {
			window.location = "cardviewer.html";
		}
	});
});