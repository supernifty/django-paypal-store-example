from django.db import models
from django.contrib.auth.models import User

class Resource( models.Model ):
  '''resources available for purchase'''
  name = models.CharField( max_length=250 )
  location = models.CharField( max_length=250 )
  price = models.DecimalField( decimal_places=2, max_digits=7 )

class Purchase( models.Model ):
  '''purchases'''
  resource = models.ForeignKey( Resource )
  purchaser = models.ForeignKey( User )
  purchased_at = models.DateTimeField(auto_now_add=True)
  tx = models.CharField( max_length=250 )
