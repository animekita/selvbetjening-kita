# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'webfactionemail_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_prefix', self.gf('django.db.models.fields.CharField')(unique=True, max_length=24)),
            ('forwards_other', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'webfactionemail', ['Email'])

        # Adding M2M table for field forwards on 'Email'
        db.create_table(u'webfactionemail_email_forwards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('email', models.ForeignKey(orm[u'webfactionemail.email'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'webfactionemail_email_forwards', ['email_id', 'user_id'])

        # Adding M2M table for field forwards_group on 'Email'
        db.create_table(u'webfactionemail_email_forwards_group', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('email', models.ForeignKey(orm[u'webfactionemail.email'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'webfactionemail_email_forwards_group', ['email_id', 'group_id'])

        # Adding model 'MailingList'
        db.create_table(u'webfactionemail_mailinglist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('forwards_other', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal(u'webfactionemail', ['MailingList'])

        # Adding M2M table for field forwards on 'MailingList'
        db.create_table(u'webfactionemail_mailinglist_forwards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailinglist', models.ForeignKey(orm[u'webfactionemail.mailinglist'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'webfactionemail_mailinglist_forwards', ['mailinglist_id', 'user_id'])

        # Adding M2M table for field forwards_group on 'MailingList'
        db.create_table(u'webfactionemail_mailinglist_forwards_group', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailinglist', models.ForeignKey(orm[u'webfactionemail.mailinglist'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'webfactionemail_mailinglist_forwards_group', ['mailinglist_id', 'group_id'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'webfactionemail_email')

        # Removing M2M table for field forwards on 'Email'
        db.delete_table('webfactionemail_email_forwards')

        # Removing M2M table for field forwards_group on 'Email'
        db.delete_table('webfactionemail_email_forwards_group')

        # Deleting model 'MailingList'
        db.delete_table(u'webfactionemail_mailinglist')

        # Removing M2M table for field forwards on 'MailingList'
        db.delete_table('webfactionemail_mailinglist_forwards')

        # Removing M2M table for field forwards_group on 'MailingList'
        db.delete_table('webfactionemail_mailinglist_forwards_group')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'webfactionemail.email': {
            'Meta': {'object_name': 'Email'},
            'email_prefix': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '24'}),
            'forwards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'email_forwards'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'forwards_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'email_forwards'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'forwards_other': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'webfactionemail.mailinglist': {
            'Meta': {'object_name': 'MailingList'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'forwards': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'mailing_lists'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'forwards_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'mailing_lists'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'forwards_other': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['webfactionemail']