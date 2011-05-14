from django.db.models.signals import post_save
from django.contrib.auth.models import User

from kita_website.apps.achievements.models import Achivement, Award

# Member of Kita (free) Achivement
#
# - Automatically award achievement when user is created

def user_created_handler(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']

    if created:
        achievement = Achivement.Default.member_of_kita()

        Award.objects.create(achievement=achievement,
                             user=user,
                             note='medlemsnummer #%s' % user.pk)

post_save.connect(user_created_handler, sender=User)