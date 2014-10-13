from flashcardapp.datacontroller import DataController
from flashcardapp.models import Container, Box
from dajaxice.decorators import dajaxice_register
from django.http import HttpResponse
from django.template import Context, loader
from django.utils import simplejson as json
import pdb

#----- get*List methods -----------------------------------

@dajaxice_register
def getBoxList(request, containerId):
    ''' Ajax wrapper for the DataController function 'getBoxList'

    *Takes*
      The Id of the container to put this box in.
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getBoxList(containerId)

@dajaxice_register
def getContainerList(request, classId):
    ''' Ajax wrapper for the DataController function 'getContainerList'

    *Takes*
      The Id of the container to put this box in.
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getContainerList(classId, request.user)

@dajaxice_register
def getClassList(request):
    ''' Ajax wrapper for the DataController function 'getClassList'

    *Takes*
      The Id of the container to put this box in.
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getClassList(request.user)

@dajaxice_register
def getLabelList(request):
    ''' Ajax wrapper for the DataController function 'getLabelList'

    *Takes*
      The Id of the container to put this box in.
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getLabelList(request.user)

@dajaxice_register
def getTagList(request):
    ''' Ajax wrapper for the DataController function 'getTagList'

    *Returns*
      A list of Tags encoded in json

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getTagList()

# ----- get* methods --------------------------------------

@dajaxice_register
def getFlashcard(request, flashcardId):
    ''' Ajax wrapper for the DataController function 'getFlashcard'

    *Returns*
      A Flashcard with the given id encoded in json

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getFlashcard(flashcardId)

@dajaxice_register
def getBox(request, boxId):
    '''Ajax wrapper for the DataController function 'getBox'

    *Returns*
      A Box with the given id encoded in json

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getBox(boxId)

@dajaxice_register
def getContainer(request, containerId):
    '''Ajax wrapper for the DataController function 'getContainer'

    *Returns*
      A Container with the given id encoded in json

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getContainer(containerId, request.user)

@dajaxice_register
def getClass(request, classId):
    '''Ajax wrapper for the DataController function 'getClass'

    *Returns*
      A Class with the given id encoded in json

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getClass(classId)

@dajaxice_register
def getContainers(request, classId):
    ''' Ajax wrapper for the DataController function
    'getContainersWithBoxesFromClass'

    *Takes*
      The id of the Class
    *Returns*
      JSON representation of the list of containers with their boxes

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getContainersWithBoxesFromClass(classId)

@dajaxice_register
def getBoxesAndFlashcards(request, containerId):
    '''Ajax wrapper for the DataController function 'getBoxesAndFlashcards'

    *Returns*
      A list of boxes with their corresponding flashcards encoded in json.

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.getBoxesAndFlashcardsFromContainer(containerId)



# ----- add* methods --------------------------------------

@dajaxice_register
def addFlashcard(request, FlashcardData):
    ''' Ajax wrapper for the DataController function 'addFlashcard'

    *Takes*
      A dictionary representing a flashcard
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.addFlashcard(FlashcardData, request.user)

@dajaxice_register
def addBox(request, BoxData):
    ''' Ajax wrapper for the DataController function 'addBox'

    *Takes*
      A dictionary representing a box
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.addBox(BoxData)

@dajaxice_register
def addContainer(request, ContainerData):
    ''' Ajax wrapper for the DataController function 'addContainer'

    *Takes*
      A dictionary representing a container
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.addContainer(ContainerData, request.user)

@dajaxice_register
def addClass(request, ClassData):
    ''' Ajax wrapper for the DataController function 'addClass'

    *Takes*
      A dictionary representing a class
    *Returns*
      A json string declaring saved data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.addClass(ClassData, request.user)

# ----- update* methods ----------------------------------
@dajaxice_register
def updateFlashcard(request, flashcardData):
    '''Ajax wrapper for the DataController function 'updateFlashcard'

    *Takes*
      A dictionary representing the updates to the flashcard
    *Returns*
      A json string declaring updated data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.updateFlashcard(flashcardData, request.user)

@dajaxice_register
def updateBox(request, boxData):
    '''Ajax wrapper for the DataController function 'updateBox'

    *Takes*
      A dictionary representing the updates to the box
    *Returns*
      A json string declaring updated data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.updateBox(boxData)

@dajaxice_register
def updateContainer(request, containerData):
    '''Ajax wrapper for the DataController function 'updateContainer'

    *Takes*
      A dictionary representing the updates to the container
    *Returns*
      A json string declaring updated data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.updateContainer(containerData, request.user)

@dajaxice_register
def updateClass(request, classData):
    '''Ajax wrapper for the DataController function 'updateClass'

    *Takes*
      A dictionary representing the updates to the class
    *Returns*
      A json string declaring updated data success or failure

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.updateClass(classData)

# ----- delete* methods ----------------------------------

@dajaxice_register
def deleteFlashcards(request, data):
    '''Ajax wrapper for the DataController function 'deleteFlashcards'.

    *Takes*
      **data** - A Dictionary indexed by box ids to a list of Flashcard ids
            *Example*: {boxId: [flashcardids], boxId: [flashcardIds],...}
    *Returns*
      A json string representing the success or failure of the delete

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.deleteFlashcards(data)

