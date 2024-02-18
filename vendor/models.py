from django.db import models
from django.contrib.auth.models import User
from store.models import *


class store_details(models.Model):
    store_vendor = models.ForeignKey(User, on_delete=models.SET_NULL,null = True)
    store_name = models.CharField(max_length=50)
    store_username = models.CharField(max_length=50)
    store_logo = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None,null=True,blank = True)
    store_images = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None,null=True, blank = True)
    store_date_created = models.DateTimeField(auto_now=True,)
    store_date_updated = models.DateTimeField(auto_now_add = True,null=True)

    def __str__(self):
        return str(self.store_username)
    