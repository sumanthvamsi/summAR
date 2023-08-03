# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class team(models.Model):
    member=models.CharField(max_length=20,default=True)
    memberGen=models.CharField(max_length=20,default=True)
    memid=models.IntegerField(default=True)
    age=models.IntegerField(default=True)
    adhaar=models.IntegerField(default=True)
    location=models.CharField(max_length=20,default=True)
    job=models.CharField(max_length=20,default=False)
    description=models.TextField(max_length=50,default=False)

    def __str__(self):
        return self.member
    
class forum(models.Model):
    user_name=models.CharField(max_length=20,default=True)
    answer=models.TextField(max_length=500,default=True)

    def __str__(self):
        return self.user_name

class buy_energy(models.Model):
    cus_name=models.CharField(max_length=20,default=None)
    meter_id=models.IntegerField(default="",blank=True,null=True)
    quantity=models.IntegerField(default="",blank=True,null=True)
    energy_price=models.IntegerField(default="",blank=True,null=True)

    def __str__(self):
        return self.cus_name
    

class capture(models.Model):
    date=models.IntegerField(default=True)

    def __str__(self):
        return self.date
    
class cloud(models.Model):
    p_num=models.IntegerField(default=True)
    p_name=models.CharField(default=True,max_length=10)


    def __str__(self):
        return self.p_name
    
class ipfs(models.Model):
    f_hash=models.TextField(default=True,max_length=100)

    def __str__(self):
        return self.f_hash
    
class meter_analytics(models.Model):
    res=models.CharField(default=True,max_length=5)

    def __str__(self):
        return self.res
    

class summary_file(models.Model):
    p_name=models.CharField(default=False,max_length=10)
    p_num=models.BigIntegerField(default=True)

    def _str_(self):
        return self.p_name
    
class meta_video(models.Model):
    pv_name=models.CharField(default=False,max_length=10)
    pv_num=models.BigIntegerField(default=True)

    def _str_(self):
        return self.pv_name