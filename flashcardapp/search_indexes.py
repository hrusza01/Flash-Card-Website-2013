import datetime
from haystack.indexes import *
from haystack import site
from flashcardapp.models import SharedAttributes, Container

#class SharedAttributesIndex(SearchIndex):
 #   text = CharField(document=True, use_template=True)
  #  publicationDate = DateTimeField(model_attr='publicationDate')
   # rating = IntegerField(model_attr='rating')
    #author = CharField(model_attr='author')
    #professorApproved = BooleanField(model_attr='professorApproved')
    #whichProfessors = CharField(model_attr='whichProfessors')

    #def index_queryset(self):
     #   return SharedAttributes.objects.filter(author__startswith='')

class ContainerIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	title = CharField(model_attr='title')

	def index_queryset(self):
		return Container.objects.filter(title__startswith='')
	
	
site.register(Container, ContainerIndex)
