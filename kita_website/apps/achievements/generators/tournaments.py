from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from selvbetjening.core.events.models import Event

from kita_website.apps.achievements.models import Achievement, AchievementGroup, Award

# Tournament Winner Achievement
#
# - Tournament and winning history tracked in Tournament and Winner
# - Automatically create achievement if entry is added to Tournament
# - Automatically remove achievement if entry is removed from Tournament
#
# - Automatically award achievement if entry is added to Winner
# - Automatically redraw achievement if entry is removed from Winner
# - Automatically update achievement if Winner or Tournament are changed

class Tournament(models.Model):
    name = models.CharField(_('name'), max_length=255)

    achievement = models.ForeignKey(Achievement, blank=True)

    class Meta:
        app_label = 'achievements'

    def save(self, *args, **kwargs):
        try:
            self.achievement
        except Achievement.DoesNotExist:
            self.achievement = Achievement.objects.create(slug=slugify(self.name)[:50],
                                                          group=get_achievement_group(),
                                                          name=self.name)

        # updates
        self.achievement.name = self.name
        self.achievement.save()

        super(Tournament, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Tournament, self).delete(*args, **kwargs)

        try:
            self.achievement.delete()
        except Achievement.DoesNotExist:
            pass #ignore

    def __unicode__(self):
        return self.name

class Winner(models.Model):
    user = models.ForeignKey(User)
    tournament = models.ForeignKey(Tournament, db_column='turnament_id')
    event = models.ForeignKey(Event)

    note = models.CharField(_(u'note'), max_length=255, blank=True)

    award = models.ForeignKey(Award, blank=True)

    class Meta:
        unique_together = ('user', 'tournament', 'event')
        app_label = 'achievements'

    def save(self, *args, **kwargs):
        try:
            self.award
        except Award.DoesNotExist:
            self.award = Award.objects.create(achievement=self.tournament.achievement,
                                              user=self.user,
                                              note='')

        # updates
        self.award.note = self.event.title if self.note == '' else '%s - %s' % (self.note, self.event.title)
        self.award.user = self.user
        self.award.achievement = self.tournament.achievement
        self.award.timestamp = self.event.enddate
        self.award.save()

        super(Winner, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Winner, self).delete(*args, **kwargs)

        try:
            self.award.delete()
        except:
            pass # ignore

def get_achievement_group():
    group, created = AchievementGroup.objects.get_or_create(slug='tournaments',
                                                            defaults={
                                                                'name': 'Konkurrencer',
                                                                'order': 3,
                                                            })

    return group
