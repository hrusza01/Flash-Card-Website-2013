from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from audiofield.fields import AudioField
from videothumbs.fields import VideoThumbnailField
import os.path



# Create your models here.

class Class(models.Model):
	Id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User, null=True)

	def __unicode__(self):
        	return self.title
	def __str__(self):
		return self.title
	
	class Meta:
		verbose_name_plural = "Classes"
	
class SharedAttributes(models.Model):
	Id = models.AutoField(primary_key=True)
	publicationDate = models.DateTimeField(default=timezone.now())
	rating = models.IntegerField(null=True)
	author = models.CharField(max_length=200, blank=False)
	professorApproved = models.BooleanField(default=False)
	whichProfessors = models.CharField(max_length=200, blank=True)
	
	def __unicode__(self):
		return self.author
	def __str__(self):
		return self.author
	
	class Meta:
		verbose_name_plural = "Shared Attributes"	

class Container(models.Model):
	Id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=200)
	classes = models.ManyToManyField(Class, null=True)
        isPrivate = models.BooleanField(default=True)
	owner = models.ForeignKey(User, null=True)
	sharedAttributes = models.OneToOneField(SharedAttributes, null=True)
	#BoxInteraction

	def __unicode__(self):
        	return self.title
	def __str__(self):
		return self.title
	class Meta:
		verbose_name_plural = "Containers"

class Tag(models.Model):
	Id = models.AutoField(primary_key=True)
	tag = models.CharField(max_length=200)
	containers = models.ManyToManyField(Container, null=True)

	def __unicode__(self):
        	return self.tag
	def __str__(self):
		return self.tag	
	class Meta:
		verbose_name_plural = "Tags"


#class BoxPlan(models.Model):

class Box(models.Model):
	Id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=200)
	containers = models.ManyToManyField(Container, null=True)
	#StudyPlan

	def __unicode__(self):
        	return self.title
	def __str__(self):
		return self.title
	class Meta:
		verbose_name_plural = "Boxes"
	
class Label(models.Model):
	Id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	userKey = models.ForeignKey(User, null=True)
	
	def __unicode__(self):
        	return self.name	


class Flashcard(models.Model):
	Id = models.AutoField(primary_key=True)
	term = models.CharField(max_length=200)
	defaultSideLabel = models.ForeignKey(Label, null=True)
	boxes = models.ManyToManyField(Box, null=True)

	def __unicode__(self):
        	return self.term
	
class TextSide(models.Model):
	Id = models.AutoField(primary_key=True)
	text = models.CharField(max_length=200)
	flashcardKey = models.ForeignKey(Flashcard, null=True)
	labelKey = models.ForeignKey(Label, null=True)
	
	def __unicode__(self):
        	return self.text	

class ImageSide(models.Model):
	Id = models.AutoField(primary_key=True)
	image = models.ImageField(upload_to='images/')
	flashcardKey = models.ForeignKey(Flashcard, null=True)
	labelKey = models.ForeignKey(Label, null=True)	

class AudioSide(models.Model):
	Id = models.AutoField(primary_key=True)
	#audio_file = AudioField(upload_to='audio', blank=True,
                        #ext_whitelist=(".mp3", ".wav", ".ogg"),
                        #help_text=("Allowed type - .mp3, .wav, .ogg"))
	flashcardKey = models.ForeignKey(Flashcard, null=True)
	labelKey = models.ForeignKey(Label, null=True)	

class VideoSide(models.Model):
	Id = models.AutoField(primary_key=True)
	#video = VideoThumbnailField(upload_to='videos', sizes=((80,80),))
	flashcardKey = models.ForeignKey(Flashcard, null=True)
	labelKey = models.ForeignKey(Label, null=True)	
