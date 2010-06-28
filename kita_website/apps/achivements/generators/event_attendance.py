from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, post_delete
from django.db import models

from selvbetjening.data.events.models import Event, Attend, AttendState

from kita_website.apps.achivements.models import Achivement, AchivementGroup, Award

# Event attendance achivement
#
# - Automatically creates achivement when event is created
# - Automatically award achivement when user attended event
# - Automatically revoke awarded achivement if user is removed from attended status

class EventAttendanceAchivement(models.Model):
    event = models.ForeignKey(Event)
    achivement = models.ForeignKey(Achivement)

    class Meta:
        unique_together = ('event', 'achivement')
        app_label = 'achivements'

def attendance_deleted_handler(sender, **kwargs):
    attend = kwargs['instance']

    relation = EventAttendanceAchivement.objects.get(event=attend.event)
    achivement = relation.achivement

    Award.objects.filter(achivement=achivement, user=attend.user).delete()

post_delete.connect(attendance_deleted_handler, sender=Attend)

def attendance_changed_handler(sender, **kwargs):
    attend = kwargs['instance']

    relation = EventAttendanceAchivement.objects.get(event=attend.event)
    achivement = relation.achivement

    if attend.state == AttendState.attended:
        Award.objects.get_or_create(achivement=achivement, user=attend.user)
    else:
        Award.objects.filter(achivement=achivement, user=attend.user).delete()


post_save.connect(attendance_changed_handler, sender=Attend)

def event_changed_handler(sender, **kwargs):
    event = kwargs['instance']
    created = kwargs['created']

    if created:
        group = AchivementGroup.objects.get(slug=AchivementGroup.EVENTS)

        achivement = Achivement.objects.create(name=event.title,
                                               slug=slugify(event.title),
                                               group=group)

        EventAttendanceAchivement.objects.create(event=event,
                                                 achivement=achivement)

post_save.connect(event_changed_handler, sender=Event)

