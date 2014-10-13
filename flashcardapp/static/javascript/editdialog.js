/**
 * @author Evan Larson
 */


function editClass(classid, updateClassName){
	
	Dajaxice.flashcardapp.getClass(function(data) {
		var classdata = eval(data);
		if (classdata.message === "SUCCESS") {
			$("#newclassname").val(classdata.class.title);
		}
	},{"classId":classid});
	
    $("#editclassdialog").dialog({
        height: 240,
        width: 415,
        modal: true,
        resizable: false,

        buttons:{
            Cancel: function(){
                clearClassFields()
                $(this).dialog("close");
            },

            "Edit Class Name": function() 
            {
               var classname = $("#newclassname").val();

               if(classname == ''){
                    alert("Sorry, but you need to give your class a name")
               }
               else{
                   var classdict = {'classId':classid,'title':classname}
                   Dajaxice.flashcardapp.updateClass(function(response) {
                   		var res = eval(response);
                   		if (res.updated) {
                   			displayMessage("Edit Successful");
                   			updateClassName(classname)
                   		}
                   		else {
                   			displayMessage("Edit Failed","failure");
                   		}
                   },{'classData':classdict});
                   $(this).dialog("close");
               }    
            }
       }
    })
}

function editContainer(containerId, updateContainerName){

    Dajaxice.flashcardapp.getContainer(function(data) {
    	var containerdata = eval(data);
    	if(containerdata.message === "SUCCESS") {
    		var container = containerdata.container
    		$("#newcontainername").val(container.title);
    	}
    },{"containerId":containerId});

    $("#editcontainerdialog").dialog({
        height: 250,
        width: 470,
        modal: true,
        resizable: false,

        buttons:{
            Cancel: function() {
                clearContainerFields()
                $(this).dialog("close")

            },
            "Edit Container Name": function() 
            {
                var name = $("#newcontainername").val();
                if (name === ""){
                    alert("Sorry, but you need to give your container a name")
                }
                else{
                    var containerdict = {'title':name,'containerId':containerId}
                    Dajaxice.flashcardapp.updateContainer(function(response) {
                    	var res = eval(response);
                    	if(res.updated) {
                    		displayMessage("Edit Successful");
                    		updateContainerName(name);
						}
						else {
							displayMessage("Edit Failed","failure");
						}
                    },{'containerData':containerdict})
						
                    $(this).dialog("close");
                }
            },
        }

    });
}

function editBox(boxid, updateBoxName){
	
	Dajaxice.flashcardapp.getBox(function(data) {
		var boxdata = eval(data);
		if (boxdata.message === "SUCCESS") {
			$("#newboxname").val(boxdata.box.title);
		}
	},{"boxId":boxid})

    $("#editboxdialog").dialog(
    {
        height: 260,
        width: 420,
        modal: true,
        resizable: false,


        buttons:
        {
            Cancel: function() {
                $(this).dialog("close");
                clearBoxFields()
            },

            "Edit Box Name": function() {
                var boxname = $("#newboxname").val();

                if(boxname == ''){
                    alert("Sorry, but you need to give your box a name")
                }
                else{     
                    var boxdict = {'title':boxname,'boxId':boxid}
                    Dajaxice.flashcardapp.updateBox(function(response) {
                    	var res = eval(response);
                    	if(res.updated) {
                    		displayMessage("Edit Successful");
                    		updateBoxName(boxname);
                    	}
                    	else {
                    		displayMessage("Edit Failed","failure");
                    	}
                    },{'boxData':boxdict})
                    $(this).dialog("close");
                }
            },
        }
    })  
}

