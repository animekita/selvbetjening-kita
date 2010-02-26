
from south.db import db
from django.db import models
from kita_website.apps.kitamembership.models import *

class Migration:
    
    def forwards(self, orm):
        db.rename_table('kitamembership_payment', 'kitamembership_membership')
        db.rename_column('kitamembership_membership', 'timestamp', 'bind_date')
        db.rename_column('kitamembership_membership', 'type', 'membership_type')
    
    def backwards(self, orm):
        db.rename_table('kitamembership_membership', 'kitamembership_payment')
        db.rename_column('kitamembership_payment', 'bind_date', 'timestamp')
        db.rename_column('kitamembership_payment', 'membership_type', 'type')
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'kitamembership.yearlyrate': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'rate': ('models.IntegerField', [], {}),
            'year': ('models.IntegerField', [], {'max_length': '4'})
        },
        'kitamembership.membership': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'bind_date': ('models.DateTimeField', [], {}),
            'membership_type': ('models.CharField', [], {'max_length': '5'}),
            'user': ('models.ForeignKey', ['User'], {'verbose_name': "_(u'user')"})
        }
    }
    
    complete_apps = ['kitamembership']
