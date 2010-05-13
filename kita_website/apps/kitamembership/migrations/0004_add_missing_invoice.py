from south.db import db
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from kita_website.apps.kitamembership.models import *

class Migration:

    no_dry_run = True

    depends_on = (
        ("events", "0013_add_missing_invoices"),
    )

    def forwards(self, orm):
        for membership in orm.Membership.objects.all():
            try:
                invoice = membership.invoice
                continue
            except ObjectDoesNotExist:
                pass


            # try to connect payment to event, and possible attend - invoice
            event = None
            invoice = None

            try:
                event = orm['events.Event'].objects.get(startdate=membership.bind_date)
            except ObjectDoesNotExist:
                pass

            if event is not None:
                try:
                    attendee = orm['events.Attend'].objects.get(event=event,
                                                                user=membership.user)

                    invoice = attendee.invoice
                except ObjectDoesNotExist:
                    pass

            if invoice is None:
                invoice = orm['invoice.Invoice'].objects.create(user=membership.user,
                                                                name='Membership payment')

            try:
                invoice_revision = orm['invoice.InvoiceRevision'].objects.filter(invoice=invoice).latest('id')
            except ObjectDoesNotExist:
                invoice_revision = orm['invoice.InvoiceRevision'].objects.create(invoice=invoice)

            if membership.membership_type == 'FULL':
                price = 100
            else:
                price = 50

            orm['invoice.Line'].objects.create(revision=invoice_revision,
                                               description=u'%s membership' % membership.membership_type,
                                               price=price,
                                               managed=True)

            orm['invoice.Payment'].objects.create(revision=invoice_revision,
                                                  amount=price,
                                                  note='Automatic payment (pre invoice)')

            membership.invoice = invoice
            membership.event = event
            membership.save()

    def backwards(self, orm):
        pass

    models = {
        'events.event': {
            'change_confirmation': ('models.TextField', [], {'blank': 'True'}),
            'description': ('models.TextField', ["_(u'description')"], {'blank': 'True'}),
            'enddate': ('models.DateField', ["_(u'end date')"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'maximum_attendees': ('models.IntegerField', ["_('Maximum attendees')"], {'default': '0'}),
            'registration_confirmation': ('models.TextField', [], {'blank': 'True'}),
            'registration_open': ('models.BooleanField', ["_(u'registration open')"], {}),
            'show_change_confirmation': ('models.BooleanField', [], {'default': 'False'}),
            'show_registration_confirmation': ('models.BooleanField', [], {'default': 'False'}),
            'startdate': ('models.DateField', ["_(u'start date')"], {'null': 'True', 'blank': 'True'}),
            'title': ('models.CharField', ["_(u'title')"], {'max_length': '255'})
        },
        'events.attend': {
            'Meta': {'unique_together': "('event','user')"},
            'event': ('models.ForeignKey', ['Event'], {}),
            'has_attended': ('models.BooleanField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('models.ForeignKey', ['Invoice'], {'blank': 'True'}),
            'user': ('models.ForeignKey', ['User'], {})
        },
        'kitamembership.membership': {
            'Meta': {'unique_together': "(('user','invoice'),)"},
            'bind_date': ('models.DateTimeField', [], {}),
            'event': ('models.ForeignKey', ['Event'], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('models.ForeignKey', ['Invoice'], {'blank': 'True'}),
            'membership_type': ('models.CharField', [], {'max_length': '5'}),
            'user': ('models.ForeignKey', ['User'], {'verbose_name': "_(u'user')"})
        },
        'kitamembership.yearlyrate': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'rate': ('models.IntegerField', [], {}),
            'year': ('models.IntegerField', [], {'max_length': '4'})
        },
        'invoice.invoice': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '256'}),
            'user': ('models.ForeignKey', ['User'], {})
        },
        'invoice.payment': {
            'amount': ('models.IntegerField', [], {}),
            'created_date': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'note': ('models.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'revision': ('models.ForeignKey', ['InvoiceRevision'], {}),
            'signee': ('models.ForeignKey', ['User'], {'related_name': "'signed_payment_set'", 'null': 'True', 'blank': 'True'})
        },
        'auth.user': {
            'date_joined': ('models.DateTimeField', ["_('date joined')"], {'default': 'None'}),
            'email': ('models.EmailField', ["_('e-mail address')"], {'blank': 'True'}),
            'first_name': ('models.CharField', ["_('first name')"], {'max_length': '30', 'blank': 'True'}),
            'groups': ('models.ManyToManyField', ['Group'], {'verbose_name': "_('groups')", 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('models.BooleanField', ["_('active')"], {'default': 'True'}),
            'is_staff': ('models.BooleanField', ["_('staff status')"], {'default': 'False'}),
            'is_superuser': ('models.BooleanField', ["_('superuser status')"], {'default': 'False'}),
            'last_login': ('models.DateTimeField', ["_('last login')"], {'default': 'None'}),
            'last_name': ('models.CharField', ["_('last name')"], {'max_length': '30', 'blank': 'True'}),
            'password': ('models.CharField', ["_('password')"], {'max_length': '128'}),
            'user_permissions': ('models.ManyToManyField', ['Permission'], {'verbose_name': "_('user permissions')", 'blank': 'True'}),
            'username': ('models.CharField', ["_('username')"], {'unique': 'True', 'max_length': '30'})
        },
        'invoice.invoicerevision': {
            'created_date': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('models.ForeignKey', ['Invoice'], {'related_name': "'revision_set'"})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label','codename')", 'unique_together': "(('content_type','codename'),)"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.group': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'invoice.line': {
            'description': ('models.CharField', [], {'max_length': '255'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'managed': ('models.BooleanField', [], {'default': 'False'}),
            'price': ('models.IntegerField', [], {'default': '0'}),
            'revision': ('models.ForeignKey', ['InvoiceRevision'], {})
        }
    }

    complete_apps = ['kitamembership']

