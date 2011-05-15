from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class AchievementGroup(models.Model):
    slug = models.SlugField(primary_key=True)

    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subgroups')

    order = models.IntegerField(_(u'Order (asc)'), default=5)

    class Meta:
        app_label = 'achievements'

    @staticmethod
    def get_general_group():
        group, created = AchievementGroup.objects.get_or_create(
            slug='general', defaults={'name': 'Overordnet', 'order': 0})

        return group

    def __unicode__(self):
        return self.name

class Achievement(models.Model):
    slug = models.SlugField(primary_key=True)

    group = models.ForeignKey(AchievementGroup)
    name = models.CharField(max_length=255)

    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'achievements'
        ordering = ['-timestamp']

class Award(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(User)

    note = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'achievements'

