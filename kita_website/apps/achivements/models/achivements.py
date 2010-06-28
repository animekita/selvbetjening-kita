from django.db import models
from django.contrib.auth.models import User

class AchivementGroup(models.Model):
    EVENTS = 'events'
    GENERAL = 'general'

    slug = models.SlugField(primary_key=True)

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'achivements'

class Achivement(models.Model):
    MEMBER_OF_KITA = 'member_of_kita'

    slug = models.SlugField(primary_key=True)

    group = models.ForeignKey(AchivementGroup)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'achivements'

class Award(models.Model):
    achivement = models.ForeignKey(Achivement)
    user = models.ForeignKey(User)

    note = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'achivements'

