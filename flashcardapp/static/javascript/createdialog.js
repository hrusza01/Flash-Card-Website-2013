function createClass() {
    $("#classdialog").dialog({
        height: 230,
        width: 415,
        modal: true,
        resizable: false,

        buttons:{
            Cancel: function(){
                clearClassFields()
                $(this).dialog("close");
            },

            "Create New Class": function() 
            {            
               var classinput = $('#classname').val();

               if(classinput == ''){
                    $('#classname').addClass('error')
                }   
               else{
                   var classdict = {'title':classinput}
                   Dajaxice.flashcardapp.addClass(callback,{'ClassData':classdict});
                   $(this).dialog("close");
               }    
            }
       }
    })
    clearClassFields()
}

function createContainer() {

    populateClassDD('#containerclassoption');

    $("#containerdialog").dialog({
        height: 280,
        width: 470,
        modal: true,
        resizable: false,

        buttons:{
            Cancel: function() {
                clearContainerFields();
                $(this).dialog("close");
            },
            "Create New Container": function() 
            {
                var containerName = $('#containername').val();
                var classID = $('#containerclassoption option:selected').data('classid');
                var flag = true
            
                flag = checkInputWithEmpty('#containername',flag)
                flag = checkInput_Undefined('#containerclassoption',flag,'classid')

                if(flag){
                    var containerdict = {'title':containerName,'classId':classID}
                    Dajaxice.flashcardapp.addContainer(callback,{'ContainerData':containerdict});
                    $(this).dialog("close");
                }
            }
        }
    });
    clearContainerFields()
}

function createBox() {
    populateClassDD('#boxclassoption')
            
    $('#boxclassoption').change(function(){
        populateContainerDD('#boxclassoption','#boxcontaineroption')
    });

    $("#boxdialog").dialog(
    {
        height: 310,
        width: 420,
        modal: true,
        resizable: false,
        buttons:
        {
            Cancel: function() {
                $(this).dialog("close");
                clearBoxFields()
            },

            "Create New Box": function() {
                var boxinput = $('#boxname').val();

                var classID = $('#boxclassoption option:selected').data('classid')
                var containerID = $('#boxcontaineroption option:selected').data('containerid')
                var flag = true

                flag = checkInputWithEmpty('#boxname',flag)
                flag = checkInput_Undefined('#boxclassoption',flag,'classid')
                flag = checkInput_Undefined('#boxcontaineroption',flag,'containerid')

                if(flag){
                    var boxdict = {'title':boxinput,'containerId':containerID}
                    Dajaxice.flashcardapp.addBox(callback,{'BoxData':boxdict})
                    $(this).dialog("close");
                }
            }
        }
    })
    clearBoxFields()   
}

function createCard(){
    populateClassDD('#cardclassoption')
            
    $('#cardclassoption').change(function(){
        populateContainerDD('#cardclassoption','#containeroption')
    });

    $('#cardclassoption').change(function(){
        populateContainerDD('#cardclassoption','#cardcontaineroption')
    })

    $('#cardcontaineroption').change(function(){
        populateBoxDD('#cardcontaineroption','#cardboxoption')
    })
    
    addNewBack();

    $("#carddialog").dialog({
        height: 550,
        width: 485,
        modal: true,
        
        buttons:{
        
            Cancel: function(){
                clearCardFields()
                $(this).dialog("close");

            },

            "Create Card": function(){
                var flag = checkingAndAdding()
                if(flag){
                    $(this).dialog("close");
                    clearCardFields()                    
                }

            },

            "Create Multiple": function(){
                var flag = checkingAndAdding()
                if(flag){ 
                    $('#cardfront').val("")
                    resetBack()
                }


            }
        }
    })
    clearCardFields()
}
function getSelectedDict(){
    count = 0
    var selectedDict = {'0':count,'1':count,'2':count,'3':count,'4':count,'5':count,'6':count,'7':count}
    $('#backarea div').each(function() {
        var select = $(this).find('.backoption option:selected').data('selectid');
        currentcount = selectedDict[select];
        selectedDict[select] = currentcount + 1;
    })
    return selectedDict
}

