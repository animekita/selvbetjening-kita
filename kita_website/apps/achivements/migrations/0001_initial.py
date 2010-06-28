# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AchivementGroup'
        db.create_table('achivements_achivementgroup', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('achivements', ['AchivementGroup'])

        # Adding model 'Achivement'
        db.create_table('achivements_achivement', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, primary_key=True, db_index=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achivements.AchivementGroup'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('achivements', ['Achivement'])

        # Adding model 'Award'
        db.create_table('achivements_award', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('achivement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achivements.Achivement'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('achivements', ['Award'])

        # Adding model 'EventAttendanceAchivement'
        db.create_table('achivements_eventattendanceachivement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('achivement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achivements.Achivement'])),
        ))
        db.send_create_signal('achivements', ['EventAttendanceAchivement'])

        # Adding unique constraint on 'EventAttendanceAchivement', fields ['event', 'achivement']
        db.create_unique('achivements_eventattendanceachivement', ['event_id', 'achivement_id'])


    def backwards(self, orm):
        
        # Deleting model 'AchivementGroup'
        db.delete_table('achivements_achivementgroup')

        # Deleting model 'Achivement'
        db.delete_table('achivements_achivement')

        # Deleting model 'Award'
        db.delete_table('achivements_award')

        # Deleting model 'EventAttendanceAchivement'
        db.delete_table('achivements_eventattendanceachivement')

        # Removing unique constraint on 'EventAttendanceAchivement', fields ['event', 'achivement']
        db.delete_unique('achivements_eventattendanceachivement', ['event_id', 'achivement_id'])


    models = {
        'achivements.achivement': {
            'Meta': {'object_name': 'Achivement'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achivements.AchivementGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'achivements.achivementgroup': {
            'Meta': {'object_name': 'AchivementGroup'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'achivements.award': {
            'Meta': {'object_name': 'Award'},
            'achivement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achivements.Achivement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'achivements.eventattendanceachivement': {
            'Meta': {'unique_together': "(('event', 'achivement'),)", 'object_name': 'EventAttendanceAchivement'},
            'achivement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achivements.Achivement']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'change_confirmation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enddate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_page': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'maximum_attendees': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'move_to_accepted_policy': ('django.db.models.fields.CharField', [], {'default': "'always'", 'max_length': '32'}),
            'registration_confirmation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'show_change_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'show_invoice_page': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'show_registration_confirmation': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['achivements']
