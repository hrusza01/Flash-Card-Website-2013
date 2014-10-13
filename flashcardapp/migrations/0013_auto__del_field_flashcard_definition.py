# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Flashcard.definition'
        db.delete_column('flashcardapp_flashcard', 'definition')


    def backwards(self, orm):
        # Adding field 'Flashcard.definition'
        db.add_column('flashcardapp_flashcard', 'definition',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flashcardapp.audioside': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'AudioSide'},
            'flashcardKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Flashcard']", 'null': 'True'}),
            'labelKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Label']", 'null': 'True'})
        },
        'flashcardapp.box': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Box'},
            'containers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['flashcardapp.Container']", 'null': 'True', 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'flashcardapp.class': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Class'},
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'flashcardapp.container': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Container'},
            'classes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['flashcardapp.Class']", 'null': 'True', 'symmetrical': 'False'}),
            'isPrivate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'sharedAttributes': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['flashcardapp.SharedAttributes']", 'unique': 'True', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'flashcardapp.flashcard': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Flashcard'},
            'boxes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['flashcardapp.Box']", 'null': 'True', 'symmetrical': 'False'}),
            'defaultSideLabel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Label']", 'null': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'flashcardapp.imageside': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'ImageSide'},
            'flashcardKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Flashcard']", 'null': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'labelKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Label']", 'null': 'True'})
        },
        'flashcardapp.label': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Label'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'flashcardapp.sharedattributes': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'SharedAttributes'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'professorApproved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'publicationDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 14, 0, 0)'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'whichProfessors': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'flashcardapp.tag': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Tag'},
            'containers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['flashcardapp.Container']", 'null': 'True', 'symmetrical': 'False'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'flashcardapp.textside': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'TextSide'},
            'flashcardKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Flashcard']", 'null': 'True'}),
            'labelKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Label']", 'null': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'flashcardapp.videoside': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'VideoSide'},
            'flashcardKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Flashcard']", 'null': 'True'}),
            'labelKey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Label']", 'null': 'True'})
        }
    }

    complete_apps = ['flashcardapp']