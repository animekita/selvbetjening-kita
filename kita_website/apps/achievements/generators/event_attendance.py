from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, post_delete
from django.db import models

from selvbetjening.core.events.models import Event, Attend, AttendState

from kita_website.apps.achievements.models import Achivement, AchivementGroup, Award

# Event attendance achievement
#
# - Automatically creates achievement when event is created
# - Automatically award achievement when user attended event
# - Automatically revoke awarded achievement if user is removed from attended status

class EventAttendanceAchivement(models.Model):
    event = models.ForeignKey(Event)
    achievement = models.ForeignKey(Achivement)

    class Meta:
        unique_together = ('event', 'achievement')
        app_label = 'achievements'

def attendance_deleted_handler(sender, **kwargs):
    attend = kwargs['instance']

    relation = EventAttendanceAchivement.objects.get(event=attend.event)
    achievement = relation.achievement

    Award.objects.filter(achievement=achievement, user=attend.user).delete()

post_delete.connect(attendance_deleted_handler, sender=Attend)

def attendance_changed_handler(sender, **kwargs):
    attend = kwargs['instance']

    relation = EventAttendanceAchivement.objects.get(event=attend.event)
    achievement = relation.achievement

    if attend.state == AttendState.attended:
        Award.objects.get_or_create(achievement=achievement, user=attend.user)
    else:
        Award.objects.filter(achievement=achievement, user=attend.user).delete()


post_save.connect(attendance_changed_handler, sender=Attend)

def event_changed_handler(sender, **kwargs):
    event = kwargs['instance']
    created = kwargs['created']

    if created:
        group = AchivementGroup.Default.events()

        achievement = Achivement.objects.create(name=event.title,
                                               slug=slugify(event.title),
                                               group=group)

        EventAttendanceAchivement.objects.create(event=event,
                                                 achievement=achievement)

post_save.connect(event_changed_handler, sender=Event)

