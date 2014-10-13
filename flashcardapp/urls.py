from django.conf.urls import patterns, include, url
from epicstudy import settings


urlpatterns = patterns('',
    url(r'^$','flashcardapp.views.index',name='index'),
    url('study.html', 'flashcardapp.views.study', name='study'),
    url('createcard.html', 'flashcardapp.views.createcard', name='create'),
    url('mycards.html', 'flashcardapp.views.mycards', name='mycards'),
    url('studyplan.html','flashcardapp.views.studyplan', name='stydyplan'),
    url('cardviewer.html','flashcardapp.views.cardviewer', name='cardviewer'),
    url('browsecard.html','flashcardapp.views.browsecard', name='browsecard'),
    #url('login.html','flashcardapp.views.login', name='login'),
    #url('logout.html','flashcardapp.views.logout_then_login', name='logout'),
    url('newuserlogin/','flashcardapp.views.newuserlogin', name='newuserlogin'),
)
