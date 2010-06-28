from datetime import date

from django.template.defaultfilters import slugify
from django.db.models.signals import m2m_changed
from django.db import models
from django.contrib.auth.models import User, Group

from kita_website.apps.achivements.models import Achivement, AchivementGroup, Award

# Event attendance achivement
#
# - Automatically award achivement when user joins group (sets note)
# - Automatically update awarded achivement when user is removed form group (sets note)
# - Only groups in GroupMembersAchivement are tracked

class GroupMembersAchivement(models.Model):
    group = models.ForeignKey(Group, unique=True)
    achivement = models.ForeignKey(Achivement, unique=True)

    class Meta:
        app_label = 'achivements'

def add_group(group_id, user, today):
    try:
        achivement = GroupMembersAchivement.objects.get(group=group_id).achivement
        Award.objects.create(achivement=achivement, user=user,
                             note='%s - nu' % today)

    except GroupMembersAchivement.DoesNotExist:
        return #ignore

def remove_group(group_id, user, today):
    try:
        achivement = GroupMembersAchivement.objects.get(group=group_id).achivement

        award = Award.objects.filter(achivement=achivement, user=user)\
                             .latest('timestamp')

        if '- nu' in award.note:
            award.note = award.note.replace('- nu', '- %s' % today)
            award.save()

    except GroupMembersAchivement.DoesNotExist:
        return # ignore

    except Award.DoesNotExist:
        return # ignore

def clear_groups(user, today):
    for tracked in GroupMembersAchivement.objects.all():
        remove_group(tracked.group, user)

def membership_changed(sender, **kwargs):
    user = kwargs['instance']
    model = kwargs['model']
    action = kwargs['action']
    pk_set = kwargs['pk_set']

    if model != Group:
        return

    today = date.today().strftime('%B %Y')

    if action == 'post_add':
        for pk in pk_set:
            add_group(pk, user, today)

    elif action == 'post_remove':
        for pk in pk_set:
            remove_group(pk, user, today)

    elif action == 'post_clear':
        clear_groups(user, today)

m2m_changed.connect(membership_changed, sender=User.groups.through)

