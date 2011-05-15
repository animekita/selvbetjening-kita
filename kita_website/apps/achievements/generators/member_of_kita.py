from django.db.models.signals import post_save
from django.contrib.auth.models import User

from kita_website.apps.achievements.models import Achievement, AchievementGroup, Award

# Member of Kita (free) Achievement
#
# - Automatically award achievement when user is created

NOTE_FORMAT = 'Medlemsnummer #%s'

def get_achievement():
    achievement, created = Achievement.objects.get_or_create(
        slug='member_of_kita',
        defaults={'name' : 'Medlem af Anime Kita',
                  'group' : AchievementGroup.get_general_group()})

    return achievement

def refresh():
    achievement = get_achievement()

    for user in User.objects.all():
        award, created = Award.objects.get_or_create(achievement=achievement, user=user,
                                                     defaults={'note': NOTE_FORMAT % user.pk})

        award.note = NOTE_FORMAT % user.pk
        award.save()

def user_created_handler(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']

    if created:
        achievement = get_achievement()

        Award.objects.create(achievement=achievement,
                             user=user,
                             note=NOTE_FORMAT % user.pk)

post_save.connect(user_created_handler, sender=User)