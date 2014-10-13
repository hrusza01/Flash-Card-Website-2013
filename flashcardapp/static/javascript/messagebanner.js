function displayMessage(message, type) {
	if (type === "failure") {
		$("#successOrFailureMessage").removeClass("successmessage").addClass("errormessage");
	}
	else {
		$("#successOrFailureMessage").removeClass("errormessage").addClass("successmessage");
	}
	$("#successOrFailureMessage").html(message);
	$("#successOrFailureMessage").slideToggle("slow",function() {
		setTimeout(function() {
			$("#successOrFailureMessage").slideToggle("slow");
		},1000);
	});
}