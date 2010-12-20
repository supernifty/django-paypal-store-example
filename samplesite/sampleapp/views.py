from django.http import HttpResponse

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

import models
import paypal

def home( request ):
  return render_to_response('home.html', { 'list': models.Resource.objects.all() } )

@login_required
def profile( request ):
  '''show resources that a user has purchased'''
  return render_to_response('registration/profile.html', { 'list': models.Purchase.objects.filter( purchaser=request.user ) }, context_instance=RequestContext(request) )

@login_required
def download( request, id ):
  '''display a resource'''
  resource = get_object_or_404( models.Resource, pk=id )
  try:
    purchased = models.Purchase.objects.get( resource=resource, purchaser=request.user )
    f = open( settings.RESOURCES_DIR + resource.location, 'r' )
    data = f.read()
    f.close()
    # return item as file
    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename=%s' % resource.location
    return response
  except models.Purchase.DoesNotExist:
    return render_to_response('purchase.html', { 'resource': resource, 'paypal_url': settings.PAYPAL_URL, 'paypal_email': settings.PAYPAL_EMAIL, 'paypal_return_url': settings.PAYPAL_RETURN_URL  }, context_instance=RequestContext(request) )

def purchased( request, uid, id ):
    resource = get_object_or_404( models.Resource, pk=id )
    user = get_object_or_404( User, pk=uid )
    if request.REQUEST.has_key('tx'):
      tx = request.REQUEST['tx']
      try:
        existing = models.Purchase.objects.get( tx=tx )
        return render_to_response('error.html', { 'error': "Duplicate transaction" }, context_instance=RequestContext(request) )
      except models.Purchase.DoesNotExist:
        result = paypal.Verify( tx )
        if result.success() and resource.price == result.amount(): # valid
          purchase = models.Purchase( resource=resource, purchaser=user, tx=tx )
          purchase.save()
          return render_to_response('purchased.html', { 'resource': resource }, context_instance=RequestContext(request) )
        else: # didn't validate
          return render_to_response('error.html', { 'error': "Failed to validate payment" }, context_instance=RequestContext(request) )
    else: # no tx
      return render_to_response('error.html', { 'error': "No transaction specified" }, context_instance=RequestContext(request) )
