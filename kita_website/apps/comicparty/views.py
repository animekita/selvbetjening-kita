from datetime import datetime, timedelta

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from selvbetjening.core.members.shortcuts import get_or_create_profile

from kita_website.apps.kitamembership.models import Membership, MembershipState

from models import Order, comicparty_order_source
from forms import OrderForm

def register(request):

    is_member = Membership.objects.get_membership_state(request.user) != MembershipState.INACTIVE
    already_ordered = Order.objects.filter(user=request.user)\
                                   .filter(timestamp__gt=datetime.now() - timedelta(days=4*30))\
                                   .exists()

    profile = get_or_create_profile(request.user)

    initial = {}
    initial['name'] = request.user.get_full_name()
    initial['street'] = profile.street
    initial['city'] = profile.city
    initial['postalcode'] = profile.postalcode
    initial['email'] = request.user.email

    if request.method == 'POST' and is_member:
        form = OrderForm(request.POST, initial=initial)

        if form.is_valid():
            form.cleaned_data.pop('accept')

            order = Order.objects.create(user=request.user,
                                         **form.cleaned_data)

            # send e-mail
            comicparty_order_source.trigger(request.user, order=order)

            return HttpResponseRedirect(reverse('comicparty_accepted'))

    else:
        form = OrderForm(initial=initial)

    return render_to_response('comicparty/register.html',
                              {'form' : form,
                               'is_member' : is_member,
                               'already_ordered' : already_ordered},
                              context_instance=RequestContext(request))
