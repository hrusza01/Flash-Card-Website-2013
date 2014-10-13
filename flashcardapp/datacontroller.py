from django.utils import simplejson as json
from flashcardapp.models import *
from django.db.models import Q
from django.contrib.auth.models import User
import urllib2
import urllib
import logging
import random
import pdb

logger = logging.getLogger('dajaxice')


class DataController:
    SUCCESS_STR = "SUCCESS"
    DEFAULT_TITLE = "__default__"


    #Utility method
    def getModelFieldsDict(self, obj):
        d = obj.__dict__.copy()
        if '_state' in d:
            del d['_state']
        if 'eav' in d:
            del d['eav']
        if 'publicationDate' in d:
            d['publicationDate'] = d['publicationDate'].isoformat(' ')
        d['id'] = d.pop('Id')
        return d

    # ------ Add* methods -------------------------

    def addFlashcard(self, data, curr_user):
        ''' Adds a flashcard to the database and associates it with the
        appropriate box if necessary.

        This function takes a dictionary that holds the values of the flashcard.
        Recognized dictionary keys are:
            + 'boxId' - The id of the box to hold the flashcard (optional)
              If left out, flashcard is put into the default class.
            + 'term' - The flashcard's term/front side (Required)
            + 'defaultSideLabelId' - The flashcard's definition/back side (Required)
            + 'otherSides' - A list of dictionaries describing the additional sides (Optional)
               Each side dictionary should be of the following form:
                 {'type': 'text'|'image'|'audio'|'video', 'labelId': <labelId>, 'data': <data based on type>}

        If the term and definition aren't defined, the flashcard won't be saved
        to the database and will return a message notifying of such.

        *Takes*
          **data** - A json string representing a dictionary that describes
          the flashcard.

          **curr_user** - The current user. This method will check to see if the
          user is authenticated.
        *Returns*
          A json string declaring success or failure
        '''
        try:
            if not curr_user.is_authenticated():
                raise Exception("You are not logged in! Log in to create a Flashcard!")
                # Create flashcard from hashtable data
            flashcard = Flashcard()
            keys = ["term", "defaultSideLabelId", "boxId", "otherSides"]

            if keys[0] in data:
                flashcard.term = data["term"]
            else:
                raise Exception("No 'term' is defined for this flashcard")

            if keys[1] in data:
                flashcard.defaultSideLabel = Label.objects.get(pk=data[keys[1]])
            else:
                raise Exception("No 'defaultSideLabel' is defined for this flashcard")

                #if keys[1] in data:
            #flashcard.definition = data["definition"]
            #else:
            #raise Exception("No 'definition' is defined for this flashcard")

            flashcard.save()

            if keys[2] in data and data[keys[2]]:
                id = data["boxId"]
                box = Box.objects.get(pk=id)
                flashcard.boxes.add(box)
                flashcard.save()
            else:
                # Add to the default box of the default container of the default class
                self.addToDefaultClass(flashcard, curr_user)

            #Parse through the different sides
            if keys[3] in data:
                sides = data[keys[3]]
                for side in sides:
                    if side['type'] == 'text':
                        ts = TextSide(text=side['data'])
                        ts.labelKey = Label.objects.get(pk=side['labelId'])
                        ts.flashcardKey = flashcard
                        ts.save()
                    elif side['type'] == 'image':
                        pass
                    elif side['type'] == 'audio':
                        pass
                    elif side['type'] == 'video':
                        pass

            return json.dumps({"saved": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'saved': False, 'message': e.message})

    def addBox(self, data):
        ''' Adds a Box to the database and associates it with the
        appropriate container if necessary.

        This function takes a dictionary that holds the values of the box.
        Recognized dictionary keys are:
            + 'title' - The title of the box (Required)
            + 'containerId' - The id of the container to hold the box (optional)

        If the title isn't defined, the box won't be saved to the database and
        will return a message notifying of such.

        *Takes*
          **data** - A json string representing a dictionary that describes the box.
        *Returns*
          A json string declaring success or failure
        '''
        try:
        # Create box from dictionary data
            box = Box()
            keys = ["title", "containerId"]
            if keys[0] in data:
                box.title = data["title"]
            else:
                raise Exception("No 'title' is defined for this box")

            box.save()
            if keys[1] in data:
                id = data["containerId"]
                cn = Container.objects.get(pk=id)
                box.containers.add(cn)
            else:
                raise Exception("No 'containerId' was defined for this box")

            return json.dumps({"saved": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'saved': False, 'message': e.message})


    def addContainer(self, data, curr_user):
        ''' Adds a Container to the database and associates it with the
        appropriate class if necessary.

        This function takes a dictionary that holds the values of the box.
        Recognized dictionary keys are:
            + 'title' - The title of the box (Required)
            + 'classId' - The id of the container to hold the box (optional)

        If the title isn't defined, the container won't be saved to the database
        and will return a message notifying of such.

        *Takes*
          **data** - A json string representing a dictionary that describes the
          container.
        *Returns*
          A json string declaring success or failure
        '''
        try:
            # Create box from dictionary data
            cn = Container()
            keys = ["title", "classId"]

            if keys[0] in data:
                cn.title = data["title"]
            else:
                raise Exception("No 'title' is defined for this container")

            if keys[1] in data:
                cn.save()
                classid = data[keys[1]]
                cl = Class.objects.get(pk=classid)
                cn.classes.add(cl)
            else:
                raise Exception("No 'classId' was defined for this container")

            #Set the owner
            cn.owner = curr_user

            cn.save()

            return json.dumps({"saved": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'saved': False, 'message': e.message})

    def addClass(self, data, curr_user):
        ''' Adds a Class to the database and associates it with the
        appropriate user if necessary.

        This function takes a dictionary that holds the values of the box.
        Recognized dictionary keys are:
            + 'title' - The title of the class (Required)

        If the user isn't logged in (authenticated), this method will throw an
        error capable informing the user of such.

        If the title isn't defined, the class won't be saved to the database and
        will return a message notifying of such.

        *Takes*
          **data** - A json string representing a dictionary that describes the class.

          **curr_user** - The current user. This method will check to see if the
          user is authenticated.
        *Returns*
          A json string declaring success or failure
        '''
        try:
            # Ensure the user is authenticated
            if not curr_user.is_authenticated():
                raise Exception("You are not logged in! Log in to create a class!")
            cls = Class(user=curr_user)
            keys = ["title"]
            if keys[0] in data:
                cls.title = data["title"]
            else:
                raise Exception("No 'title' is defined for this box")
            cls.save()

            return json.dumps({"saved": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'saved': False, 'message': e.message})


    # ----- Different Add Methods ------------------------------------
    def addContainerToMyCards(self, containerId, toClassId, isAutoUpdated):
        ''' Copies a shared container to a class of another user and sets whether
        it auto-updates or not.

        Technically, a copy of the container and its boxes are made and associated
        with the given class. However, these new boxes still contain references
        to the old flashcards.

        *Takes*
          **containerId** - Id of the shared container to copy.

          **classId** - Id of the class to copy the container to.

          **isAutoUpdated** - Whether the container will be auto updated or not.
        *Returns*
          A json string declaring success or failure
        '''
        try:
            cnt = Container.objects.get(pk=containerId)
            toClass = Class.objects.get(pk=toClassId)
            if isAutoUpdated:
                cnt.classes.add(toClass)
            else:
                #Save away the box foreign keys for later
                boxIds = [box.Id for box in cnt.box_set.all()]
                #Copy and save the new container
                cnt.pk = None
                cnt.Id = None
                cnt.isPrivate = True
                cnt.owner = toClass.user
                cnt.sharedAttributes = None
                cnt.save()

                #Update the classes on the NEW container
                cnt.classes.clear()
                cnt.classes.add(toClass)
                cnt.save()

                #Copy and save the new boxes while keeping references to all
                #the Flashcards.
                for id in boxIds:
                    box = Box.objects.get(pk=id)
                    fcset = box.flashcard_set.all()
                    box.pk = None
                    box.Id = None
                    box.save()
                    box.flashcard_set = fcset
                    box.containers.add(cnt)
            cnt.save()
            return json.dumps({"added": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'added': False, 'message': e.message})

    def addToDefaultClass(self, item, curr_user):
        ''' Adds a container, box, or flashcard to the default container

        **NOTE** - Currently, the implementation only allows flashcards to be
        added to the default container.

        *Takes*
          **item** - The Container, Box, or Flashcard to add to the default Class

          **curr_user** - The current user. This method will check to see if the
          user is authenticated.
        *Returns*
          A json string declaring success or failure
        '''
        # Ensure the user is authenticated
        if not curr_user.is_authenticated():
            raise Exception("You are not logged in!")

        #If 'item' is a Flashcard, add it to the default Box of the default
        #Container of the default Class
        qs = Class.objects.filter(user=curr_user, title=DataController.DEFAULT_TITLE)
        if not qs.exists():
            self.addDefaultClass(curr_user)
        if isinstance(item, Flashcard):
            defaultCls = Class.objects.get(user=curr_user, title=DataController.DEFAULT_TITLE)
            defaultCnt = defaultCls.container_set.all()[0]
            dbox = defaultCnt.box_set.all()[0]
            item.boxes.add(dbox)
            item.save()

    def addDefaultClass(self, curr_user):
        ''' Adds the default class for a particular user. This class holds any
        flashcards that aren't registered with other classes.

        *Takes*
          **curr_user** - The current user. This method will check to see if the
          user is authenticated.
        *Returns*
          A json string declaring success or failure
        '''
        try:
            #TODO - Do a check to see if the user is invalid, ensure the user is
            # still active and is definitely new.
            # Ensure the user is authenticated
            if not curr_user.is_authenticated():
                raise Exception("You are not logged in!")
                # Create box from dictionary data
            cls = Class.objects.create(title=DataController.DEFAULT_TITLE, user=curr_user)
            cnt = Container.objects.create(title=DataController.DEFAULT_TITLE)
            cnt.classes.add(cls)
            box = Box.objects.create(title=DataController.DEFAULT_TITLE)
            box.containers.add(cnt)

            return json.dumps({"saved": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'saved': False, 'message': e.message})


    # ------------- Different Get Methods -------------------------

    def getRandomFlashcardsFromBoxes(self, listofboxids, numofcards):
        ''' Pulls a random number of flashcards from the boxes given.

        If the number of flashcards is greater than the number of flashcards in
        the boxes combined, then all the cards will be returned.

        The randomness of this method is based on the Python random module and
        there is no gaurenteed that all the cards will be selected before
        another flashcard shows up again.

        *Takes*
          **listofboxids** - A list of ids of the box to get the flashcards from.

          **numofcards** - The number of cards to return.

        *Returns*
          A dictionary with a key 'message', describing how the operation
          performed, and a key 'cards', the list of random flashcards
        '''
        try:
            data = self.getFlashcardsFromBoxes(listofboxids)
            if data['message'] != DataController.SUCCESS_STR:
                raise Exception(data['message'])
            if numofcards > len(data['cards']):
                numofcards = len(data['cards'])
            randomcards = random.sample(data['cards'], numofcards)
            return {'message': DataController.SUCCESS_STR, 'cards': randomcards}
        except Exception, e:
            return {'message': e.message, 'cards': None}



    def getFlashcardsFromBoxes(self, listofboxids):
        ''' Gets all the Flashcards in the specified boxes

        *Takes*
          **listofboxids** - A list of numbers representing box ids

            *Example*: (["Box1id","Box2id"])
        *Returns*
          JSON representation of a list of cards with their fields
          ([{"id":<id>,"term":<term>,"defaultSideLabel_id":<definition>,"sidelabels:"[{"id":<labelId>,"name":<labelName>}],"sides":{<labelid>:{"id":<id>, "text":<text>}}}])
        '''
        try:
            q = Q()
            for Id in listofboxids:
                q = q | Q(boxes__Id=Id)
            qs = Flashcard.objects.filter(q)
            carddata = []
            for card in qs:
                carddict = self.getModelFieldsDict(card)
                labellist = []
                sidedict = {}
                for ts in TextSide.objects.filter(flashcardKey__Id=card.Id):
                    tsdict = {}
                    tsdict['id'] = ts.Id
                    tsdict['text'] = ts.text

                    label = ts.labelKey
                    labellist.append({"id": label.Id, "name": label.name})

                    sidedict[label.Id] = tsdict

                carddict['sidelabels'] = labellist
                carddict['sides'] = sidedict

                carddata.append(carddict)

            return {'message': DataController.SUCCESS_STR, 'cards': carddata}
        except Exception, e:
            return {'message': e.message, 'cards': None}

    def getClasses(self, curr_user):
        ''' Gets all of the class objects in the database associated with the
        current user. If the current user isn't authenticated, then it will return
        all the classes that aren't associated with any user. This may be no
        classes at all or perhaps sample classes.

        *Take*
          **curr_user** - The current user. This method will check to see if the
          user is authenticated.
        *Returns*
          A python list of the Class objects
        '''
        if curr_user.is_authenticated():
            return Class.objects.filter(user=curr_user).order_by('title')
        else:
            return Class.objects.filter(user=None).exclude(title=DataController.DEFAULT_TITLE)

    def getContainersFromClass(self, classId):
        ''' Gets all of the container objects associated with the given class id.

        *Takes*
          **classId** - Id of the class to get the Containers from.
        *Returns*
          A json encoded list of containers
        '''
        try:
            cls = Class.objects.get(pk=classId)
            data = cls.container_set.all()
            containers = []
            for cnt in data:
                cntdict = self.getModelFieldsDict(cnt)
                cntdict['isUpdatable'] = (cnt.owner == cls.user)
                containers.append(cntdict)
            return json.dumps({'message': DataController.SUCCESS_STR, 'containers': containers})
        except Exception, e:
            return json.dumps({'message': e.message, 'containers': None})

    def getBoxesFromContainer(self, containerId):
        ''' Gets all of the box objects associated with the given container id.

        *Takes*
          **containerId** - Id of the Container to get the boxes from.
        *Returns*
          A json encoded list of boxes.
        '''
        try:
            cnt = Container.objects.get(pk=containerId)
            data = cnt.box_set.all()
            boxes = []
            for i in range(len(data)):
                boxes.append(self.getModelFieldsDict(data[i]))
            return json.dumps({'message': DataController.SUCCESS_STR, 'boxes': boxes})
        except Exception, e:
            return json.dumps({'message': e.message, 'boxes': None})

    def getSharedContainers(self):
        ''' Gets all the containers that are shared, or public.

        *Returns*
          A json encoded list of Containers
        '''
        try:
            data = Container.objects.filter(isPrivate=False)
            sharedContainers = []
            for i in range(len(data)):
                cnt = data[i]
                cdict = self.getModelFieldsDict(cnt)
                taglist = []
                for tag in cnt.tag_set.all():
                    taglist.append(self.getModelFieldsDict(tag))
                cdict['tags'] = taglist
                cdict['sharedAttributes'] = self.getModelFieldsDict(cnt.sharedAttributes)
                sharedContainers.append(cdict)
            return json.dumps({'message': DataController.SUCCESS_STR, 'containers': sharedContainers})
        except Exception, e:
            return json.dumps({'message': e.message, 'containers': None})

    def getContainersWithBoxesFromClass(self, classId):
        ''' Gets all Containers and their boxes from a certain class.

        *Takes*
          **classId** - Id of the class to get the Containers and Boxes from.
        *Returns*
          JSON representation of the list of containers with their boxes
          ([{"title": <ClassTitle>,"boxes":[{"title":<box1title>,"id":<box1id>},...])
        '''
        try:
            hashtable = {}
            containers = Container.objects.filter(classes__Id=classId)
            for c in containers:
                hashtable[c] = Box.objects.filter(containers__Id=c.Id)
                # Create the json string
            responsedata = []
            for c in hashtable.keys():
                boxes = []
                for b in hashtable[c]:
                    boxes.append(self.getModelFieldsDict(b))
                cntdata = self.getModelFieldsDict(c)
                cntdata['isUpdatable'] = (c.owner == Class.objects.get(pk=classId).user)
                #if cntdata.sharedAttributes != None:
                #cntdata['sharedAttributes'] = self.getModelFieldsDict(c.sharedAttributes)
                cntdata['boxes'] = boxes
                responsedata.append(cntdata)
            return json.dumps({'message': DataController.SUCCESS_STR, 'containers': responsedata})
        except Exception, e:
            return json.dumps({'message': e.message, 'containers': None})


    def getBoxesAndFlashcardsFromContainer(self, containerId):
        '''Get all the Boxes with their Flashcards from a given Container

        *Takes*
          **containerId** - Id of the container to get the Boxes and Flashcards from.
        *Returns*
          A JSON representation of the list of Boxes with their Flashcards.
            *Example*:
            [{'title':<title>,'flashcards':[{'term':<term>,'definition':<definition>,'textsides':[{'label':<label>,'text':<text>}]}]}]
        '''
        try:
            cnt = Container.objects.get(pk=containerId)
            boxes = cnt.box_set.all()
            responsedata = []

            # Build the list of boxes
            for box in boxes:
                bdict = {}
                bdict['title'] = box.title
                flashcards = box.flashcard_set.all()
                fclist = []
                #Build the list of flashcards for each box
                for fc in flashcards:
                    fcdict = {}
                    fcdict['term'] = fc.term
                    fcdict['defaultSideLabel'] = {'id': fc.defaultSideLabel.Id, 'name': fc.defaultSideLabel.name}
                    textsides = fc.textside_set.all()
                    if len(textsides) > 0:
                        tslist = []
                        #If the Flashcard has extra side, build the list
                        #of different sides for the Flashcard.
                        for ts in textsides:
                            tsdict = {}
                            tsdict['label'] = ts.labelKey.name
                            tsdict['text'] = ts.text
                            tslist.append(tsdict)

                        fcdict['sides'] = tslist
                    else:
                        fcdict['sides'] = None

                    fclist.append(fcdict)

                bdict['flashcards'] = fclist
                responsedata.append(bdict)

            return json.dumps({'message': DataController.SUCCESS_STR, 'data': responsedata})
        except Exception, e:
            return json.dumps({'message': e.message, 'data': None})


    # ----- Get* methods -----------------------------------

    def getFlashcard(self, id):
        ''' Returns a dictionary representation of a Flashcard encoded in json.
        The following keys in the dictionary are:
          + 'id' - The Id of the Flashcard
          + 'term' - The front facing term of the Flashcard
          + 'definition' - The Flashcard's definition

        *Takes*
          **id** - Id of the Flashcard to return

        *Returns*
          A json string representing the Flashcard
        '''
        try:
            f = Flashcard.objects.get(pk=id)
            fdict = self.getModelFieldsDict(f)
            tslist = []
            for ts in f.textside_set.all():
                tsdict = self.getModelFieldsDict(ts)
                label = Label.objects.get(pk=tsdict['labelKey_id'])
                tsdict['label'] = self.getModelFieldsDict(label)
                tslist.append(tsdict)

            fdict['textsides'] = tslist
            return json.dumps({'message': DataController.SUCCESS_STR, 'flashcard': fdict})
        except Exception, e:
            return json.dumps({'message': e.message, 'flashcard': None})

    def getBox(self, id):
        ''' Returns a dictionary representation of a Box encoded in json.
        The keys in the dictionary are:
          + 'id' - The Id of the Box
          + 'title' - The box's title

        *Takes*
          **id** - Id of the Flashcard to return

        *Returns*
          A json string representing the Box
        '''
        try:
            b = Box.objects.get(pk=id)
            return json.dumps({'message': DataController.SUCCESS_STR, 'box': self.getModelFieldsDict(b)})
        except Exception, e:
            return json.dumps({'message': e.message, 'box': None})

    def getContainer(self, id, curr_user):
        ''' Returns a dictionary representation of a Container encoded in json.
        The keys in the dictionary are:
          + 'id' - The Id of the Container
          + 'title' - The title of the Container
          + 'author' - The container's author
          + 'owner_id' - Id of the owner, a User object
          + 'sharedAttributes' - A string of the name of the professor's who
             approved this container
          + 'classkey_id' - The Foreign Key to this container's class
          + 'isPrivate' - A flag indicating whether this container is private
             or public

        *Takes*
          **id** - Id of the Container to return

        *Returns*
          A json string representing the Container
        '''
        try:
            cn = Container.objects.get(pk=id)
            cndict = self.getModelFieldsDict(cn)
            if cn.sharedAttributes != None:
                cndict['sharedAttributes'] = self.getModelFieldsDict(cn.sharedAttributes)
            cndict['isUpdatable'] = (cn.owner == curr_user)
            return json.dumps({'message': DataController.SUCCESS_STR, 'container': cndict})
        except Exception, e:
            return json.dumps({'message': e.message, 'container': None})

    def getClass(self, id):
        ''' Returns a dictionary representation of a Class encoded in json.
        The keys in the dictionary are:
          + 'id' - The Id of the Class
          + 'title' - The front facing term of the Class

        *Takes*
          **id** - Id of the Class to return

        *Returns*
          A json string representing the Class
        '''
        try:
            cls = Class.objects.get(pk=id)
            return json.dumps({'message': DataController.SUCCESS_STR, 'class': self.getModelFieldsDict(cls)})
        except Exception, e:
            return json.dumps({'message': e.message, 'class': None})


    # ----- get*List Methods ---------------------------------

    def getBoxList(self, containerId):
        ''' Gets the list of boxes, with titles and id's, under a given container.
        The useful keys in the dictionary:
          + 'id' - The id of the Box
          + 'title' - The title of the Box

        *Takes*
          **containerId** - Id of the container to get the boxes from

        *Returns*
          A json string representing the list of boxes
        '''
        try:
            qs = Container.objects.get(pk=containerId).box_set.all()
            boxList = []
            for box in qs:
                boxList.append(self.getModelFieldsDict(box))
            return json.dumps({'message': DataController.SUCCESS_STR, 'list': boxList})
        except Exception, e:
            return json.dumps({'message': e.message, 'list': None})

    def getContainerList(self, classId, curr_user):
        ''' Gets the list of containers, with titles and id's, under a given class.
        The useful keys in the dictionary:
          + 'id' - The id of the Container
          + 'title' - The title of the Container

        *Takes*
          **classId** - Id of the class to get the containers from

        *Returns*
          A json string representing the list of containers
        '''
        try:
            qs = Container.objects.filter(classes__Id=classId, owner=curr_user)
            cntList = []
            for cnt in qs:
                cntList.append(self.getModelFieldsDict(cnt))
            return json.dumps({'message': DataController.SUCCESS_STR, 'list': cntList})
        except Exception, e:
            return json.dumps({'message': e.message, 'list': None})

    def getClassList(self, curr_user):
        ''' Gets the list of classes, with titles and id's, associated with a given user.
        The useful keys in the dictionary:
          + 'id' - The id of the class
          + 'title' - The title of the class

        *Takes*
          **curr_user** - The current user. *MUST* be authenticated.

        *Returns*
          A json string representing the list of classes
        '''
        try:
            qs = Class.objects.filter(user=curr_user).exclude(title=DataController.DEFAULT_TITLE)
            clsList = []
            for cls in qs:
                clsList.append(self.getModelFieldsDict(cls))
            return json.dumps({'message': DataController.SUCCESS_STR, 'list': clsList})
        except Exception, e:
            return json.dumps({'message': e.message, 'list': None})

    def getLabelList(self, curr_user):
        ''' Gets the list of labels, with names and id's, associated with a given user.
        The useful keys in the dictionary:
          + 'id' - The id of the label
          + 'name' - The name of the label

        *Takes*
          **curr_user** - The current user. *MUST* be authenticated.

        *Returns*
          A json string representing the list of labels
        '''
        try:
            q = Q(userKey=curr_user) | Q(userKey=None)
            qs = Label.objects.filter(q)
            labelList = []
            for label in qs:
                labelList.append(self.getModelFieldsDict(label))
            return json.dumps({'message': DataController.SUCCESS_STR, 'list': labelList})
        except Exception, e:
            return json.dumps({'message': e.message, 'list': None})

    def getTagList(self):
        ''' Gets the list of all the Tags that exist. This list only contains
        the text of the tag.

        *Returns*
          A json encoded list of Tags
        '''
        try:
            qs = Tag.objects.all()
            taglist = []
            for tag in qs:
                taglist.append(tag.tag)
            return json.dumps({'message': DataController.SUCCESS_STR, 'list': taglist})
        except Exception, e:
            return json.dumps({'message': e.message, 'list': None})


    # ----- Delete* Methods ----------------------------------

    def deleteFlashcards(self, data):
        ''' Deletes Flashcards based on the specified id's.

        *Takes*
          **data** - A Dictionary indexed by box ids to a list of Flashcard ids
            *Example*: {boxId: [flashcardids], boxId: [flashcardIds],...}
        *Returns*
          A json string representing the success or failure of the
          delete operation
        '''
        try:
            q = Q()
            for boxid in data.keys():
                box = Box.objects.get(pk=boxid)
                for cardid in data[boxid]:
                    card = Flashcard.objects.get(pk=cardid)
                    box.flashcard_set.remove(card)
                    if len(card.boxes.all()) == 0:
                        card.delete()
                    box.save()

            return json.dumps({'deleted': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'deleted': False, 'message': e.message})

    def deleteBoxes(self, listofids):
        ''' Deletes Boxes based on the specified id's. Deletes all the Flashcards
        under these boxes as well.

        *Takes*
          **listofids** - A list of Box id's to be deleted
        *Returns*
          A json string representing the success or failure of the
          delete operation
        '''
        try:
            q = Q()
            for id in listofids:
                q = q | Q(pk=id)
            qs = Box.objects.filter(q)

            #Delete flashcards from this box, then delete this box
            for box in qs:
                fcids = []
                for fc in box.flashcard_set.all():
                    fcids.append(fc.Id)
                result = json.loads(self.deleteFlashcards({box.Id: fcids}))
                if result['deleted']:
                    box.delete()
                else:
                    raise Exception(result['message'])

            return json.dumps({'deleted': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'deleted': False, 'message': e.message})

    def deleteContainers(self, listofids, curr_user):
        ''' Deletes Containers based on the specified id's. Deletes all the boxes
        under this Container as well.

        *Takes*
          **listofids** - A list of Container id's to be deleted
        *Returns*
          A json string representing the success or failure of the
          delete operation
        '''
        try:
            q = Q()
            for id in listofids:
                q = q | Q(pk=id)
            qs = Container.objects.filter(q)
            #pdb.set_trace()
            #Delete the boxes in each container, then delete the container
            for cnt in qs:
                # If the user is deleting a container they aren't the owner of.
                if curr_user != cnt.owner:
                    for cls in cnt.classes.all():
                        if cls.user == curr_user:
                            cnt.classes.remove(cls)

                else:
                    #Add this container to all the other containers that
                    #had downloaded with auto updates turned on
                    for cls in cnt.classes.all():
                        if cls.user != cnt.owner:
                            self.addContainerToMyCards(cnt.Id, cls.Id, False)

                    boxids = []
                    for box in cnt.box_set.all():
                        boxids.append(box.Id)
                    result = json.loads(self.deleteBoxes(boxids))
                    if (result['deleted']):
                        if cnt.sharedAttributes != None:
                            cnt.sharedAttributes.delete()
                        cnt.delete()
                    else:
                        raise Exception(result['message'])

            return json.dumps({'deleted': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'deleted': False, 'message': e.message})


    def deleteClasses(self, listofids):
        ''' Deletes Classes based on the specified id's. Deletes all the Containers
        under this class as well.

        *Takes*
          **listofids** - A list of Class id's to be deleted
        *Returns*
          A json string representing the success or failure of the
          delete operation
        '''
        try:
            q = Q()
            for id in listofids:
                q = q | Q(pk=id)
            qs = Class.objects.filter(q)

            #Delete all containers under this class, then delete the class
            for cls in qs:
                cntids = [cnt.Id for cnt in cls.container_set.all()]
                result = json.loads(self.deleteContainers(cntids, cls.user))
                if result['deleted']:
                    cls.delete()
                else:
                    raise Exception(result['message'])

            return json.dumps({'deleted': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'deleted': False, 'message': e.message})


    # ----- update* methods -------------------------
    def updateFlashcard(self, data, curr_user):
        ''' Updates a flashcard in the database. If these cards are shared and shouldn't
        be updated for any of the shared instances, a new flashcard will be made.

        This function takes a dictionary that holds the values of the flashcard.
        Recognized dictionary keys are:
            + 'cardid' - Id of the card to be updated
            + 'boxId' - Id of the box this card is being updated from
            + 'term' - The flashcard's term/front side
            + 'defaultSideLabelId' - Id of the label that will be used to identify the default side.
            + 'otherSides' - A list of dictionaries describing the additional sides (Optional)
               Each side dictionary should be of the following form:
                 {'type': {text|image|audio|video}, 'labelId': <labelId>, 'data': <data based on type>}

        *Takes*
          **data** - A json string representing a dictionary that describes the updates to
          the flashcard.

          **curr_user** - The current user.
        *Returns*
          A json string declaring success or failure
        '''
        try:
            keys = ["cardId", "term", "defaultSideLabelId", "otherSides"]
            if keys[0] in data:
                flashcard = Flashcard.objects.get(pk=data[keys[0]])
            else:
                raise Exception("No card id was given.")

            if len(flashcard.boxes.all()) > 1:
                #This card is referenced by multiple sets of cards.
                #Change this card for just the boxId given. That is, create a
                #new flashcard for that box and leave it for the others.
                flashcard.boxes.remove(data['boxId'])
                return self.addFlashcard(data, curr_user)


            #Update basic flashcard fields from dictionary data
            if keys[1] in data:
                flashcard.term = data[keys[1]]
            if keys[2] in data:
                flashcard.defaultSideLabel = Label.objects.get(pk=data[keys[2]])
            flashcard.save()

            #Update the multiple sides of the flashcard
            if keys[3] in data:
                sides = data[keys[3]]
                for side in sides:
                    if side['type'] == "text":
                        qs = TextSide.objects.filter(labelKey__Id=side['labelId'], flashcardKey=flashcard)
                        if qs.exists():
                            qs.update(text=side['data'])
                        else:
                            label = Label.objects.get(pk=side['labelId'])
                            TextSide.objects.create(labelKey=label, text=side['data'], flashcardKey=flashcard)

            return json.dumps({"updated": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'updated': False, 'message': e.message})

    def updateBox(self, data):
        ''' Updates a box in the database

        This function takes a dictionary that holds the values of the box.
        Recognized dictionary keys are:
            + 'boxId' - Id of the box
            + 'title' - The title of the box (Required)

        If the title isn't defined, the updates to the box won't be saved to the
        database and will return a message notifying of such.

        *Takes*
          **data** - A json string representing a dictionary that describes the updates to the box.
        *Returns*
          A json string declaring success or failure
        '''
        try:

            keys = ["boxId", "title"]
            if not keys[0] in data:
                raise Exception("No 'boxId' was defined")
            if not keys[1] in data:
                raise Exception("No 'title' is defined for this box")

            # Edit the box from dictionary data
            Box.objects.filter(pk=data[keys[0]]).update(title=data[keys[1]])

            return json.dumps({"updated": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'updated': False, 'message': e.message})

    def updateContainer(self, data, curr_user):
        ''' Updates a container in the database.

        This function takes a dictionary that holds the values of the box.
        Recognized dictionary keys are:
            + 'containerId' - Id of the Container
            + 'title' - The title of the box (Required)

        If the title isn't defined, the container updates won't be saved to the
        database and will return a message notifying of such.

        *Takes*
          **data** - A json string representing a dictionary that describes the updates to the container
        *Returns*
          A json string declaring success or failure
        '''
        try:
            keys = ['containerId', 'title']
            if not keys[0] in data:
                raise Exception("No 'containerId' was defined.")
            if not keys[1] in data:
                raise Exception("No 'title' is defined for this container")

            # Edit container from dictionary data
            rows = Container.objects.filter(pk=data[keys[0]],owner=curr_user).update(title=data[keys[1]])
            if rows == 0:
                raise Exception("You are not the owner of this container!")

            return json.dumps({"updated": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'updated': False, 'message': e.message})

    def updateClass(self, data):
        ''' Updates a class in the database.

        This function takes a dictionary that holds the values of the class.
        Recognized dictionary keys are:
            + 'classId' - Id of the class
            + 'title' - The title of the class (Required)

        If the title isn't defined, the class won't be updated and a message
        will be returned notifying of such.

        *Takes*
          **data** - A json string representing a dictionary that describes the updates to the class.
        *Returns*
          A json string declaring success or failure
        '''
        try:

            keys = ["classId", "title"]
            if not keys[0] in data:
                raise Exception("No 'classId' was defined.")
            if not keys[1] in data:
                raise Exception("No 'title' is defined for this Class")
            Class.objects.filter(pk=data[keys[0]]).update(title=data[keys[1]])

            return json.dumps({"updated": True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'updated': False, 'message': e.message})


    # ----- Move* methods -------------------------
    def moveFlashcards(self, cardIds, boxId):
        ''' Moves a set of flashcards from one box to another.

        *Takes*
          **cardIds** - A list of the flashcard ids

          **boxId** - Id of the box to move the flashcards to.

        *Returns*
          A json string representing whether the move operation succeded or not.
        '''
        try:
            toBox = Box.objects.get(pk=boxId)
            q = Q()
            for id in cardIds:
                q = q | Q(pk=id)
            qs = Flashcard.objects.filter(q)
            for card in qs:
                card.boxes.clear()
                card.boxes.add(toBox)

            return json.dumps({'moved': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'moved': False, 'message': e.message})

    def moveBoxes(self, boxIds, containerId):
        ''' Moves a set of boxes from one box to another.

        *Takes*
          **boxIds** - A list of the flashcard ids

          **containerId** - Id of the box to move the flashcards to.

        *Returns*
          A json string representing whether the move operation succeded or not.
        '''
        try:
            toContainer = Container.objects.get(pk=containerId)
            q = Q()
            for id in boxIds:
                q = q | Q(pk=id)
            qs = Box.objects.filter(q)
            for box in qs:
                box.containers.clear()
                box.containers.add(toContainer)

            return json.dumps({'moved': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'moved': False, 'message': e.message})


    #----- Share Methods -------------------------------
    def shareContainer(self, containerId, tagnamelist, user):
        '''Shares a container. Specifically, it changes the Container from
        private to public.

        *Takes*
          **containerId** - Id of the container to share.
        *Returns*
          A json string representing whether the move operation succeded or not.
        '''
        try:
            container = Container.objects.get(pk=containerId)
            if (container.owner != user):
                raise Exception("This container is receiving Automatic updates and can't be shared.")

            sharedAttrs = SharedAttributes(author=user.get_full_name())
            sharedAttrs.save()
            container.sharedAttributes = sharedAttrs
            container.save()

            container.isPrivate = False
            container.save()

            #Add tags
            for tagname in tagnamelist:
                if tagname != "":
                    if Tag.objects.filter(tag__iexact=tagname).exists():
                        tag = Tag.objects.get(tag__iexact=tagname)
                    else:
                        tag = Tag.objects.create(tag=tagname)
                    tag.containers.add(container)
                    tag.save()

            return json.dumps({'shared': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'shared': False, 'message': e.message})

    def unshareContainer(self, containerId):
        '''Unshares a container. Specifically, it changes the Container from
        public to private.

        *Takes*
          **containerId** - Id of the container to unshare.
        *Returns*
          A json string representing whether the move operation succeded or not.
        '''
        try:
            container = Container.objects.get(pk=containerId)

            #Remove the tags and shared attributes
            container.tag_set.clear()
            sharedattr = container.sharedAttributes
            container.sharedAttributes = None
            container.save()
            sharedattr.delete()

            #Add this container to all the other containers that
            #had downloaded with auto updates turned on
            for cls in container.classes.all():
                if cls.user != container.owner:
                    container.classes.remove(cls)
                    self.addContainerToMyCards(container.Id, cls.Id, False)

            #Finally make the container to private (unshared)
            container.isPrivate = True
            container.save()
            return json.dumps({'unshared': True, 'message': DataController.SUCCESS_STR})
        except Exception, e:
            return json.dumps({'unshared': False, 'message': e.message})
    # ---------- Moodle connection methods ------------------------

    def connectToMoodle(self, function, params):
        ''' Connects to a moodle server and calls the given function with the
        given parameters. (Right now this is only the katie-test server, but
        will be updated to be variable)

        *Takes*
          **function** - Name of the function to call on the moodle server

          **params** - A dictionary of parameters to pass to the function

        *Returns*
          The json encoded response data from the moodle server
        '''
        #Will have to store tokens and domain names in database
        #and associate them with a certain email.
        token = "f36f30decbac7ca1bbde9fc940cd2b02"
        domainname = "https://katie-test.luther.edu/moodlesenior/"

        serverurl = domainname + 'webservice/rest/server.php'

        postdata.update({'moodlewsrestformat':'json','wstoken':token,'wsfunction':function})

        data = urllib.urlencode(postdata)
        req = urllib2.Request(serverurl, data)

        resp = urllib2.urlopen(req)
        return resp.read()


    def getUserEnrolledCourses(self, curr_user):
        ''' Gets the courses a user is enrolled in on a moodle instance.
        (Right now, this only works for katie-test.)

        *Takes*
          **curr_user** - The current user

        *Returns*
          A json encoded list of courses
        '''
        try:
            userbyemailfunc = 'local_epicstudy_get_user_by_email'
            enrolledcoursesfunc = 'core_enrol_get_users_courses'

            params = {'useremail':curr_user.email}
            userid = json.loads(connectToMoodle(userbyemailfunc, params))

            params = {'userid':userid}
            courses = json.loads(connectToMoodle(enrolledcoursesfunc, params))
            return json.dumps({'message':DataController.SUCCESS_STR, 'courses':courses})
        except Exception,e:
            return json.dumps({'message': e.message, 'courses': None})

    def getParticipantsFromCourse(self, courseid):
        '''Get the participants of a moodle course.
        (Right now this only works for katie-test.)

        *Takes*
          **courseid** - The id of the course to get the participants from.

        *Returns*
          A json encoded list of users (participants).
        '''
        try:
            participantsfunc = 'core_enrol_get_enrolled_users'
            params = {'courseid':courseid}
            userid = json.loads(connectToMoodle(participantsfunc, params))
            return json.dumps({'message':DataController.SUCCESS_STR, 'userid':userid})
        except Exception,e:
            return json.dumps({'message': e.message, 'userid': None})
