# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Class'
        db.create_table('flashcardapp_class', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('flashcardapp', ['Class'])

        # Adding model 'SharedAttributes'
        db.create_table('flashcardapp_sharedattributes', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publicationDate', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 4, 12, 0, 0))),
            ('rating', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('professorApproved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('whichProfessors', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('flashcardapp', ['SharedAttributes'])

        # Adding model 'Container'
        db.create_table('flashcardapp_container', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('classkey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Class'], null=True)),
            ('isPrivate', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('isUpdatable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('sharedAttributes', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['flashcardapp.SharedAttributes'], unique=True, null=True)),
        ))
        db.send_create_signal('flashcardapp', ['Container'])

        # Adding model 'Tag'
        db.create_table('flashcardapp_tag', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('containerkey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Container'], null=True)),
        ))
        db.send_create_signal('flashcardapp', ['Tag'])

        # Adding model 'Box'
        db.create_table('flashcardapp_box', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('flashcardapp', ['Box'])

        # Adding M2M table for field containers on 'Box'
        db.create_table('flashcardapp_box_containers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('box', models.ForeignKey(orm['flashcardapp.box'], null=False)),
            ('container', models.ForeignKey(orm['flashcardapp.container'], null=False))
        ))
        db.create_unique('flashcardapp_box_containers', ['box_id', 'container_id'])

        # Adding model 'Flashcard'
        db.create_table('flashcardapp_flashcard', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('flashcardapp', ['Flashcard'])

        # Adding M2M table for field boxes on 'Flashcard'
        db.create_table('flashcardapp_flashcard_boxes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('flashcard', models.ForeignKey(orm['flashcardapp.flashcard'], null=False)),
            ('box', models.ForeignKey(orm['flashcardapp.box'], null=False))
        ))
        db.create_unique('flashcardapp_flashcard_boxes', ['flashcard_id', 'box_id'])

        # Adding model 'Label'
        db.create_table('flashcardapp_label', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('userKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('flashcardapp', ['Label'])

        # Adding model 'TextSide'
        db.create_table('flashcardapp_textside', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('flashcardKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Flashcard'], null=True)),
            ('labelKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Label'], null=True)),
        ))
        db.send_create_signal('flashcardapp', ['TextSide'])

        # Adding model 'ImageSide'
        db.create_table('flashcardapp_imageside', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('flashcardKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Flashcard'], null=True)),
            ('labelKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Label'], null=True)),
        ))
        db.send_create_signal('flashcardapp', ['ImageSide'])

        # Adding model 'AudioSide'
        db.create_table('flashcardapp_audioside', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flashcardKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Flashcard'], null=True)),
            ('labelKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Label'], null=True)),
        ))
        db.send_create_signal('flashcardapp', ['AudioSide'])

        # Adding model 'VideoSide'
        db.create_table('flashcardapp_videoside', (
            ('Id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flashcardKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Flashcard'], null=True)),
            ('labelKey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flashcardapp.Label'], null=True)),
        ))
        db.send_create_signal('flashcardapp', ['VideoSide'])


    def backwards(self, orm):
        # Deleting model 'Class'
        db.delete_table('flashcardapp_class')

        # Deleting model 'SharedAttributes'
        db.delete_table('flashcardapp_sharedattributes')

        # Deleting model 'Container'
        db.delete_table('flashcardapp_container')

        # Deleting model 'Tag'
        db.delete_table('flashcardapp_tag')

        # Deleting model 'Box'
        db.delete_table('flashcardapp_box')

        # Removing M2M table for field containers on 'Box'
        db.delete_table('flashcardapp_box_containers')

        # Deleting model 'Flashcard'
        db.delete_table('flashcardapp_flashcard')

        # Removing M2M table for field boxes on 'Flashcard'
        db.delete_table('flashcardapp_flashcard_boxes')

        # Deleting model 'Label'
        db.delete_table('flashcardapp_label')

        # Deleting model 'TextSide'
        db.delete_table('flashcardapp_textside')

        # Deleting model 'ImageSide'
        db.delete_table('flashcardapp_imageside')

        # Deleting model 'AudioSide'
        db.delete_table('flashcardapp_audioside')

        # Deleting model 'VideoSide'
        db.delete_table('flashcardapp_videoside')


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
            'containerkey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flashcardapp.Container']", 'null': 'True'}),
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