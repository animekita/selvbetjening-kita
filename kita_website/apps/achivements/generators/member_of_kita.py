from django.db.models.signals import post_save
from django.contrib.auth.models import User

from kita_website.apps.achivements.models import Achivement, Award

# Member of Kita (free) Achivement
#
# - Automatically award achivement when user is created

def user_created_handler(sender, **kwargs):
    user = kwargs['instance']
    created = kwargs['created']

    if created:
        achivement = Achivement.objects.get(pk=Achivement.MEMBER_OF_KITA)

        Award.objects.create(achivement=achivement,
                             user=user,
                             note='medlemsnummer #%s' % user.pk)

post_save.connect(user_created_handler, sender=User)