# -*- coding: utf-8 -*-

#===============================================================================
# Carddeed project Models declarations file
# 2008-01-31: Sergeyev V.V.
#===============================================================================

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from random import randint as rint
import os
import fnmatch
import re

#------------------------------------------------------------------------------ 
class Enterprise(models.Model):
    "Enterprises, to use in Documents"
    name = models.CharField(maxlength="200", blank=True)
    
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        
    class Admin:
        pass

#------------------------------------------------------------------------------ 
class Document(models.Model):
    """
    Document:
    number/date, enterprise
    and rows with CardItems
    """
    number = models.CharField(maxlength="10", blank=True)
    doc_date = models.DateField(blank=True, null=True)
    enterprise = models.ForeignKey(Enterprise, verbose_name = "Организация", blank=True, null=True)
    
    def __str__(self):
        return "Акт №%s от %s" % (self.number, self.doc_date)

    def __unicode__(self):
        return "Акт №%s от %s" % (self.number, self.doc_date)
    
    def get_absolute_url(self):
        return "/edit_docs/%i/" % self.id

    class Meta:
        ordering = ['-doc_date']
        verbose_name = "Акт приёмки-передачи карточек"
        verbose_name_plural = "Акты приёмки-передачи карточек"
        
    class Admin:
        list_display = ('doc_date', 'number', 'enterprise')

#------------------------------------------------------------------------------
class CardItem(models.Model):
    "Item - person's full name and account number. Used in Documents"
    name = models.CharField("ФИО", maxlength="200", blank=True)
    number = models.CharField("Номер зарпл. карты", maxlength="16", blank=True)
    credit_number = models.CharField("Номер кред. карты", maxlength="16", blank=True)
    have_pin = models.BooleanField("Есть код")
    note = models.CharField("Примечание", maxlength="200", blank=True)
    doc = models.ForeignKey(Document, verbose_name = "Акт", related_name='items')
    
    def __str__(self):
        return self.number

    def __unicode__(self):
        return self.number

    class Meta:
        ordering = ['number']
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"
        
    class Admin:
        list_display = ('doc', 'name', 'number', 'credit_number', 'have_pin')

#------------------------------------------------------------------------------ 
class AtmDocument(models.Model):
    """
    ATM Document:
    number/date, enterprise
    and rows with CardItems
    """
    number = models.CharField(maxlength="10", blank=True)
    doc_date = models.DateField(blank=True, null=True)
    enterprise = models.ForeignKey(Enterprise, verbose_name = "Организация", blank=True, null=True)
    
    def __str__(self):
        return "Банкоматный акт №%s от %s" % (self.number, self.doc_date)

    def __unicode__(self):
        return "Банкоматный акт №%s от %s" % (self.number, self.doc_date)
    
    def get_absolute_url(self):
        return "/edit_docs_atm/%i/" % self.id
    
    class Meta:
        ordering = ['-doc_date']
        verbose_name = "Банкоматный акт"
        verbose_name_plural = "Банкоматные акты"
        
    class Admin:
        list_display = ('doc_date', 'number', 'enterprise')

#------------------------------------------------------------------------------
class AtmCardItem(models.Model):
    "ATM Item - person's full name, card number, arrival date and delivery date. Used in ATM Documents"
    name = models.CharField("ФИО", maxlength="200", blank=True)
    number = models.CharField("Номер карты", maxlength="16", blank=True)
    arrival_date = models.CharField("Дата приёма", maxlength="20", blank=True)
    delivery_date = models.CharField("Дата выдачи", maxlength="20", blank=True)
    note = models.CharField("Примечание", maxlength="200", blank=True)
    doc = models.ForeignKey(AtmDocument, verbose_name = "Банкоматный акт", related_name='items')
    
    def __str__(self):
        return self.number

    def __unicode__(self):
        return self.number

    class Meta:
        ordering = ['number']
        verbose_name = "Банкоматная Карточка"
        verbose_name_plural = "Банкоматные Карточки"
        
    class Admin:
        list_display = ('doc', 'name', 'number', 'arrival_date', 'delivery_date')
   
#------------------------------------------------------------------------------ 