@dajaxice_register
def deleteBoxes(request, listofids):
    '''Ajax wrapper for the DataController function 'deleteBoxes'.

    *Takes*
      A list of box ids
    *Returns*
      A json string representing the success or failure of the delete

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.deleteBoxes(listofids)

@dajaxice_register
def deleteContainers(request, listofids):
    '''Ajax wrapper for the DataController function 'deleteContainers'.

    *Takes*
      A list of container ids
    *Returns*
      A json string representing the success or failure of the delete

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.deleteContainers(listofids, request.user)

@dajaxice_register
def deleteClasses(request, listofids):
    '''Ajax wrapper for the DataController function 'deleteClasses'.

    *Takes*
      A list of class ids
    *Returns*
      A json string representing the success or failure of the delete

    See the DataController documentation for more information
    '''
    dc = DataController()
    return dc.deleteClasses(listofids)

# ----- move* methods ------------------------------------

@dajaxice_register
def moveFlashcards(request, cardIds, boxId):
    ''' Ajax wrapper for the DataController method 'moveFlashcards'

    *Takes*
      **cardIds** - A list of the flashcard ids

      **boxId** - Id of the box to move the flashcards to.

    *Returns*
      A json string representing whether the move operation succeded or not.

    See the DataController documentation for more information.
    '''
    dc = DataController()
    return dc.moveFlashcards(cardIds, boxId)

@dajaxice_register
def moveBoxes(request, boxIds, containerId):
    ''' Ajax wrapper for the DataController method 'moveBoxes'

    *Takes*
      **boxIds** - A list of the box ids

      **boxId** - Id of the container to move the boxes to.

    *Returns*
      A json string representing whether the move operation succeded or not.

    See the DataController documentation for more information.

    '''
    dc = DataController()
    return dc.moveBoxes(boxIds, containerId)

# ----- Other random methods ----------------------------------

@dajaxice_register
def getCardsFromBox(request, boxId):
    ''' Ajax wrapper for the DataController function 'getFlashcardsFromBoxes'
    which handles getting the flashcards from one box

    *Takes*
      The id of the box
    *Returns*
      A json string representing the flashcards of a given box

    See the DataController documentation for more information
    '''
    idList = [boxId]
    dc = DataController()
    return json.dumps(dc.getFlashcardsFromBoxes(idList))

@dajaxice_register
def isUserAuthenticated(request):
    ''' Ajax utility method for the front-end, in case there is a need to
    know if the user is authenticated or not.

    *Returns*
      A json dictionary stating whether the user is authenicated or not.
      The response is of this form: {'validated':True|False}
    '''
    return json.dumps({'validated': request.user.is_authenticated()})

@dajaxice_register
def getPreviewView(request, containerId):
    '''Docstring goes here
    '''
    t = loader.get_template('flashcardapp/previewPartial.html')
    dc = DataController()
    data =  dc.getBoxesAndFlashcardsFromContainer(containerId)
    c = Context({"boxflashcarddata": data}) #variable name that is referenced in the view
    return HttpResponse(t.render(c))


#----- Share Methods --------

@dajaxice_register
def getSharedContainers(request):
    '''Ajax wrapper method for the DataController method 'getSharedContainers'

    *Returns*
      A json encoded list of Containers

    See the DataController documentation for more information.
    '''
    dc = DataController()
    return dc.getSharedContainers()

@dajaxice_register
def addContainerToMyCards(request, containerId, classId, isAutoUpdated):
    '''Ajax wrapper method for the DataController method 'addContainerToMyCards'

    *Takes*
      **containerId** - Id of the shared container to copy.
      **classId** - Id of the class to copy the container to.
      **isAutoUpdated** - Whether the container will be auto updated or not.
    *Returns*
      A json string declaring success or failure

    See the DataController documentation for more information.
    '''
    dc = DataController()
    return dc.addContainerToMyCards(containerId, classId, isAutoUpdated)

@dajaxice_register
def shareContainer(request, containerId, taglist):
    '''Ajax wrapper method for the DataController method 'shareContainer'

    *Takes*
      **containerId** - Id of the container to share.
      **taglist** - A list of tags to attach to the container
    *Returns*
      A json string representing whether the move operation succeded or not.

    See the DataController documentation for more information.
    '''
    dc = DataController()
    user = request.user
    return dc.shareContainer(containerId, taglist, user)

@dajaxice_register
def unshareContainer(request, containerId):
    '''Ajax wrapper method for the DataController method 'unshareContainer'

    *Takes*
      **containerId** - Id of the container to unshare.
    *Returns*
      A json string representing whether the move operation succeded or not.

    See the DataController documentation for more information.
    '''
    dc = DataController()
    return dc.unshareContainer(containerId)
