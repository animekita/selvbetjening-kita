
from south.db import db
from django.db import models
from kita_website.apps.kitamembership.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Creating unique_together for [user, invoice] on Membership.
        db.create_unique('kitamembership_membership', ['user_id', 'invoice_id'])
    
    def backwards(self, orm):
        
        # Deleting unique_together for [user, invoice] on Membership.
        db.delete_unique('kitamembership_membership', ['user_id', 'invoice_id'])
    
    models = {
        'kitamembership.membership': {
            'Meta': {'unique_together': "(('user','invoice'),)"},
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