function callback(data){
    if (data['saved']){
        displayMessage("Save Success",'Success')
    }
    else{
        displayMessage("Save Unsucessful" + data['message','failure'])
    }
}
function checkingAndAdding(){
    {
        var carddict = getBackInput()
        var keycount = 0;
        var input = $('#cardfront').val();
        var back = $('#newback').val();
        var defaultside = $('#defaultback option:selected').data('selectid');
        var classID = $('#cardclassoption option:selected').data('classid');
        var containerID = $('#cardcontaineroption option:selected').data('containerid');
        var boxID = $('#cardboxoption option:selected').data('boxid');
        var backdict = getBackInput()
        var selectedDict = getSelectedDict();


        var errorstring = 'The following errors were found: ' + "\n" + '\n'
        var createFlag = true;

        for(var keys in selectedDict){
            if(keys == '0'){
                if(selectedDict['0'] >= 1){
                    errorstring = errorstring + 'A side was not selected' + "\n"
                    createFlag = false
                    $('#newback').removeClass('defaultback').addClass('error')

                }
            }

            else{
                if(selectedDict[keys] >= 2){
                    errorstring = errorstring + 'Duplicate sides were selected' + "\n"
                    createFlag = false
                    $('.backoption').removeClass('backoption').addClass('error')

                }
            }
        }
        
         $('#backarea div').each(function(){
            var backinput = $(this).find('.cardback').val();
            if(backinput == ''){
                $(this).find('.cardback').addClass('error');
                createFlag = false
            }
            else{
                $(this).find('.cardback').removeClass('error');
            }
        })
        createFlag = checkInput_Undefined('#cardclassoption',createFlag,'classid')
        createFlag = checkInput_Undefined('#cardcontaineroption',createFlag,'containerid')
        createFlag = checkInput_Undefined('#cardboxoption',createFlag,'boxid')
        createFlag = checkInputWithEmpty('#cardfront',createFlag)

        if(defaultside == 0){
            errorMethod('#defaultback')
            createFlag = false
        }
        else{
            fixError('#defaultback')
        }
        $('#backarea div').each(function() {
            var text = $(this).find('.cardback').val()
            var selection = $(this).find('.backoption option:selected').data('selectid');
            if(text == ''){

                $(this).find('.cardback').addClass('error')
                createFlag = false
            }
            else{
                $(this).find('.cardback').addClass('error')
                checked = false
            } 

            if(selection == 0){
                errorMethod('.backoption')
                createFlag = false
            }
            else
                fixError('.backoption')

        })

        if(createFlag == true){
            var flashcarddict = {'term':input,'defaultSideLabelId':defaultside, 'boxId': boxID,'otherSides':backdict}
            Dajaxice.flashcardapp.addFlashcard(callback,{'FlashcardData':flashcarddict})

        }
        else{
            //alert(errorstring)
        }
    }
    return createFlag
}
function errorMethod(id){
    $(id).addClass('error')
}
function fixError(id){
    $(id).removeClass('error')
}

function checkInputWithEmpty(id,flag){
    var valid = flag
    currentinput = $(id).val()
    if(currentinput == ''){
        $(id).addClass('error')
        valid = false
    }
    else{
        $(id).removeClass('error')
    }
    return valid
}
function checkInput_Undefined(id,flag,lowerid){
    var valid = flag
    currentinput = $(id + ' option:selected').data(lowerid)
    if(currentinput == undefined){
        $(id).addClass('error')
        valid = false
    }
    else{
        $(id).removeClass('error')
    }
    return valid          
}
function addButton(backarea){
    var count = $("#"+ backarea +" div").length;
    var ddcount = 7 //fix this    
    
    if (count != ddcount){
        addNewBack();
    }
    else{
        displayMessage("You have exceeded your add count",'failure');
    }
}

function addNewBack(){
    if($('#backarea div').size() === 0){
        var newdiv = document.createElement("div");
        newdiv.innerHTML = "<label>Back: </label><textarea rows='3' cols='40' class='cardback'id='defaulttext'></textarea><select id='defaultback' class='backoption'></select>"
        document.getElementById("backarea").appendChild(newdiv);

        Dajaxice.flashcardapp.getLabelList(function(response){
            var labelList = eval(response);

            if ($('#defaultback option').size() != 8){
                $('.backoption').html("<option data-selectid = 0 >Select a Side</option>");
                for (var i = 0; i<labelList.list.length;i++){
                    $('.backoption').append('<option data-selectid="'+labelList.list[i].id+'" >'+labelList.list[i].name+'</option>');
                }
            }
        })
    }
    else{
        var newdiv = document.createElement("div");
        newdiv.innerHTML ="<label>Back: </label><textarea rows='3' cols='40' class='cardback'id='newback'></textarea><select class='backoption'></select>"
		document.getElementById("backarea").appendChild(newdiv);

        Dajaxice.flashcardapp.getLabelList(function(response){
        var labelList = eval(response);
            $('#backarea div').each(function() {
                if($(this).find('.backoption option').size() != 8){
                    $(this).find('.backoption').html("<option data-selectid = 0 >Select a Side</option>");
                    for(var i = 0; i<labelList.list.length;i++){
                        $(this).find('.backoption').append('<option data-selectid="'+labelList.list[i].id+'" >'+labelList.list[i].name+'</option>');
                    }
                }
            })
        })
    }
}
function removeABack(){
    var size = $('#backarea div').size()
    if(size ==1){
        displayMessage("Cannot Remove the orginal Back" ,'failure')
    }
    else{
        $('#backarea div').last().remove()
    }
}


