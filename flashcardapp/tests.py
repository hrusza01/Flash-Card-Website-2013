from django.utils import simplejson as json
#from django.utils import unittest
from django.test import TestCase
from flashcardapp.datacontroller import DataController
from django.contrib.auth.models import User
from flashcardapp.models import *
import pdb

class DataControllerTest(TestCase):
    fixtures = ['test-data2.json']

    def setUp(self):
        # Create Database objects here
        self.superuser = User.objects.get(pk=1)
        self.user = User.objects.get(pk=2)

    def tearDown(self):
        # Remove Database objects here (This is done by the test framework!!)
        pass


    # ------ Test the add* methods -----------------

    def test_addFlashcard(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Creates a new json string representing the data of a flashcard based
           on the specifications of the DataController's addFlashcard method.
        3. Passes the json string to the DataController's addFlashcard method
           and gets the result of the method (response).
        4. Asserts that there is a 'saved' key in the response.
        5. Asserts that the value of 'saved' is True.
        """
        dc = DataController()
        fcTerm = "Term"
        fcDefaultSideLabelId = 1
        boxId = 1
        otherSides = [{"type":"text", "labelId":1, "data":"Definition"}, {"type":"text", "labelId":2, "data":"Translation"}, {"type":"text", "labelId":7, "data":"Conjugation"}]
        data = {"term":fcTerm, "defaultSideLabelId":1, "boxId":boxId, "otherSides":otherSides}
        resultStr = dc.addFlashcard(data, self.user)
        result = json.loads(resultStr)
        self.assertTrue('saved' in result)
        self.assertTrue(result['saved'], result['message'])

        #Check the association was done correctly
        box = Box.objects.get(pk=boxId)
        fc = Flashcard.objects.get(term=fcTerm)

        self.assertIn(fc, box.flashcard_set.all())
        self.assertIn(box, fc.boxes.all())

        self.assertEqual(len(fc.textside_set.all()), len(otherSides))

    def test_addBox(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Creates a new json string representing the data of a box based
           on the specifications of the DataController's addBox method.
        3. Passes the json string to the DataController's addBox method
           and gets the result of the method (response).
        4. Asserts that there is a 'saved' key in the response.
        5. Asserts that the value of 'saved' is True.
        """
        dc = DataController()
        boxTitle = "Test Box"
        cntId = 1
        data = {"title":boxTitle, "containerId":cntId}
        resultStr = dc.addBox(data)
        result = json.loads(resultStr)
        self.assertTrue('saved' in result)
        self.assertTrue(result['saved'], result['message'])

        #Check the association was done correctly
        box = Box.objects.get(title=boxTitle)
        cnt = Container.objects.get(pk=cntId)

        self.assertIn(cnt, box.containers.all())
        self.assertIn(box, cnt.box_set.all())

    def test_addContainer(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Creates a new json string representing the data of a container based
           on the specifications of the DataController's addContainer method.
        3. Passes the json string to the DataController's addContainer method
           and gets the result of the method (response).
        4. Asserts that there is a 'saved' key in the response.
        5. Asserts that the value of 'saved' is True.
        """
        dc = DataController()
        cName = "Test Container"
        clsKey = 1
        numofcontainers = 4
        data = {"title":cName, "classId":clsKey}
        resultStr = dc.addContainer(data, self.user)
        result = json.loads(resultStr)
        self.assertTrue('saved' in result)
        self.assertTrue(result['saved'], result['message'])

        #Check that the associatation was actually made
        clist = Container.objects.filter(classes__Id=clsKey)
        self.assertEqual(len(clist), numofcontainers)

        cls = Class.objects.get(pk=clsKey)
        cnt = Container.objects.get(title=cName)

        self.assertIn(cls, cnt.classes.all())
        self.assertTrue(cnt in cls.container_set.all(), "The container is not associated with the class.")


    def test_addClass(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Creates a new json string representing the data of a class based
           on the specifications of the DataController's addClass method.
        3. Passes the json string to the DataController's addClass method
           and gets the result of the method (response).
        4. Asserts that there is a 'saved' key in the response.
        5. Asserts that the value of 'saved' is True.
        """
        dc = DataController()
        clsTitle = "New Class"
        data = {"title":clsTitle}
        resultStr = dc.addClass(data, self.user)
        result = json.loads(resultStr)
        self.assertTrue('saved' in result)
        self.assertTrue(result['saved'], result['message'])

        #Check that the associatation was actually made
        cls = Class.objects.get(title=clsTitle)

        self.assertEquals(cls.user, self.user)
        self.assertIn(cls, self.user.class_set.all())


    # ------- Test the other random methods ------------------------


    def test_getClasses(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Attempts to retreive all the classes from the DataController
        3. Asserts the number of classes is 5
        4. Asserts the title of the class is equal to self.className
        """
        dc = DataController()
        numOfClasses = 5
        clsName = "CS 150"
        #clsName = "German 101"
        classes = dc.getClasses(self.user)
        self.assertEqual(len(classes), numOfClasses)
        self.assertEqual(classes[0].title, clsName)

    def test_getFlashcardsFromBoxes(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Attempts to retreive the json representation of all Flashcard from
           the a list of boxes
        3. Asserts the number of flashcards is 2
        4. Asserts the Flashcard term is "Guten Tag"
        5. Asserts the Flashcard defintion is "Good Day"
        """
        dc = DataController()
        numOfCards = 5
        boxes = [1,13]
        translationLabel = Label.objects.get(name="Translation")
        data = dc.getFlashcardsFromBoxes(boxes)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        cards = data['cards']
        self.assertEqual(len(cards), numOfCards)
        self.assertEqual(cards[0]['term'], "Der Bauch")
        self.assertEqual(cards[0]['defaultSideLabel_id'], translationLabel.Id)
        textside = TextSide.objects.get(flashcardKey=cards[0]['id'], labelKey=translationLabel)
        self.assertEqual(textside.text, "The Stomach")

        self.assertEqual(cards[1]['term'], "Das Wetter")
        self.assertEqual(cards[1]['defaultSideLabel_id'], translationLabel.Id)
        textside = TextSide.objects.get(flashcardKey=cards[1]['id'], labelKey=translationLabel)
        self.assertEqual(textside.text, "The Weather")

        self.assertEqual(cards[2]['term'], "Das Essen")
        self.assertEqual(cards[2]['defaultSideLabel_id'], translationLabel.Id)
        textside = TextSide.objects.get(flashcardKey=cards[2]['id'], labelKey=translationLabel)
        self.assertEqual(textside.text, "The Food")

    def test_getContainersWithBoxesFromClass(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Attempts to retrieve a json string that represents the all the
           containers with their boxes that are associated with the given class
        3. Validates and decodes the json returned
        4. Asserts their is only one container
        5. Asserts the title of the Container is self.containerName
        6. Asserts the number of boxes is 1
        7. Asserts the title of of the box is self.boxName
        """
        clsId = 1
        cntName = "Verbs"
        boxName = "Day 1"
        numOfContainers = 3
        numOfBoxes = 3
        dc = DataController()
        jsonStr = dc.getContainersWithBoxesFromClass(clsId)
        data = json.loads(jsonStr)
        self.assertTrue(data['message'] == DataController.SUCCESS_STR, data['message'])
        containers = data['containers']
        self.assertEqual(len(containers), numOfContainers)
        self.assertEqual(containers[0]["title"], cntName)
        boxes = containers[0]['boxes']
        self.assertEqual(len(boxes), numOfBoxes)
        self.assertEqual(boxes[0]['title'], boxName)

    def test_getBoxesAndFlashcardFromContainer(self):
        """
        Docstring goes here
        """
        containerid = 2
        numofboxes = 2
        numoffcs = 3
        dc = DataController()
        data = json.loads(dc.getBoxesAndFlashcardsFromContainer(2))
        self.assertEqual(data['message'], DataController.SUCCESS_STR)

        boxes = data['data']
        self.assertIsNotNone(boxes)
        self.assertEqual(len(boxes), numofboxes)

        for box in boxes:
            self.assertEqual(len(box['flashcards']), numoffcs)

    def test_getBoxesFromContainer(self):
        """
        Docstring goes here
        """
        containerid = 3
        numofboxes = 3
        dc = DataController()
        data = json.loads(dc.getBoxesFromContainer(containerid))
        self.assertEqual(data['message'], DataController.SUCCESS_STR)

        boxes = data['boxes']
        self.assertIsNotNone(boxes)
        self.assertEqual(len(boxes), numofboxes)

    def test_getContainersFromClass(self):
        """
        Docstring goes here
        """
        classid = 1
        numofcontainers = 3
        dc = DataController()
        data = json.loads(dc.getContainersFromClass(classid))
        self.assertEqual(data['message'], DataController.SUCCESS_STR)

        containers = data['containers']
        self.assertIsNotNone(containers)
        self.assertEqual(len(containers), numofcontainers)

    def test_addDefaultClass(self):
        """
        Docstring goes here
        """
        defaulttitle = "__default__"
        dc = DataController()
        response = json.loads(dc.addDefaultClass(self.superuser))
        self.assertTrue(response['saved'], response['message'])
        self.assertEqual(response['message'], DataController.SUCCESS_STR)

        cls_set = self.superuser.class_set
        titles = []
        for cls in cls_set.all():
            titles.append(cls.title)
        self.assertIn(defaulttitle, titles)

        defaultClass = cls_set.get(title=defaulttitle)
        self.assertEqual(len(defaultClass.container_set.all()), 1)
        self.assertEqual(defaultClass.container_set.all()[0].title, defaulttitle)
        self.assertEqual(len(defaultClass.container_set.all()[0].box_set.all()), 1)
        self.assertEqual(defaultClass.container_set.all()[0].box_set.all()[0].title, defaulttitle)


    def test_addToDefaultClass(self):
        """
        Docstring goes here
        """
        defaulttitle = "__default__"
        fcterm = "term"
        fcdsl = Label.objects.get(name="Definition")
        dc = DataController()
        flashcard = Flashcard.objects.create(term=fcterm, defaultSideLabel=fcdsl)
        definitionside = TextSide.objects.create(text="Definition", labelKey=fcdsl, flashcardKey=flashcard)

        dc.addToDefaultClass(flashcard, self.user)

        defaultcls = self.user.class_set.get(title=defaulttitle)
        defaultcnt = defaultcls.container_set.get(title=defaulttitle)
        defaultbox = defaultcnt.box_set.get(title=defaulttitle)

        self.assertEqual(len(defaultbox.flashcard_set.all()), 1)


    def test_addContainerToMyCardsWithAutoUpdates(self):
        """
        Steps this test will run:

        1.
        .
        .
        .
        ?.
        """
        cntName = "Shared Greetings"
        toClassId = 1
        fromClassId = 6
        cntToGetId = 5
        numofcontainers = 4
        dc = DataController()
        toClass = Class.objects.get(pk=toClassId)
        toCopyContainer = Container.objects.get(pk=cntToGetId)

        result = dc.addContainerToMyCards(toCopyContainer.Id, toClass.Id, True)
        data = json.loads(result)

        self.assertTrue(data['added'], data['message'])

        self.assertEqual(len(toClass.container_set.all()), numofcontainers)
        self.assertIsNotNone(toClass.container_set.get(title=cntName))

        copiedContainer = toClass.container_set.get(title=cntName)

        self.assertEqual(copiedContainer.Id, toCopyContainer.Id)
        self.assertNotEqual(copiedContainer.owner, toClass.user)
        self.assertEqual(len(copiedContainer.box_set.all()), len(toCopyContainer.box_set.all()))
        self.assertEqual(copiedContainer, toCopyContainer)
        self.assertIn(toClass, copiedContainer.classes.all())
        self.assertIn(toClass, toCopyContainer.classes.all())


    def test_addContainerToMyCardsWithoutAutoUpdates(self):
        """
        Steps this test will run:

        1.
        .
        .
        .
        ?.
        """
        cntName = "Shared Greetings"
        toClassId = 1 #'German 101' class of testuser
        fromClassId = 6 #'German 101' class of jake (superuser)
        cntToGetId = 5 #'Shared Greetings' container of jake
        numofcontainers = 4
        dc = DataController()
        toClass = Class.objects.get(pk=toClassId)
        toCopyContainer = Container.objects.get(pk=cntToGetId)
        #pdb.set_trace()
        result = dc.addContainerToMyCards(toCopyContainer.Id, toClass.Id, False)
        data = json.loads(result)

        self.assertTrue(data['added'], data['message'])

        self.assertEqual(len(toClass.container_set.all()), numofcontainers)
        self.assertIsNotNone(toClass.container_set.get(title=cntName))

        copiedContainer = toClass.container_set.get(title=cntName)

        #Make sure containers aren't the same
        self.assertNotEqual(copiedContainer, toCopyContainer)
        self.assertNotEqual(copiedContainer.Id, toCopyContainer.Id)

        #Check the owners/users of the containers/classes
        self.assertNotEqual(toCopyContainer.owner, toClass.user)
        self.assertNotEqual(copiedContainer.owner, toCopyContainer.owner)
        self.assertEqual(copiedContainer.owner, toClass.user)

        #Check the classes that the containers are related too.
        self.assertIn(toClass, copiedContainer.classes.all())
        self.assertNotIn(toClass, toCopyContainer.classes.all())

        #Make sure the privacy settings are right
        self.assertTrue(copiedContainer.isPrivate)
        self.assertFalse(toCopyContainer.isPrivate)

        #Make sure both containers have the same number of boxes
        self.assertEqual(len(copiedContainer.box_set.all()), len(toCopyContainer.box_set.all()))

        toCopyBoxes = toCopyContainer.box_set.all()
        copiedBoxes = copiedContainer.box_set.all()

        for i in range(len(copiedBoxes)):
            tcBox = toCopyBoxes[i]
            cBox = copiedBoxes[i]
            self.assertNotEqual(tcBox.Id, cBox.Id)
            self.assertEqual(tcBox.title, cBox.title)

            self.assertEqual(len(cBox.containers.all()), 1)
            self.assertEqual(len(tcBox.containers.all()), 1)

            self.assertEqual(len(tcBox.flashcard_set.all()), len(cBox.flashcard_set.all()))
            tcFlashcards = tcBox.flashcard_set.all()
            cFlashcards = cBox.flashcard_set.all()

            for j in range(len(cFlashcards)):
                tcFlashcard = tcFlashcards[j]
                cFlashcard = cFlashcards[j]

                self.assertEqual(tcFlashcard.Id, cFlashcard.Id)



    # ------ Test the get* methods ------------------

    def test_getFlashcard(self):
        """
        Steps this test will run:

        1. Create a new DataController
        2. Call the DataController's 'getFlashcard' method
        3. Validates and decodes the json returned
        4. Assert the message is the success message
        5. Assert all the keys specified by the 'getFlashcard' docstring are in
           the dictionary
        """
        keys = ['id', 'term', 'defaultSideLabel_id', 'textsides']
        dc = DataController()
        jsonStr = dc.getFlashcard(2)
        data = json.loads(jsonStr)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        fDict = data['flashcard']
        for key in keys:
            self.assertIn(key, fDict)
        textsides = fDict['textsides']
        self.assertEqual(len(textsides), 3)
        for ts in textsides:
            self.assertIn('label', ts)


    def test_getBox(self):
        """
        Steps this test will run:

        1. Create a new DataController
        2. Call the DataController's 'getBox' method
        3. Validates and decodes the json returned
        4. Assert the message is the success message
        5. Assert all the keys specified by the 'getBox' docstring are in
           the dictionary
        """
        keys = ['id', 'title']
        dc = DataController()
        jsonStr = dc.getBox(1)
        data = json.loads(jsonStr)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        fDict = data['box']
        for key in keys:
            self.assertIn(key, fDict)

    def test_getContainer(self):
        """
        Steps this test will run:

        1. Create a new DataController
        2. Call the DataController's 'getContainer' method
        3. Validates and decodes the json returned
        4. Assert the message is the success message
        5. Assert all the keys specified by the 'getContainer' docstring are in
           the dictionary
        """
        keys = ['id', 'title' , 'isPrivate', 'isUpdatable', 'sharedAttributes_id']
        dc = DataController()
        jsonStr = dc.getContainer(1, self.user)
        data = json.loads(jsonStr)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        containerDict = data['container']
        for key in keys:
            self.assertIn(key, containerDict)

    def test_getClass(self):
        """
        Steps this test will run:

        1. Create a new DataController
        2. Call the DataController's 'getClass' method
        3. Validates and decodes the json returned
        4. Assert the message is the success message
        5. Assert all the keys specified by the 'getClass' docstring are in
           the dictionary
        """
        keys = ['id', 'title']
        dc = DataController()
        jsonStr = dc.getClass(1)
        data = json.loads(jsonStr)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        fDict = data['class']
        for key in keys:
            self.assertIn(key, fDict)


    # ------ Test get*List methods ------------------

    def test_getLabelList(self):
        """
        Docstring goes here
        """
        #First, test an actual user with extra labels
        numoflabels = 13
        dc = DataController()
        jsonStr = dc.getLabelList(self.user)
        data = json.loads(jsonStr)
        self.assertTrue(data != None)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        labels = data['list']
        self.assertIsNotNone(labels)
        self.assertEqual(len(labels), numoflabels)

        #Now test a no user case. Should get back the default labels
        numoflabels = 12
        data = json.loads(dc.getLabelList(None))
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        labels = data['list']
        self.assertIsNotNone(labels)
        self.assertEqual(len(labels), numoflabels)

    def test_getBoxList(self):
        """
        Docstring goes here
        """
        containerId = 1
        numofboxes = 3
        dc = DataController()
        jsonStr = dc.getBoxList(containerId)
        data = json.loads(jsonStr)
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        boxes = data['list']
        self.assertIsNotNone(boxes)
        self.assertEqual(len(boxes), numofboxes)

    def test_getContainerList(self):
        """
        Docstring goes here
        """
        classId = 1
        numofcontainers = 3
        dc = DataController()
        jsonStr = dc.getContainerList(classId, self.user)
        data = json.loads(jsonStr)
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        containers = data['list']
        self.assertIsNotNone(containers)
        self.assertEqual(len(containers), numofcontainers)

    def test_getClassList(self):
        """
        Docstring goes here
        """
        numofclasses = 4
        dc = DataController()
        jsonStr = dc.getClassList(self.user)
        data = json.loads(jsonStr)
        self.assertIsNotNone(data)
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        classes = data['list']
        self.assertIsNotNone(classes)
        self.assertEqual(len(classes), numofclasses)

    # ------ Test delete* methods  ------------------

    def test_deleteFlashcards(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Calls the data controller method to delete flashcard 1, 2, and 19
        3. Receives and validates the returned json string
        4. Asserts the returns json says the deleted was successful
        5. Asserts the message matches DataController.SUCCESS_STR
        """
        persistingFc = Flashcard.objects.get(pk=19)
        box1 = Box.objects.get(pk=1)
        box2 = Box.objects.get(pk=8)
        numofflashcards = 2

        dc = DataController()
        jsonStr = dc.deleteFlashcards({1:[2,19], 8:[7]})
        data = json.loads(jsonStr)
        self.assertTrue(data['deleted'], data['message'])
        self.assertEqual(data['message'], DataController.SUCCESS_STR)
        self.assertEqual(len(box1.flashcard_set.all()), numofflashcards)
        self.assertEqual(len(box2.flashcard_set.all()), numofflashcards)

        with self.assertRaises(Flashcard.DoesNotExist):
            Flashcard.objects.get(pk=2)
        with self.assertRaises(Flashcard.DoesNotExist):
            Flashcard.objects.get(pk=7)

        self.assertIsNotNone(persistingFc)
        self.assertEqual(len(persistingFc.boxes.all()), 1)

    def test_deleteBoxes(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Calls the data controller method to delete box
        3. Receives and validates the returned json string
        4. Asserts the returns json says the deleted was successful
        5. Asserts the message matches DataController.SUCCESS_STR
        """
        boxids = [1,8]
        dc = DataController()
        jsonStr = dc.deleteBoxes(boxids)
        data = json.loads(jsonStr)
        self.assertTrue(data['deleted'], data['message'])
        self.assertEqual(data['message'], DataController.SUCCESS_STR)

        with self.assertRaises(Box.DoesNotExist):
            Box.objects.get(pk=boxids[0])
        with self.assertRaises(Box.DoesNotExist):
            Box.objects.get(pk=boxids[1])

    def test_deleteContainers(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Calls the data controller method to delete container 1
        3. Receives and validates the returned json string
        4. Asserts the returns json says the deleted was successful
        5. Asserts the message matches DataController.SUCCESS_STR
        """
        cntids = [1,3]
        dc = DataController()
        jsonStr = dc.deleteContainers(cntids, self.user)
        data = json.loads(jsonStr)
        self.assertTrue(data['deleted'], data['message'])
        self.assertEqual(data['message'], DataController.SUCCESS_STR)

        with self.assertRaises(Container.DoesNotExist):
            Container.objects.get(pk=cntids[0])
        with self.assertRaises(Container.DoesNotExist):
            Container.objects.get(pk=cntids[1])

    def test_deleteClasses(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Calls the data controller method to delete class 1
        3. Receives and validates the returned json string
        4. Asserts the returns json says the deleted was successful
        5. Asserts the message matches DataController.SUCCESS_STR
        """
        clsids = [2,5]
        dc = DataController()
        jsonStr = dc.deleteClasses(clsids)
        data = json.loads(jsonStr)
        self.assertTrue(data['deleted'], data['message'])
        self.assertEqual(data['message'], DataController.SUCCESS_STR)

        with self.assertRaises(Class.DoesNotExist):
            Class.objects.get(pk=clsids[0])
        with self.assertRaises(Class.DoesNotExist):
            Class.objects.get(pk=clsids[1])

    # ----- Test move* methods ----------------------

    def test_moveFlashcards(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Calls the data controller method to move flashcard 3 to box 2
        3. Receives and validates the returned json string
        4. Asserts the returns json says the card was successfully moved
        5. Asserts the message matches DataController.SUCCESS_STR
        """
        dc = DataController()
        jsonStr = dc.moveFlashcards([3], 2)
        data = json.loads(jsonStr)
        self.assertTrue(data['moved'], data['message'])
        self.assertEqual(data['message'], DataController.SUCCESS_STR)

    def test_moveBoxes(self):
        """
        Steps this test will run:

        1. Creates a new DataController
        2. Calls the data controller method to move box 2 to container 2
        3. Receives and validates the returned json string
        4. Asserts the returns json says the card was successfully moved
        5. Asserts the message matches DataController.SUCCESS_STR
        """
        dc = DataController()
        jsonStr = dc.moveFlashcards([2], 2)
        data = json.loads(jsonStr)
        self.assertTrue(data['moved'], data['message'])
        self.assertEqual(data['message'], DataController.SUCCESS_STR)


    # ------ Test update* methods -------------------

    def test_updateFlashcard(self):
        """
        Docstring goes here
        """
        numoftextsides = 3
        data = {'cardId':4, 'term':"New Term",'defaultSideLabel_id':2,\
                'otherSides': [{'labelId':8,'type':"text",'data':"None"},\
                               {'labelId':2,'type':"text",'data':"New Translation"}, \
                               {'labelId':13,'type':"text",'data':"Das Essen schmeckt mir."}]}

        dc = DataController()
        response = json.loads(dc.updateFlashcard(data, self.user))
        self.assertTrue(response['updated'], response['message'])
        self.assertEqual(response['message'], DataController.SUCCESS_STR)

        flashcard = Flashcard.objects.get(pk=data['cardId'])
        self.assertEquals(flashcard.term, data['term'])
        self.assertEquals(flashcard.defaultSideLabel.Id, data['defaultSideLabel_id'])

        self.assertEquals(len(flashcard.textside_set.all()), numoftextsides)

        for tsinfo in data['otherSides']:
            qs = flashcard.textside_set.filter(labelKey__Id=tsinfo['labelId'])
            self.assertTrue(qs.exists())
            for ts in qs:
                self.assertEqual(ts.text, tsinfo['data'])

    def test_updateBox(self):
        """
        Docstring goes here
        """
        dc = DataController()
        data = {'boxId':1, 'title':"Updated Title"}
        response = json.loads(dc.updateBox(data))

        self.assertTrue(response['updated'], response['message'])
        self.assertEqual(response['message'], DataController.SUCCESS_STR)

        self.assertEqual(Box.objects.get(pk=data['boxId']).title, data['title'])

    def test_updateContainer(self):
        """
        Docstring goes here
        """
        dc = DataController()
        data = {'containerId':3, 'title':"Updated Title"}
        response = json.loads(dc.updateContainer(data, self.user))

        self.assertTrue(response['updated'], response['message'])
        self.assertEqual(response['message'], DataController.SUCCESS_STR)

        self.assertEqual(Container.objects.get(pk=data['containerId']).title, data['title'])

    def test_updateClass(self):
        """
        Docstring goes here
        """
        dc = DataController()
        data = {'classId':1, 'title':"Updated Title"}
        response = json.loads(dc.updateClass(data))

        self.assertTrue(response['updated'], response['message'])
        self.assertEqual(response['message'], DataController.SUCCESS_STR)

        self.assertEqual(Class.objects.get(pk=data['classId']).title, data['title'])


    # ------ Test Shared methods --------------------

    def test_getSharedContainers(self):
        """
        Docstring goes here.
        """
        numofcontainers = 2
        dc = DataController()
        data = json.loads(dc.getSharedContainers())
        self.assertEquals(data['message'], DataController.SUCCESS_STR)
        containers = data['containers']
        self.assertIsNotNone(containers)
        self.assertEqual(len(containers), numofcontainers)

        for cnt in containers:
            self.assertIsNotNone(cnt['sharedAttributes'])
            self.assertTrue(len(cnt['tags']) == 2 or len(cnt['tags']) == 3, "The length of cnt['tags'] is actually: %d" % len(cnt['tags']))


    def test_shareContainer(self):
        """
        Docstring goes here.
        """
        containerid = 1
        dc = DataController()
        response = dc.shareContainer(containerid,[], self.user)
        response = json.loads(response)
        self.assertTrue(response['shared'], response['message'])
        self.assertEqual(response['message'], DataController.SUCCESS_STR)

        container = Container.objects.get(pk=containerid)
        self.assertFalse(container.isPrivate)
        self.assertIsNotNone(container.sharedAttributes)


    def test_unshareContainer(self):
        """
        Docstring goes here.
        """
        containerid = 4
        dc = DataController()
        response = dc.unshareContainer(containerid)
        response = json.loads(response)
        self.assertTrue(response['unshared'])
        self.assertEqual(response['message'], DataController.SUCCESS_STR)

        container = Container.objects.get(pk=containerid)
        self.assertTrue(container.isPrivate)
        self.assertIsNone(container.sharedAttributes)

    def test_unshareWithAutoUpdatingUsers(self):
        """
        Scenario: superuser has already shared cards
        self.user saves these cards with automatic updates.
        superuser unshares these
        self.user should now have their own set of the cards they saved.
        """
        pass