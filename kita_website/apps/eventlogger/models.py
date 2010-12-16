import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings
from django.db.models.signals import post_delete, post_save

from selvbetjening.core.events.models import Attend, Selection
from selvbetjening.core.invoice.models import Payment

from kita_website.apps.kitamembership.models import Membership

handler = RotatingFileHandler(settings.AUDIT_FILE)
logger = logging.getLogger('audit')
logger.setLevel(logging.NOTSET)
logger.addHandler(handler)

def user_event_signup(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        logger.info(u'%s signed up to event %s' % (instance.user.username, instance.event.title))
    else:
        logger.info(u'%s changed attendance (now %s) to event %s' % (instance.user.username, instance.has_attended, instance.event.title))

post_save.connect(user_event_signup, Attend)

def user_event_signoff(sender, **kwargs):
    instance = kwargs['instance']

    logger.info(u'%s signed off from event %s' % (instance.user.username, instance.event.title))

post_delete.connect(user_event_signoff, Attend)

def payment_added_changed(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        logger.info(u'payment (%s) added for user %s by the amount %s' % (instance.id, instance.revision.invoice.user.username, instance.amount))
    else:
        logger.info(u'payment (%s) changed for user %s to the amount %s' % (instance.id, instance.revision.invoice.user.username, instance.amount))

post_save.connect(payment_added_changed, Payment)

def payment_removed(sender, **kwargs):
    instance = kwargs['instance']

    logger.info(u'payment (%s) removed for user %s' % (instance.id, instance.revision.invoice.user.username))

post_delete.connect(payment_removed, Payment)

def selection_added_changed(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        logger.info(u'selection (%s) added for event %s, user %s selected %s' % (instance.id, instance.attendee.event.title, instance.attendee.user.username, instance))
    else:
        logger.info(u'selection (%s) changed for event %s, user %s selected %s' % (instance.id, instance.attendee.event.title, instance.attendee.user.username, instance))

post_save.connect(selection_added_changed, Selection)

def selection_removed(sender, **kwargs):
    instance = kwargs['instance']

    logger.info(u'selection (%s) removed for event %s, user %s deselected %s' % (instance.id, instance.attendee.event.title, instance.attendee.user.username, instance))

post_delete.connect(selection_removed, Selection)

def membership_added_changed(sender, **kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        logger.info(u'membership (%s) created for user %s of %s' % (instance.id, instance.user, instance))
    else:
        logger.info(u'membership (%s) changed for user %s now %s' % (instance.id, instance.user, instance))

post_save.connect(membership_added_changed, Membership)

def membership_removed(sender, **kwargs):
    instance = kwargs['instance']

    logger.info(u'membership (%s) removed for user %s' % (instance.id, instance.user))

post_delete.connect(membership_removed, Membership)