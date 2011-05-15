from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.admin.helpers import AdminForm

from selvbetjening.portal.profile.models import UserPrivacy
from selvbetjening.portal.profile.processor_handlers import profile_page_processors, \
     extended_privacy_processors

from models import Achievement, AchievementGroup, Award, Privacy

class ProfilePageProcessor(object):
    template_name = 'achievements/profile_page.html'

    def __init__(self, request, user):
        self.request = request
        self.user = user

    def view(self, own_profile):
        user_privacy, created = UserPrivacy.objects.get_or_create(user=self.user)
        privacy, created = Privacy.objects.get_or_create(user=self.user)

        if own_profile or \
           (user_privacy.public_profile and privacy.public_achievements):

            awards = Award.objects.filter(user=self.user).\
                   order_by('achievement__group__order', 'achievement__group__pk', '-timestamp')

            return render_to_string(self.template_name,
                                    {'awards' : awards,},
                                    context_instance=RequestContext(self.request))

        else:
            return ''

profile_page_processors.register(ProfilePageProcessor)

class ExtendedPrivacyProcessor(object):
    def __init__(self, user):
        self.user = user

        self.privacy, created = Privacy.objects.get_or_create(user=self.user)

    def get_privacy_options(self):
        return [('achievement', 'Achievement', self.privacy.public_achievements),]

    def save_privacy_options(self, options):
        privacy_setting = bool(options.get('achievement', False))

        self.privacy.public_achievements = privacy_setting
        self.privacy.save()

extended_privacy_processors.register(ExtendedPrivacyProcessor)
