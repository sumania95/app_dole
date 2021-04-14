from django.db import models
from django.db.models import Model, ForeignKey
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.utils import timezone

class Barangay(models.Model):
    name                    = models.CharField(max_length = 200)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.name)

gender = (
    ('1', 'Male',),
    ('2', 'Female',),
)

civil_status = (
    ('1', 'Single',),
    ('2', 'Married',),
    ('3', 'Widowed',),
    ('4', 'Separated',),
    ('5', 'Annulled',),
)

class Profile(models.Model):
    surname                 = models.CharField(max_length = 200)
    firstname               = models.CharField(max_length = 200)
    middlename              = models.CharField(max_length = 200,blank=True)
    ext_name                = models.CharField(max_length = 200,blank=True)
    date_of_birth           = models.DateField(default=timezone.now)
    gender                  = models.CharField(max_length=10,choices=gender)
    civil_status            = models.CharField(max_length=10,choices=civil_status)
    contact_no              = models.CharField(max_length = 11,blank=True)
    purok_street            = models.CharField(max_length = 200,blank=True)
    barangay                = models.ForeignKey(Barangay, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    @property
    def name(self):
        return str(self.surname) + ", " + str(self.firstname) + " " + str(self.middlename)

    @property
    def age(self):
        now = timezone.now()
        return int((now.date() - self.date_of_birth).days / 365.25)

    class Meta:
        ordering = ['surname','firstname','middlename']

class Programs(models.Model):
    description             = models.CharField(max_length = 200)
    sponsored_by            = models.CharField(max_length = 200,blank=True)
    date_from               = models.DateField(default=timezone.now)
    date_to                 = models.DateField(default=timezone.now)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Programs_Detail(models.Model):
    profile                 = models.ForeignKey(Profile, on_delete = models.CASCADE)
    programs                = models.ForeignKey(Programs, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Sms_Bluster(models.Model):
    profile                 = models.ForeignKey(Profile, on_delete = models.CASCADE)
    message                 = models.CharField(max_length = 1000)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Sms_Config(models.Model):
    ip_address              = models.CharField(max_length = 200)
    username                = models.CharField(max_length = 200)
    password                = models.CharField(max_length = 200)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)
