# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        for tag in orm.Tag.objects.all():
            cntid = tag.containerkey.Id
            tag.containers.add(orm.Container.objects.get(pk=cntid))
            tag.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        for tag in orm.Tag.objects.all():
            cntid = tag.containers.all()[0].Id
            tag.containerkey = orm.Container.objects.get(pk=cntid)
            tag.save()

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
            'classkey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Class']", 'null': 'True'}),
            'isPrivate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'isUpdatable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sharedAttributes': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['flashcardapp.SharedAttributes']", 'unique': 'True', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'flashcardapp.flashcard': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Flashcard'},
            'boxes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['flashcardapp.Box']", 'null': 'True', 'symmetrical': 'False'}),
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'publicationDate': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 12, 0, 0)'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'whichProfessors': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'flashcardapp.tag': {
            'Id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Tag'},
            'containerkey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'oldcontainer'", 'null': 'True', 'to': "orm['flashcardapp.Container']"}),
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
    symmetrical = True