function resetBack(){
    $('#backarea').html('');
    var newdiv = document.createElement("div");
    newdiv.innerHTML ="<label>Back: </label><textarea rows='3' cols='40' class='cardback'id='newback'></textarea><select class='backoption' id='defaultback'>"
   
    Dajaxice.flashcardapp.getLabelList(function(response) {
        var labelList = eval(response);

        if($('#defaultback option').size() != 8){
            $('.backoption').html("<option data-selectid = 0 >Select a Side</option>")
            for(var i = 0; i<labelList.list.length;i++){
                $('.backoption').append('<option data-selectid="'+labelList.list[i].id+'" >'+labelList.list[i].name+'</option>');
            }
        }
    })
    $('#backarea').append(newdiv)
}

function getBackInput(){
    var backdict = []
    $('#backarea div').each(function() {
            
        var backtext = $(this).find('textarea').val();
        var optionselected = $(this).find('.backoption option:selected').data('selectid');

        backdict.push({'type':'text', 'labelId':optionselected, 'data':backtext});
    })
    return backdict
}

function callback(data){
    if (data['saved'])
    {
        displayMessage("Save Success",'Success')
    }
    else
    {
        displayMessage("Save Unsucessful" + data['message'],'failure')
    }
}
function clearClassFields(){
    $("#classname").val("")
    $('#classname').removeClass('error')
}

function clearBoxFields(){
    $("#boxclassoption")[0].selectedIndex = 0;
    $("#boxcontaineroption")[0].selectedIndex = 0;
    $('#boxcontaineroption').html('')
    $('#boxname').val('');
    $('#boxname').removeClass('error')
    $('#boxcontaineroption').removeClass('error')
    $('#boxclassoption').removeClass('error')
}

function clearContainerFields(){
    $("#containername").val('')
    $("#containerclassoption")[0].selectedIndex = 0
    $('#containername').removeClass('error')
    $('#containerclassoption').removeClass('error')
}
function clearCardFields(){
    resetBack()
    $('#cardclassoption')[0].selectedIndex = 0
    $('#cardcontaineroption').html('')
    $('#cardboxoption').html('')
    $('#cardfront').val('')
    $('#cardclassoption').removeClass('error')
    $('#cardcontaineroption').removeClass('error')
    $('cardboxoption').removeClass('error')
    $('cardfront').removeClass('error')

}
function populateClassDD(string){
        Dajaxice.flashcardapp.getClassList(function(response) {
        var classList = eval(response);
        $(string).html("<option>Please Select a Class</option>")
        for(var i = 0; i<classList.list.length;i++){
            $(string).append('<option data-classid="'+classList.list[i].id+'" >'+classList.list[i].title+'</option>');
        }
    });
}
function populateContainerDD(classoption, containeroption){
    var classID = $(classoption + ' option:selected').data('classid')

    Dajaxice.flashcardapp.getContainerList(function(response){
        var containerList = eval(response);
        $(containeroption).html("<option id='containerselect'>Please Select a Container</option>")

        for(var i = 0; i<containerList.list.length;i++){
            $(containeroption).append('<option data-containerid="'+containerList.list[i].id+'" >'+containerList.list[i].title+'</option>');
        }
    },{'classId':classID})
}
function populateBoxDD(containeroption, boxoption){
    var containerID = $(containeroption + ' option:selected').data('containerid')

    Dajaxice.flashcardapp.getBoxList(function(response){
        var boxList = eval(response)
        $(boxoption).html("<option id='boxselect'>Please Select a Box</option")
        for(var i=0; i<boxList.list.length;i++){
            $(boxoption).append('<option data-boxid="'+boxList.list[i].id+'" >'+boxList.list[i].title+'</option>');
        }
    },{'containerId':containerID})
}