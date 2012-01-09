# coding=utf8

from datetime import date

from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.db.models.signals import m2m_changed
from django.db import models
from django.contrib.auth.models import User, Group

from kita_website.apps.achievements.models import Achievement, AchievementGroup, Award

# Position achievement
#
# - Position histroy tracked in Position
# - Automatically award achievement when entry is added to PositionHistory
# - Automatically update achievement if PositionHistory is changed
# - Automatically remove achievement if entry is removed from PositionHistory

class Position(models.Model):
    name = models.CharField(_(u'name'), max_length=255)
    monitor_group = models.ForeignKey(Group, blank=True, null=True)

    achievement = models.ForeignKey(Achievement, blank=True)

    class Meta:
        app_label = 'achievements'

    def save(self, *args, **kwargs):
        try:
            self.achievement
        except Achievement.DoesNotExist:
            self.achievement = Achievement.objects.create(slug=slugify(self.name),
                                                          group=get_achievement_group(),
                                                          name=self.name)

        return super(Position, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class PositionHistory(models.Model):
    position = models.ForeignKey(Position)
    user = models.ForeignKey(User)

    joined = models.DateField()
    leaved = models.DateField(null=True, blank=True)

    note = models.CharField(_(u'note'), max_length=255, blank=True)

    award = models.ForeignKey(Award)

    def save(self, *args, **kwargs):
        try:
            self.award
        except Award.DoesNotExist:
            self.award = Award.objects.create(achievement=self.position.achievement,
                                              user=self.user)

        self.award.timestamp = self.joined

        leaved = self.leaved if self.leaved is not None else 'nu'
        note = ' (%s)' % self.note if self.note != '' else ''
        self.award.note = '%s - %s%s' % (self.joined, leaved, note)
        self.award.save()

        return super(PositionHistory, self).save(*args, **kwargs)

    class Meta:
        app_label = 'achievements'

def get_achievement_group():
    group, created = AchievementGroup.objects.get_or_create(slug='positions',
                                                            defaults={
                                                                'name': 'Arbejde i Anime Kita',
                                                                'order': 2,
                                                            })

    return group

def refresh():
    for position in Position.objects.all():
        if position.monitor_group:
            for user in position.monitor_group.user_set.all():
                PositionHistory.objects.get_or_create(position=position,
                                                      user=user,
                                                      defaults={'joined': date.today()})

def joined_group(group_pk, user):
    try:
        position = Position.objects.get(monitor_group__pk=group_pk)

        try:
            existing = PositionHistory.objects.filter(position=position,
                                                      user=user,
                                                      leaved=date.today())
            
            for instance in existing:
                instance.leaved = None
                instance.save()

        except PositionHistory.DoesNotExist:
            PositionHistory.objects.create(position=position,
                                           user=user,
                                           joined=date.today())

    except Position.DoesNotExist:
        return #ignore

def leaved_group(group_pk, user):
    try:
        for history in PositionHistory.objects.filter(position__monitor_group__pk=group_pk, user=user):
            history.leaved = date.today()
            history.save()

            if history.joined == history.leaved:
                history.delete()

    except PositionHistory.DoesNotExist:
        return # ignore

def leaved_all_groups(user):
    for position in Position.objects.all():

        if position.monitor_group:
            leaved_group(position.monitor_group.pk, user)

def membership_changed(sender, **kwargs):
    user = kwargs['instance']
    model = kwargs['model']
    action = kwargs['action']
    pk_set = kwargs['pk_set']

    if model != Group:
        return

    if action == 'post_add':
        for pk in pk_set:
            joined_group(pk, user)

    elif action == 'post_remove':
        for pk in pk_set:
            leaved_group(pk, user)

    elif action == 'post_clear':
        leaved_all_groups(user)

m2m_changed.connect(membership_changed, sender=User.groups.through)

