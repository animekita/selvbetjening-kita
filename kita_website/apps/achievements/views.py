from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import Achievement, AchievementGroup

@login_required
def list_achievements(request,
                     template_name='achievements/list_achievements.html'):

    achievements = Achievement.objects.all().order_by('-group__pk', 'name')
    awarded = achievements.filter(award__user=request.user)

    return render_to_response(template_name,
                              {'achievements' : achievements,
                               'awarded' : awarded},
                              context_instance=RequestContext(request))