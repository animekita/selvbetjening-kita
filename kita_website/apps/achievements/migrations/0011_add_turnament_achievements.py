# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Winner'
        db.create_table('achievements_winner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('turnament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Turnament'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('award', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Award'], blank=True)),
        ))
        db.send_create_signal('achievements', ['Winner'])

        # Adding unique constraint on 'Winner', fields ['user', 'turnament', 'event']
        db.create_unique('achievements_winner', ['user_id', 'turnament_id', 'event_id'])

        # Adding model 'Turnament'
        db.create_table('achievements_turnament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('achievement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Achievement'], blank=True)),
        ))
        db.send_create_signal('achievements', ['Turnament'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Winner', fields ['user', 'turnament', 'event']
        db.delete_unique('achievements_winner', ['user_id', 'turnament_id', 'event_id'])

        # Deleting model 'Winner'
        db.delete_table('achievements_winner')

        # Deleting model 'Turnament'
        db.delete_table('achievements_turnament')


    models = {
        'achievements.achievement': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Achievement'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.AchievementGroup']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'achievements.achievementgroup': {
            'Meta': {'object_name': 'AchievementGroup'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subgroups'", 'null': 'True', 'to': "orm['achievements.AchievementGroup']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'achievements.award': {
            'Meta': {'object_name': 'Award'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Achievement']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'achievements.eventattendanceachievement': {
            'Meta': {'unique_together': "(('event', 'achievement'),)", 'object_name': 'EventAttendanceAchievement'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Achievement']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'achievements.grouptoachievementgroup': {
            'Meta': {'unique_together': "(('group', 'achievement_group'),)", 'object_name': 'GroupToAchievementGroup'},
            'achievement_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.AchievementGroup']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'achievements.position': {
            'Meta': {'object_name': 'Position'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Achievement']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'monitor_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'achievements.positionhistory': {
            'Meta': {'object_name': 'PositionHistory'},
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Award']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateField', [], {}),
            'leaved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Position']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'achievements.privacy': {
            'Meta': {'object_name': 'Privacy'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_achievements': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'achievements.turnament': {
            'Meta': {'object_name': 'Turnament'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Achievement']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'achievements.winner': {
            'Meta': {'unique_together': "(('user', 'turnament', 'event'),)", 'object_name': 'Winner'},
            'award': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Award']", 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'turnament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievements.Turnament']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
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
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'custom_change_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'custom_signup_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'custom_status_page': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enddate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_attendees': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'move_to_accepted_policy': ('django.db.models.fields.CharField', [], {'default': "'always'", 'max_length': '32'}),
            'registration_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_custom_change_message': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_custom_signup_message': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_custom_status_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'startdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'events.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['achievements']
