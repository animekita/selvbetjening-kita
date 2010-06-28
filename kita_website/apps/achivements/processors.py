from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.admin.helpers import AdminForm

from selvbetjening.clients.profile.processor_handlers import profile_page_processors

from models import Achivement, AchivementGroup, Award

class ProfilePageProcessor(object):
    template_name = 'achivements/profile_page.html'

    def __init__(self, request, user):
        self.request = request
        self.user = user

    def view(self):
        awards = Award.objects.filter(user=self.user).\
               order_by('-achivement__group__pk', 'achivement__name', 'note')

        return render_to_string(self.template_name,
                                {'awards' : awards,},
                                context_instance=RequestContext(self.request))

profile_page_processors.register(ProfilePageProcessor)
