
from south.db import db
from django.db import models
from kita_website.apps.kitamembership.models import *

class Migration:
    """ This migration contains pre kita membership specific migration code """
    
    def forwards(self, orm):
        #db.rename_table('accounting_payment', 'kitamembership_payment')
        #db.rename_table('accounting_yearlyrate', 'kitamembership_yearlyrate')
        pass
        
    def backwards(self, orm): 
        #db.rename_table('kitamembership_payment', 'accounting_payment')
        #db.rename_table('kitamembership_yearlyrate', 'accounting_yearlyrate')
        pass
