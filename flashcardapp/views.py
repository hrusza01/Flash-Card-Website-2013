# Create your views here.

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context, loader
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

from flashcardapp.datacontroller import DataController
from django.utils import simplejson as json
import pdb #used for traceback/debugging
from django.contrib.auth.views import logout_then_login, logout
from epicstudy import settings


def testUser(request):
    if not request.user.is_authenticated(): #the user is an AnonymousUser
        return None
    else:
        return request.user

@ensure_csrf_cookie
def index(request):
    #load in a predefined view that exists in our mytemplates/flashcardapp folder
    t = loader.get_template('flashcardapp/homeproto.html')
    c = Context({"user":testUser(request)})
    return HttpResponse(t.render(c))

@login_required
@ensure_csrf_cookie
def study(request):
    t = loader.get_template('flashcardapp/study.html')
    dc = DataController()
    classes = dc.getClasses(request.user)
    c = Context({"classlist": classes, "user":testUser(request)}) #variable name that is referenced in the view
    return HttpResponse(t.render(c))

@login_required
@ensure_csrf_cookie
def createcard(request):
    t = loader.get_template('flashcardapp/createFlashCard.html')
    c = Context({"user":testUser(request)})
    return HttpResponse(t.render(c))

@login_required
@ensure_csrf_cookie
def mycards(request):
    t = loader.get_template('flashcardapp/mycards.html')
    dc = DataController()
    classes = dc.getClasses(request.user)
    c = Context({"classlist": classes, "user":testUser(request)}) #variable name that is referenced in the view
    return HttpResponse(t.render(c))

@login_required
@ensure_csrf_cookie
def studyplan(request):
    t = loader.get_template('flashcardapp/studyPlan.html')
    c = Context({"user":testUser(request)})
    return HttpResponse(t.render(c))

@ensure_csrf_cookie
def browsecard(request):
    t = loader.get_template('flashcardapp/browsecard.html')
    dc = DataController()
    shared = dc.getSharedContainers()
    c = Context({"user":testUser(request), "shared":shared})
    return HttpResponse(t.render(c))

@login_required
@ensure_csrf_cookie
def cardviewer(request):
    boxesString = request.GET.get('boxes')
    boxesList = boxesString.split("_")
    numberofcards = request.GET.get("numberofcards");
    if numberofcards != None:
        numberofcards = int(numberofcards)
    testme = request.GET.get("testme")
    #pdb.set_trace()
    t = loader.get_template('flashcardapp/cardviewer.html')
    dc = DataController()
    #Check to see if we are in regular study mode, or test mode
    if (testme):
        cardsDict = dc.getRandomFlashcardsFromBoxes(boxesList,numberofcards)
    else:
        cardsDict = dc.getFlashcardsFromBoxes(boxesList)

    if cardsDict['message'] == DataController.SUCCESS_STR:
        cards = json.dumps(cardsDict['cards'])
        c = Context({"cards":cards,"user":testUser(request)})
        return HttpResponse(t.render(c))
    else:
        return HttpResponse(t.render(Context({"user":testUser(request)})))

def newuserlogin(request):
    #dc = DataController()
    #if testUser(request):
        #dc.addDefaultClass(request.user)
    return redirect(settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL)

def login(request):
    t = loader.get_template('flashcardapp/login.html')
    c = Context()
    return HttpResponse(t.render(c))

@login_required
def logout_view(request):
    logout(request, '/epicstudy')
