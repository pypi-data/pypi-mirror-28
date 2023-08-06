# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Book(models.Model):
    bookid = models.BigIntegerField(primary_key=True)
    bookname = models.CharField(max_length=200)
    bookprice = models.CharField(max_length=200)
    booksalescount = models.BigIntegerField()

    class Meta:
        ordering = ('bookid',)


class Appliances(models.Model):
    # bookid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    netbios_name = models.CharField(max_length=200, default='WIN')
    os_type = models.CharField(max_length=200, default='win32')


    # class Meta:
    #     ordering = ('bookid',)
