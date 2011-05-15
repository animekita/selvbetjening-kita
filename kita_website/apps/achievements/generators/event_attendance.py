from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, post_delete
from django.db import models

from selvbetjening.core.events.models import Event, Attend, AttendState, Group

from kita_website.apps.achievements.models import Achievement, AchievementGroup, Award

# Event attendance achievement
#
# - Automatically creates achievement when event is created
# - Automatically changes achievement group if event changes group
# - Automatically awards achievement when user attends event
# - Automatically revoke awarded achievement if user is removed from attended status

class GroupToAchievementGroupManager(models.Manager):

    def get_or_create(self, group):

        try:
            return self.get(group=group), False

        except GroupToAchievementGroup.DoesNotExist:

            if group == None:
                slug = 'events'
                defaults = {'name' : 'Arrangementer'}
            else:
                parent, created = self.get_or_create(group=None)

                slug = 'events-%s' % group.pk
                defaults = {'name': group.name, 'parent': parent.achievement_group}

            agroup, created = AchievementGroup.objects.get_or_create(slug=slug,
                                                                     defaults=defaults)

            return self.create(group=group, achievement_group=agroup), True

class GroupToAchievementGroup(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True)
    achievement_group = models.ForeignKey(AchievementGroup)

    objects = GroupToAchievementGroupManager()

    class Meta:
        unique_together = ('group', 'achievement_group')
        app_label = 'achievements'

class EventAttendanceAchivementManger(models.Manager):

    def get_or_create(self, event):
        try:
            return self.get(event=event), False

        except EventAttendanceAchievement.DoesNotExist:

            rel, created = GroupToAchievementGroup.objects.get_or_create(event.group)

            achievement, created = Achievement.objects.get_or_create(slug=slugify(event.title)[:50],
                                                                     defaults={'name': event.title,
                                                                               'group': rel.achievement_group})

            achievement.timestamp = event.startdate
            achievement.save()

            return EventAttendanceAchievement.objects.create(event=event,
                                                             achievement=achievement), True

class EventAttendanceAchievement(models.Model):
    event = models.ForeignKey(Event)
    achievement = models.ForeignKey(Achievement)

    objects = EventAttendanceAchivementManger()

    class Meta:
        unique_together = ('event', 'achievement')
        app_label = 'achievements'

def refresh():
    # remove old entries
    for rel in EventAttendanceAchievement.objects.all():
        rel.achievement.delete()
        rel.delete()

    # create new achievement groups
    base_group, created = GroupToAchievementGroup.objects.get_or_create(group=None)

    for group in Group.objects.all():
        GroupToAchievementGroup.objects.get_or_create(group=group)

    # create new event achievements
    for event in Event.objects.all():
        EventAttendanceAchievement.objects.get_or_create(event=event)

    # award achievements
    for attend in Attend.objects.all():
        if attend.state == AttendState.attended:
            rel, created = EventAttendanceAchievement.objects.get_or_create(event=attend.event)

            award, created = Award.objects.get_or_create(achievement=rel.achievement,
                                                         user=attend.user)

            award.timestamp = attend.event.startdate
            award.save()

def attendance_deleted_handler(sender, **kwargs):
    attend = kwargs['instance']

    relation = EventAttendanceAchievement.objects.get(event=attend.event)
    achievement = relation.achievement

    Award.objects.filter(achievement=achievement, user=attend.user).delete()

post_delete.connect(attendance_deleted_handler, sender=Attend)

def attendance_changed_handler(sender, **kwargs):
    attend = kwargs['instance']

    relation = EventAttendanceAchievement.objects.get(event=attend.event)
    achievement = relation.achievement

    if attend.state == AttendState.attended:
        Award.objects.get_or_create(achievement=achievement, user=attend.user)
    else:
        Award.objects.filter(achievement=achievement, user=attend.user).delete()

post_save.connect(attendance_changed_handler, sender=Attend)

def event_changed_handler(sender, **kwargs):
    event = kwargs['instance']
    created = kwargs['created']

    rel, created = EventAttendanceAchievement.objects.get_or_create(event=event)

    if not created:
        group_rel, created = GroupToAchievementGroup.objects.get_or_create(event.group)

        rel.achievement.group = group_rel.achievement_group
        rel.achievement.save()

post_save.connect(event_changed_handler, sender=Event)

