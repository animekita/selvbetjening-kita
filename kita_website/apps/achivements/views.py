from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from models import Achivement, AchivementGroup

@login_required
def list_achivements(request,
                     template_name='achivements/list_achivements.html'):

    achivements = Achivement.objects.all().order_by('-group__pk', 'name')
    awarded = achivements.filter(award__user=request.user)

    return render_to_response(template_name,
                              {'achivements' : achivements,
                               'awarded' : awarded},
                              context_instance=RequestContext(request))