function editCard(cardid, boxid, updateCardTerm){
    //var classSize = $('#cardclassoption option').size()
    //var containerSize = $('#cardcontaineroption option').size()
	var card = null;

	Dajaxice.flashcardapp.getFlashcard(function(data) {
		console.log("Got Flashcard Info");
		var carddata = eval(data);
		if (carddata.message === "SUCCESS") {
			card = carddata.flashcard
			$("#newcardfront").val(card.term);

			for (var i=0; i<card.textsides.length; i++) {
				addBackSide(true);
			}
			$("#editbackdiv").on("dropdownsready",function(event) {
				if (card !== null) {
					console.log("Drop Downs Ready Triggered");
					$("#editbackdiv div").each(function(index) {
						console.log(card);
						$(this).find(".editcardback").val(card.textsides[index].text);
						$(this).find("[data-selectid='"+ card.textsides[index].labelKey_id+"']").attr("selected",true);
					});
				}
			});
			populateInitialDropdowns();
		}
	},{"flashcardId":cardid});
	
	

    $("#editcarddialog").dialog({
        height: 550,
        width: 485,
        modal: true,
        resizable: false,
        
        buttons:{
        
            Cancel: function(){
                $("#editbackdiv").html("");
                $(this).dialog("close");
                card = null;
            },

            "Edit Card": function(){

                var selectedList = new Array()
                var term = $("#newcardfront").val();
                var back = $('#defaultcardback').val();
                var defaultside = $('#mydefaultback option:selected').data('selectid');
                
				var fieldsFilled = true;
                var backdict = []
    			$('#editbackdiv div').each(function() {
			        var backtext = $(this).find('textarea').val();
			        if (backtext === '' || backtext === undefined) {
			        	fieldsFilled = false;
			        }
			        else {
			        	var optionselected = $(this).find('.editbackoption option:selected').data('selectid');
			        	backdict.push({'type':'text', 'labelId':optionselected, 'data':backtext});
			        
			        	var select = $(this).find('#selectback option:selected').data('selectid');
                    	selectedList.push(select);
			        }
			    });

                selectedList = selectedList.sort();

				if (fieldsFilled) {
					var flashcardData = {'term':term,'defaultSideLabelId':defaultside,'boxId':boxid,'cardId':cardid,'otherSides':backdict}
                
                	Dajaxice.flashcardapp.updateFlashcard(function(data){
	                    if (data['updated']){
	                       displayMessage("Edit Successful");
	                       updateCardTerm(term)
	                    }
	                    else{
	                        //alert("Edit Unsucessful: " + data['message'])
	                        displayMessage("Edit Failed","failure");
	                    }
	                },{'flashcardData':flashcardData});
	                $(this).dialog("close");
	                card = null;
	                $("#editbackdiv").html('');
				}
				else {
					alert("All fields must contain text");
				}
            }
        }
    });
    card = null;
    $("#editbackdiv").html('');
}

function populateInitialDropdowns() {
	console.log("PopulateInitialDropdowns Called");
	Dajaxice.flashcardapp.getLabelList(function(response) {
	    var labelList = eval(response);
	    var $options = $('.editbackoption');

		$options.each(function() {
			$(this).html('');
			for (var i = 0; i<labelList.list.length;i++) {
				$(this).append('<option data-selectid="'+labelList.list[i].id+'" >' + labelList.list[i].name+'</option>');
	        }
	 	});
	 	$("#editbackdiv").trigger("dropdownsready");
	});
}

function addBackSide(initializing) {
	
	if ($("#editbackdiv div").size() === 0) {
		var newdiv = document.createElement("div");
    	newdiv.innerHTML = "<label>Back: </label><select id='mydefaultback' class='editbackoption'></select><textarea rows='3' cols='40' class='editcardback' id='defaultcardback'></textarea>"
    	document.getElementById("editbackdiv").appendChild(newdiv);	
	}
    else {
        var newdiv = document.createElement("div");
        newdiv.innerHTML ="<select class='editbackoption'></select><textarea rows='3' cols='40' class='editcardback' id='newback'></textarea>"
		document.getElementById("editbackdiv").appendChild(newdiv);
		
		if (!initializing) {
			Dajaxice.flashcardapp.getLabelList(function(response) {
	        	var labelList = eval(response);
	            $('#editbackdiv div').each(function() {
	                var $option = $(this).find('.editbackoption');
	                $option.each(function() {
	                	var size = $(this).find('option').size();
	                	if (size === 0) {
	            			$(this).html("<option data-selectid = 0 >Select a Side</option>");
	            			for (var i = 0; i<labelList.list.length;i++) {
								$(this).append('<option data-selectid="'+labelList.list[i].id+'" >'+labelList.list[i].name+'</option>');
	                    	}
	                	}
	                });
	            });
	        });
		} 
    }
}
