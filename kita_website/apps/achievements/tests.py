from django import test
from django.contrib.auth.models import User, Group

from selvbetjening.core.events.tests import Database

from models import GroupMembersAchievement, AchievementGroup,\
     Achievement, Award, GroupMembersAchievement

class GroupMembershipTest(test.TestCase):
    def setUp(self):
        achievementGroup = AchievementGroup.objects.create(name='ag', slug='ag')
        self.achievement = Achievement.objects.create(name='a', slug='a',
                                                    group=achievementGroup)

        self.group = Group.objects.create(name='generic group')
        self.user = Database.new_user()

    def test_add_user_to_group_not_tracked(self):
        self.user.groups.add(self.group)

        self.assertEqual(0, Award.objects.all().count())

    def test_add_user_to_group(self):
        GroupMembersAchievement.objects.create(achievement=self.achievement,
                                              group=self.group)

        self.user.groups.add(self.group)

        self.assertEqual(1, Award.objects.all().count())

    def test_remove_user_from_group(self):
        GroupMembersAchievement.objects.create(achievement=self.achievement,
                                              group=self.group)

        self.user.groups.add(self.group)
        self.user.groups.remove(self.group)

        self.assertEqual(1, Award.objects.all().count())


