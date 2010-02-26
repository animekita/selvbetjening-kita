
from south.db import db
from django.db import models
from kita_website.apps.kitamembership.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Payment'
        db.create_table('kitamembership_payment', (
            ('timestamp', models.DateTimeField()),
            ('type', models.CharField(max_length=5)),
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'], verbose_name=_(u'user'))),
        ))
        db.send_create_signal('kitamembership', ['Payment'])
        
        # Adding model 'YearlyRate'
        db.create_table('kitamembership_yearlyrate', (
            ('rate', models.IntegerField()),
            ('id', models.AutoField(primary_key=True)),
            ('year', models.IntegerField(max_length=4)),
        ))
        db.send_create_signal('kitamembership', ['YearlyRate'])
        
    def backwards(self, orm):
        
        # Deleting model 'Payment'
        db.delete_table('kitamembership_payment')
        
        # Deleting model 'YearlyRate'
        db.delete_table('kitamembership_yearlyrate')
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'kitamembership.payment': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('models.DateTimeField', [], {}),
            'type': ('models.CharField', [], {'max_length': '5'}),
            'user': ('models.ForeignKey', ['User'], {'verbose_name': "_(u'user')"})
        },
        'kitamembership.yearlyrate': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'rate': ('models.IntegerField', [], {}),
            'year': ('models.IntegerField', [], {'max_length': '4'})
        }
    }
