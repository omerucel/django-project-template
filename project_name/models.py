#-*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

"""
class Profile(models.Model):
    FEMALE = 0
    MALE = 1
    GENDER_CHOICES = (
        (FEMALE, 'female'),
        (MALE, 'male')
    )

    user = models.ForeignKey(User)
    facebook_id = models.BigIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='profiles', null=True, blank=True)
    gender = models.IntegerField(max_length=2, choices=GENDER_CHOICES, default=0)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile', args=[self.user.username])

    def get_image_url(self):
        if self.facebook_id > 0:
            return 'http://graph.facebook.com/%s/picture' %(self.facebook_id)
        else:
            return settings.STATIC_URL + 'img/profile.png'

    def get_large_image_url(self):
        if self.facebook_id > 0:
            return 'http://graph.facebook.com/%s/picture?type=large' %(self.facebook_id)
        else:
            return settings.STATIC_URL + 'img/profile.png'
"""