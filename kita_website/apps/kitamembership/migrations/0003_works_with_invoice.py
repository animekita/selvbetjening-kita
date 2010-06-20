
from south.db import db
from django.db import models
from kita_website.apps.kitamembership.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Membership.invoice'
        db.add_column('kitamembership_membership', 'invoice', models.ForeignKey(orm['invoice.Invoice'], blank=True, default=0))

        # Adding field 'Membership.event'
        db.add_column('kitamembership_membership', 'event', models.ForeignKey(orm['events.Event'], null=True, blank=True))

    def backwards(self, orm):

        # Deleting field 'Membership.invoice'
        db.delete_column('kitamembership_membership', 'invoice_id')

        # Deleting field 'Membership.event'
        db.delete_column('kitamembership_membership', 'event_id')

    models = {
        'kitamembership.membership': {
            'bind_date': ('models.DateTimeField', [], {}),
            'event': ('models.ForeignKey', ['Event'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('models.ForeignKey', ['Invoice'], {'blank': 'True'}),
            'membership_type': ('models.CharField', [], {'max_length': '5'}),
            'user': ('models.ForeignKey', ['User'], {'verbose_name': "_(u'user')"})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'kitamembership.yearlyrate': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'rate': ('models.IntegerField', [], {}),
            'year': ('models.IntegerField', [], {'max_length': '4'})
        },
        'invoice.invoice': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'events.event': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['kitamembership']
