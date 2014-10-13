$(function() {
	//add arrow to show this is the currently selected page.
	
	$("#mycardslink").after('<div class="arrow-up mycardsselected" ></div>');
	
	function displayContainers(data) {
		result = eval(data);
		if(result.message != 'SUCCESS'){
			alert(result.message);
		}
		else{
			var $cardsnavigator = $("#mycards");
			$cardsnavigator.html("");
			var containers = result.containers;
			var $moveto = $("#moveto");
			for (var i=0; i < containers.length; i++) { //Displays all of the containers within the selected class
				var container = containers[i];
				$moveto.append("<option>"+ container.title +"</option>");
				//Will need to get weather or not a container is private or not so we'll know which kind of icon to use
				if (container.isPrivate && container.isUpdatable) {
					var icon = '<img class="shareContainer" src="'+staticImagePath+'shareicon.png" />';
				}
				else if (!container.isUpdatable) {
					var icon = '<img class="notShareable" src="'+staticImagePath+'deactivatedshareicon.png" />';
				}
				else {
					var icon = '<img class="unshare" src="'+staticImagePath+'unshareicon.png" />';
				}
				$cardsnavigator.append('<h3 class="containerName"><span class="name selectable">' + container.title + '</span> ' + icon + ' </h3>');
				$cardsnavigator.append('<section class="boxsection" data-containerid="'+ container.id +'" data-title="'+ container.title +'"></section>');
				var $boxeslist = $cardsnavigator.find('[data-containerid="'+ container.id +'"]');
				var boxes = container.boxes;
				for (var j=0; j < boxes.length; j++) { //Display all of the boxes associated with the given container.
					$boxeslist.append('<div class="showbox" data-boxid="'+ boxes[j].id +'">' +
						'<p>' +
						'<img class="boximage studybox selectable" src="'+staticImagePath+'closedboxicon.png" %}" title="Double Click to Open this box" />' +
						'<span class="filename">'+ boxes[j].title +'</span>' +
						'</p>' +
					'</div>');
				}
			}
		}
	}
	
	$(".classimage").dblclick(function() {
		var classid = $(this).parent().find(".classname").data("classid");
		var classname = $(this).parent().find(".classname").html();
		$(".selected").removeClass("selected").addClass("selectable");
		$(".selectedtext").removeClass("selectedtext");
		getAndDisplaySelection();
		$("#selectedclass").html(" " + classname);
		Dajaxice.flashcardapp.getContainers(displayContainers, {'classId':classid});
	});
	
	function getAndDisplaySelection() {
		var $selected = $(".selected");
		if ($selected.length > 0) {
			var type = findSelectionType()
			if (type !== "Thing") {
				if ($(".notShareable").length !== 0) {
					if (type !== "Class" && type !== "Container") {
						//Check to see if the study box or flashcard is in a autoupdates container
						$selected.each(function() {
							var boxsection = $(this).parents()[2];
							var $autoupdateslabel = $(boxsection).prev().find(".notShareable");
							if ($autoupdateslabel.length !== 0) {
								enableButtons(false);
								manageMoveTo("none");
							}
							else {
								enableButtons(true);
								manageMoveTo(type);
							}
						});
					}
					else {
						enableButtons(true);
						manageMoveTo(type);
					}
				}
				else {
					enableButtons(true);
					manageMoveTo(type);
				}	
			}
			else {
				enableButtons(false);
				manageMoveTo("none");
			}
			
		}
		else {
			enableButtons(false);
			manageMoveTo("none");
		}
	}
	
	function findSelectionType() {
		var type = ""
		if ($(".selected").size() !== 0) {
			var type = $(".selected").first().attr("class").split(" ")[0];
		}
		switch(type) {
			case "classimage":
				type = "Class";
				break;
			case "boximage":
				type = "Study Box";
				break;
			case "cardimage":
				type = "Flashcard";
				break;
			case "name":
				type = "Container";
				break;
			default:
				type = "Thing";
		}
		return type;
	}
	
	function manageMoveTo(type) {
		var $moveto = $("#moveto");
		var $moveButton = $("#move");
		if (type === "Study Box") {
			$moveto.html("<option value='studybox'>--Move Study Box To--</option>");
			$(".boxsection").each(function() {
				$moveto.append('<option data-unitid="' + $(this).data("containerid") + '">' + $(this).data("title") + '</option>');
			})
			$moveButton.removeAttr("disabled");
		}
		else if(type === "Flashcard") {
			$moveto.html("<option value='flashcard'>--Move Cards To--</option>")
			$(".studybox").each(function() {
				$moveto.append('<option data-boxid="' + $(this).parent().parent().data("boxid") + '">' + $(this).next(".filename").html() + '</option>');
			});
			$moveButton.removeAttr("disabled");
		}
		else {
			//$("#moveto").find('option').remove();
			$('#moveto').html("<option>Move Flashcard or Box</option>");
			$moveButton.attr("disabled","disabled");
		}
	}
	
	$("#move").click(function() {
		var type = $("#moveto option:first").val();
		if (type==="flashcard") {
			var flashcardids = []
			$(".selected").each(function() {
				flashcardids.push($(this).parent().data("cardid"));
			});
			var targetboxid = $("#moveto option:selected").data("boxid");
			Dajaxice.flashcardapp.moveFlashcards(function(response) {
				var res = eval(response);
				if (res.moved) {
					var $boxtobemovedto = $(".openedbox[data-boxid='" + targetboxid + "']");
					if ($boxtobemovedto.length === 0) {
						$(".selected").each(function() {
							$(this).parent().remove();
						});
					}
					else {
						$(".selected").each(function() {
							$(this).parent().appendTo($boxtobemovedto);
						});
					}
					//alert("Cards Moved Sucessfully");
				}
				else {
					//var targetunitid = $("moveto option:selected").data("containerid");
					//res.message = our full failure message
					displayMessage("Failed to Move the Selected Flashcard(s)","failure");
				}
			}, {"cardIds":flashcardids, "boxId":targetboxid});
		}
		else { //If you have a study box selected
			var boxids = []
			$(".studybox.selected").each(function() {
				boxids.push($(this).parent().parent().data("boxid"));
			});
			var containerid = $("#moveto option:selected").data("unitid");
			Dajaxice.flashcardapp.moveBoxes(function(response) {
				var res = eval(response);
				if (res.moved) {
					var $targetunit = $('.boxsection[data-containerid="'+ containerid +'"]')
					$(".selected").each(function() {
						$(this).parent().parent().appendTo($targetunit);
					});
				}
				else {
					//res.message = our full failure message
					displayMessage("Failed to Move the Selected Box(es)", "failure");
				}
			}, {"boxIds":boxids, "containerId":containerid});
		}
	});
	
	function enableButtons(activate) {
		if (activate) {
			$("#edit").removeAttr("disabled");
			$("#delete").removeAttr("disabled");
			//$("#moveselected").removeAttr("disabled");
		}
		else {
			$("#edit").attr("disabled", "disabled");
			$("#delete").attr("disabled", "disabled");
			//$("#moveselected").attr("disabled", "disabled");
		}
	}
	
	//--------- Edit  Functionality ---------------
	
	//------ Edit Class/Flashcard/Box -------------
	$("#edit").click(function() {
		var type = findSelectionType();
		if (type === "Flashcard") {
			var cardid = $(".selected").first().parent().data("cardid");
			var boxid = $(".selected").parent().parent().data("boxid");
			console.log(cardid);
			editCard(cardid, boxid, function(name) {
				if (name !== undefined) {
					$(".selected").parent().find(".filename").html(name);
				}
			});
		}
		else if(type === "Study Box") {
			var boxid = $(".selected").parent().parent().data("boxid");
			editBox(boxid, function(name) {
				if (name !== undefined) {
					$('[data-boxid="'+ boxid +'"]').find(".filename").html(name);
				}
			});
		}
		else if(type === "Class") {
			var classid = $(".selected").parent().find(".classname").data("classid");
			editClass(classid, function(name) {
				if (name !== undefined) {
					$(".selected").parent().find(".classname").html(name);
				}
			});
		}
		else if (type === "Container") {
			var containerId = $(".selected").parent().next(".boxsection").data("containerid");
			editContainer(containerId, function(name) {
				//Get the new Container name and put it here
				if (name !== undefined) {
					$(".selected").first().html(name);
				}
			});
		}
	});
	
	
	//--------- Delete Button Functionality -------------
	$("#delete").click(function() {
		//Find out what kind of thing was selected to delete and respond accordingly
		var type = findSelectionType();
		$("#deletetype").html(type);
		
		$("#deletealert").dialog({
			modal: true,
			width: 350,
			height: 225,
			buttons: {
				Cancel: function() {
					$(this).dialog("close");
				},
				"Delete": function() {
					var data = []
					if (type === "Flashcard") {
						var data = {}
						$(".selected.cardimage").each(function() {
	        				//$(this).parent().remove();
	        				var cardId = $(this).parent().data("cardid");
							var boxId = $(this).parent().parent().data("boxid");
							if (boxId in data){
								data[boxId].push(cardId)
							}else{
								data[boxId] = [cardId]
							}
	        				//listofids.push(cardId);
        				});
        				//Dajaxice Method for Deleting Cards
        				Dajaxice.flashcardapp.deleteFlashcards(function(response) {
        					var resp = eval(response);
        					if (resp.deleted) {
        						$(".selected.cardimage").each(function() {
        							$(this).parent().remove();
        						});
        						displayMessage("Flashcard(s) Deleted Successfully");
        					}
        					else {
        						displayMessage("Delete Flashcards(s) Failed","failure");
        					}
    					},{'data':data});
					}
					else if(type === "Class") {
						$(".selected.classimage").each(function() {
							if($(this).parent().find(".classname").html() === "__default__") {
								//Can't Delete the Default Class
							}
							else {
								var classid = $(this).parent().find(".classname").data("classid");
								data.push(classid);
							}
						});
						//Dajaxice Method for Deleting Classes
						Dajaxice.flashcardapp.deleteClasses(function(response){
							var resp = eval(response);
        					if (resp.deleted) {
        						$(".selected.classimage").each(function() {
        							$(this).parent().remove();
        						});
        						displayMessage("Class(es) Deleted Successfully");
        					}
        					else {
        						displayMessage("Delete Class(es) Failed","failure");
        					}
						},{'listofids':data});
					}
					else if (type === "Study Box") {
						$(".selected.boximage").each(function() {
							var boxid = $(this).parent().parent().data("boxid");
							data.push(boxid);
						});
						Dajaxice.flashcardapp.deleteBoxes(function(response) {
							var resp = eval(response);
        					if (resp.deleted) {
        						$(".selected.boximage").each(function() {
        							$(this).parent().remove();
        						});
        						displayMessage("Box(es) Deleted Succcessfully");
        					}
        					else {
        						displayMessage("Delete Box(es) Failed");
        					}
						},{"listofids":data});
					}
					else if (type === "Container") {
						$(".selected").each(function() {
							var containerId = $(this).parent().next(".boxsection").data("containerid");
							data.push(containerId);
						})
						Dajaxice.flashcardapp.deleteContainers(function(response) {
							var resp = eval(response);
							if (resp.deleted) {
								$(".selected").each(function() {
									$(this).parent().next(".boxsection").remove();
									$(this).parent().remove();
								})
								displayMessage("Container(s) Deleted Successfully");
							}
							else {
								displayMessage("Delete Container(s) Failed", "failure");
							}
						},{"listofids":data});
					}
    				$(this).dialog("close");
				}
			}
		});
	});
	// ---------------- End Delete Button Functionality Definitions ------------------
	
	$("#mycards").delegate(".selectable", "click", function(e) {
		//Find the type of the selected thing and the type of any current selections
		var currentlyselectedtype = "";
		if ($(".selected").size() !== 0) {
			currentlyselectedtype = $(".selected").first().attr("class").split(" ")[0];
		}
		var newlyselectedtype = $(this).first().attr("class").split(" ")[0];
		if (currentlyselectedtype !== newlyselectedtype) {
			$(".selected").removeClass("selected").addClass("selectable");
			$(".selectedtext").removeClass("selectedtext");
		}
		
		$(this).removeClass("selectable").addClass("selected");
		$(this).next("span").addClass("selectedtext");
		getAndDisplaySelection();
	});
	
	$("#mycards").delegate(".selected", "click", function(e) {
		$(this).removeClass("selected").addClass("selectable");
		$(this).next("span").removeClass("selectedtext");
		getAndDisplaySelection();
	});
	
	$("#mycards").delegate(".hidebox", "click", function() {
		$(this).parent().parent().find("p").each(function() {
			if ($(this).find(".boximage").length === 0) {
				$(this).remove();
			}
			else {
				$(this).find(".boximage").removeClass("hidebox").addClass("selectable");
			}
		});
		//$(".selected").removeClass("selected").addClass("selectable");
		getAndDisplaySelection();
		$(this).parent().parent().removeClass("openedbox").addClass("showbox"); //Need to go up to levels to the parent div
		$(this).attr("src",staticImagePath+"closedboxicon.png");
	});
	
	$("#mycards").delegate(".showbox", "dblclick", function() {
		var boxId = $(this).data("boxid");
		$(this).removeClass("showbox").addClass("openedbox");
		var $boximage = $(this).first("div").find(".boximage");
		
		//Change the box image to an opened one
		$boximage.attr("src",staticImagePath+'openedboxicon.png');
		$boximage.removeClass("selectable").addClass("hidebox"); //also want to remove the selected class incase it was already selected.
		$(".selected").removeClass("selected").next("span").removeClass("selectedtext");
		getAndDisplaySelection();
		Dajaxice.flashcardapp.getCardsFromBox(function(data) {
			result = eval(data);
			if(result.message != 'SUCCESS'){
				//result.message = our full failure message
				displayMessage("Coulnd't load the contents of this box","failure");
				//alert(result.message);
			}
			else {
				var $selectedBox = $("[data-boxid='"+ boxId + "']");
				for (var i=0; i < result.cards.length; i++) {
					$selectedBox.append('<p data-cardid="'+ result.cards[i].id +'">'
					 + '<img class="cardimage selectable" src="'+staticImagePath+'flashcardicon.png" %}" />'
					 + '<span class="filename">' + result.cards[i].term + '</span>' +
					 '</p>');
				}
			}
		}, {'boxId':boxId});
	});
	
	$("#mycards").delegate(".shareContainer", "click", function() {
		var $shareicon = $(this);
		var sharedUnitId = $(this).parent().next(".boxsection").data("containerid");
        var availableTags = []
        Dajaxice.flashcardapp.getTagList(function(response) {
            var res = eval(response);
            if (res.message === "SUCCESS") {
                availableTags = res['list']
            }
            else {
                alert(res.message);
            }
        });
        
        function split( val ) {
			return val.split( /,\s*/ );
		}
        function extractLast( term ) {
			return split( term ).pop();
		}
        
        //Code for autocomplete functionality
		$( "#tagsinput" )
		  	.bind( "keydown", function( event ) {
				if ( event.keyCode === $.ui.keyCode.ENTER ){
					if ($( this ).data( "ui-autocomplete" ).menu.active ) {
						event.preventDefault();
					}else{
						var tagdiv = $("<div></div>", {'class':'tag', 'html':this.value})
						tagdiv.on('click', function(){
							$(this).remove();
						})
						tagdiv.appendTo("#tags-container");
                		this.value = "";
                   		return false;
					}
				}
		  	}).autocomplete({
				source: function( request, response ) {
					// delegate back to autocomplete, but extract the last term
					response( $.ui.autocomplete.filter(
						availableTags, extractLast( request.term ) ) );
				}
		  	});
		  	
		$("#sharealert").dialog({
			modal: true,
			width: 550,
			height: 375,
			buttons: {
				Cancel: function() {
					$(this).dialog("close");
				},
				"Share": function() {
                    //Add code to add tags
                    var tags = [];
                    $(".tag").each(function() {
                    	tags.push($(this).html());
                    })
                    
					Dajaxice.flashcardapp.shareContainer(function(response) {
						var res = eval(response);
						if (res.shared) {
							displayMessage("Share Successful");
							$shareicon.attr("src", staticImagePath+'unshareicon.png').removeClass("shareContainer").addClass("unshare");
						}
						else {
							//res.message = our full failure message
							display("Failed to Share", "failure");
						}
					},{"containerId":sharedUnitId, "taglist":tags});
    				$(this).dialog("close");
				}
			}
		});
	});
	
	$("#mycards").delegate(".unshare", "click", function() {
		var $unshareicon = $(this);
		var unitId = $(this).parent().next(".boxsection").data("containerid");
		$("#unsharealert").dialog({
			modal: true,
			width: 500,
			height: 260,
			buttons: {
				Cancel: function() {
					$(this).dialog("close");
				},
				"Remove From Shared": function() {
					Dajaxice.flashcardapp.unshareContainer(function(response) {
						var res = eval(response);
						if (res.unshared) {
							displayMessage("Successfully Removed From Shared");
							$unshareicon.attr("src", staticImagePath+"shareicon.png").removeClass("unshare").addClass("shareContainer");
						}
						else {
							//res.message = our full failure message
							displayMessage("Failed to Remove from Shared", "failure");
						}
					},{"containerId":unitId});
    				$(this).dialog("close");
				}
			}
		});
	})
});