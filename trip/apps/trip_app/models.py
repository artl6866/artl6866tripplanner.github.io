from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime
from ..app_one.models import *
from . models import *

# Create your models here.



class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destinationlength'] = "Please enter destination."
        if len(postData['description']) < 1:
            errors['descriptionlength'] = "Please enter description."
        if len(postData['startdate']) < 1:
            errors['startdatelength'] = "Please enter start date."
        elif postData['startdate'] < str(datetime.now()):
            errors['paststart'] = "Please choose future date."
        if len(postData['end_date']) < 1:
            errors['end_datelength'] = "Please enter end date."
        elif postData['end_date'] < str(datetime.now()):
            errors['pastend'] = "Please choose future date."
        if postData['startdate'] > postData['end_date']:
            errors['errordate'] = "Start date should be before the end date."

        return errors
        

class Trip(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.TextField()
    startdate = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user_create = models.ForeignKey(User, related_name = 'destination_created', on_delete = 'models.CASCADE')
    user_travel = models.ManyToManyField(User, related_name= 'user_destination')
    objects = TripManager()
