from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import Achievement, AchievementGroup

@login_required
def list_achievements(request,
                     template_name='achievements/list_achievements.html'):

    groups = AchievementGroup.objects.filter(parent=None).order_by('order', 'name')
    awarded = Achievement.objects.filter(award__user=request.user)

    return render_to_response(template_name,
                              {'groups' : groups,
                               'awarded' : awarded},
                              context_instance=RequestContext(request))