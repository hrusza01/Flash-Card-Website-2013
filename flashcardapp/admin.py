from django.contrib import admin
from django.contrib.auth.models import User
from flashcardapp.models import Flashcard, Class, Container, SharedAttributes, Tag, Box, Label, TextSide, ImageSide, AudioSide, VideoSide

class LabelInline(admin.TabularInline):
	model = Label

class LabelAdmin(admin.ModelAdmin):
	pass

class VideoSideInline(admin.TabularInline):
	model = VideoSide

class VideoSideAdmin(admin.ModelAdmin):
	pass

class AudioSideInline(admin.TabularInline):
	model = AudioSide

class AudioSideAdmin(admin.ModelAdmin):
	pass

class ImageSideInline(admin.TabularInline):
	model = ImageSide

class ImageSideAdmin(admin.ModelAdmin):
	pass

class TextSideInline(admin.TabularInline):
	model = TextSide

class TextSideAdmin(admin.ModelAdmin):
	pass

class FlashcardInline(admin.TabularInline):
        model = Flashcard.boxes.through

class FlashcardAdmin(admin.ModelAdmin):
	inlines = [FlashcardInline, TextSideInline, ImageSideInline, AudioSideInline,]
        exclude = ('boxes',)
	
class BoxInline(admin.TabularInline):
	model = Box.containers.through

class BoxAdmin(admin.ModelAdmin):
	inlines = [FlashcardInline, BoxInline,]
	exclude = ('containers',)

class TagInline(admin.TabularInline):
	model = Tag.containers.through

class TagAdmin(admin.ModelAdmin):
	pass

class SharedAttributesrAdmin(admin.ModelAdmin):
	inlines = [BoxInline, TagInline]

class ContainerInline(admin.TabularInline):
	model = Container.classes.through

class ContainerAdmin(admin.ModelAdmin):
	inlines = [BoxInline, TagInline]

class ClassInline(admin.TabularInline):
	model = Class

class ClassAdmin(admin.ModelAdmin):
	inlines = [ContainerInline,]
	#exclude = ('user',)

#class UserAdmin(admin.ModelAdmin):
	#inlines = [ClassInline,]


admin.site.register(VideoSide, VideoSideAdmin)
admin.site.register(AudioSide, AudioSideAdmin)
admin.site.register(ImageSide, ImageSideAdmin)
admin.site.register(TextSide, TextSideAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Flashcard, FlashcardAdmin)
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(SharedAttributes)
admin.site.register(Container, ContainerAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Box, BoxAdmin)
#admin.site.register(UserToClass)
#admin.site.register(ContainerToBox)
#admin.site.register(BoxToFlashcard)
