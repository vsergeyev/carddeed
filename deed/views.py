# -*- coding: utf-8 -*-

#===============================================================================
# Carddeed project Views file
# 2008-01-31: Sergeyev V.V.
#===============================================================================

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django import newforms as forms
from django.newforms import form_for_instance, form_for_model, save_instance, form_for_fields
from django.conf import settings

import datetime
import time
import math
import os
from random import randint as rint

from deed.models import CardItem, Document, Enterprise, AtmDocument, AtmCardItem

#------------------------------------------------------------------------------
def cmp_docs(a,b):
    ""
    if not a.doc_date: return -1
    if not b.doc_date: return 1
    if a.doc_date < b.doc_date: return -1
    if a.doc_date == b.doc_date: 
        if a.id < b.id: return -1
        if a.id == b.id: return 0
        if a.id > b.id: return 1
    if a.doc_date > b.doc_date: return 1

#------------------------------------------------------------------------------
def default_renderer(request, template_name, items):
    """
    Поскольку нам нужно постоянно отображать список документов слева, то проще это делать в одной функции.
    Может еще чего добавится в следующей версии :)  
    """
    
    docs = Document.objects.all().order_by("-id")
    atm_docs = AtmDocument.objects.all().order_by("-id")
    
    all_docs = list(docs) + list(atm_docs)
    
    all_docs.sort(cmp_docs, reverse=True)
    
    content = {
               "docs": all_docs,
              }
    content.update(items)
    
    return render_to_response("%s.html" % template_name, content, context_instance=RequestContext(request))

#------------------------------------------------------------------------------
def user_index(request):
    "Display index page"
    return default_renderer(request, "user_index", {})

#------------------------------------------------------------------------------ 
def search(request, kind='number'):
    "Search by card number and by Holder name"
    if request.method == "POST":
        keyword = request.POST['search_number']
        if kind == 'number':
            items = CardItem.objects.filter(number__icontains=keyword).order_by("name")
            atm_items = AtmCardItem.objects.filter(number__icontains=keyword).order_by("name")
        else:
            items = CardItem.objects.filter(name__icontains=keyword).order_by("name")
            atm_items = AtmCardItem.objects.filter(name__icontains=keyword).order_by("name")
    else:
        items = None

    return default_renderer(request, "search", {"items": items, "atm_items": atm_items})

#Note: all these "stuff" functions are universal. They may operate with any object/objects, that has only Id/Name.
#------------------------------------------------------------------------------
def show_stuff_list(request, model_name):
    "Displays list of Organizations."
    items = eval(model_name).objects.all().order_by('name')
    return default_renderer(request, "stuff_list", {'items':items})

#------------------------------------------------------------------------------
def new_stuff_item(request, model_name):
    "New Organization"
    ItemForm = form_for_model(eval(model_name))
    new_item = None
    
    if request.method == "POST":
        item_form = ItemForm(request.POST)
    
        if item_form.is_valid():
            new_item = item_form.save(True)
    
    return HttpResponseRedirect("/stuff/%s/list/" % model_name)
 
#------------------------------------------------------------------------------ 
def delete_stuff_item(request, model_name):
    "Delete Organization"
    if request.method == "POST":
        for key in request.POST:
            item = eval(model_name).objects.get(pk=key)
            item.delete()
    
    return HttpResponseRedirect("/stuff/%s/list/" % model_name)

#------------------------------------------------------------------------------
def edit_stuff_item(request, model_name):
    "Edit Organization"
    if request.method == "POST":
        item = eval(model_name).objects.get(pk=request.POST['id'])
        item.name = request.POST['name']
        item.save()
    
    return HttpResponseRedirect("/stuff/%s/list/" % model_name)

#------------------------------------------------------------------------------ 
def new_doc(request):
    "Creates a new document"
    
    DocForm = form_for_model(Document)
    
    if request.method == "POST":
        doc_form = DocForm(request.POST)
        if doc_form.is_valid():
            # сохраняем новый документ
            doc = doc_form.save(True)
            
            # теперь распарсим строки документа
            i = 1
            while True:
                if request.has_key("card_name%i" % i):
                    card_name = request.POST["card_name%i" % i]
                    if card_name=="":
                        break
                    card_number = request.POST["card_number%i" % i]
                    card_credit = request.POST["card_credit%i" % i]
                    card_note = request.POST["card_note%i" % i]
                    have_pin = False
                    if request.has_key("have_pin%i" % i):
                        have_pin = True
                    
                    # сохраняем карточку
                    new_item = CardItem(name=card_name, number=card_number, credit_number=card_credit, have_pin=have_pin, note=card_note, doc=doc)
                    new_item.save()
                    
                    # индекс следующей строки
                    i=i+1
            
        return HttpResponseRedirect("/edit_docs/%s/" % doc.id)
    else:
        doc_form = DocForm()
        #items = Enterprise.objects.all()
    
    return default_renderer(request, "card_deed", {'doc_form':doc_form})

#------------------------------------------------------------------------------
# sorry mom for copy/paste, haven't any ideas
def new_atm_doc(request):
    "Creates a new ATM Document"
    
    DocForm = form_for_model(AtmDocument)
    
    if request.method == "POST":
        doc_form = DocForm(request.POST)
        if doc_form.is_valid():
            # сохраняем новый документ
            doc = doc_form.save(True)
            
            # теперь распарсим строки документа
            i = 1
            while True:
                if request.has_key("card_name%i" % i):
                    card_name = request.POST["card_name%i" % i]
                    if card_name=="":
                        break
                    card_number = request.POST["card_number%i" % i]
                    arrival_date = request.POST["arrival_date%i" % i]
                    delivery_date = request.POST["delivery_date%i" % i]
                    card_note = request.POST["card_note%i" % i]
                    
                    # сохраняем карточку
                    new_item = AtmCardItem(name=card_name, number=card_number, delivery_date=delivery_date, arrival_date=arrival_date, note=card_note, doc=doc)
                    new_item.save()
                    
                    # индекс следующей строки
                    i=i+1
            
        return HttpResponseRedirect("/edit_docs_atm/%s/" % doc.id)
    else:
        doc_form = DocForm()
    
    return default_renderer(request, "atm_doc", {'doc_form':doc_form})

#------------------------------------------------------------------------------ 
def edit_doc(request, doc_id):
    "Edit document"
    doc = Document.objects.get(pk=doc_id)
    DocForm = form_for_instance(doc)
    if request.method == "POST":
        doc_form = DocForm(request.POST)
        if doc_form.is_valid():
            # сохраняем новый документ
            doc = doc_form.save(True)
            save_instance(doc_form, doc, True)
            
            # теперь распарсим строки документа
            i = 1
            while True:
                if request.has_key("card_name%i" % i):
                    card_name = request.POST["card_name%i" % i]
                    if card_name=="":
                        break
                    card_number = request.POST["card_number%i" % i]
                    card_credit = request.POST["card_credit%i" % i]
                    card_note = request.POST["card_note%i" % i]
                    have_pin = False
                    if request.has_key("have_pin%i" % i):
                        have_pin = True
                    
                    if request.has_key("card_id%i" % i):
                        card_id = request.POST["card_id%i" % i]
                        item = CardItem.objects.get(pk=card_id)
                        item.name = card_name
                        item.number = card_number
                        item.credit_number = card_credit
                        item.have_pin = have_pin
                        item.note=card_note
                        item.save()
                    else:
                        # сохраняем новую карточку
                        new_item = CardItem(name=card_name, number=card_number, credit_number=card_credit, have_pin=have_pin, note=card_note, doc=doc)
                        new_item.save()
                    
                    # индекс следующей строки
                    i=i+1
            
        return HttpResponseRedirect("/edit_docs/%s/" % doc.id)
    else:
        doc_form = DocForm()
        items = CardItem.objects.filter(doc=doc).order_by("id")
    
    content = {
               "doc": doc,
               "doc_form": doc_form,
               "items": items,
               }
    
    return default_renderer(request, "card_edit", content)

#------------------------------------------------------------------------------ 
def edit_atm_doc(request, doc_id):
    "Edit ATM Document"
    doc = AtmDocument.objects.get(pk=doc_id)
    DocForm = form_for_instance(doc)
    if request.method == "POST":
        doc_form = DocForm(request.POST)
        if doc_form.is_valid():
            # сохраняем новый документ
            doc = doc_form.save(True)
            save_instance(doc_form, doc, True)
            
            # теперь распарсим строки документа
            i = 1
            while True:
                if request.has_key("card_name%i" % i):
                    card_name = request.POST["card_name%i" % i]
                    if card_name=="":
                        break
                    card_number = request.POST["card_number%i" % i]
                    arrival_date = request.POST["arrival_date%i" % i]
                    delivery_date = request.POST["delivery_date%i" % i]
                    card_note = request.POST["card_note%i" % i]
                    
                    if request.has_key("card_id%i" % i):
                        card_id = request.POST["card_id%i" % i]
                        item = AtmCardItem.objects.get(pk=card_id)
                        item.name = card_name
                        item.number = card_number
                        item.arrival_date = arrival_date
                        item.delivery_date = delivery_date
                        item.note=card_note
                        item.save()
                    else:
                        # сохраняем новую карточку
                        new_item = AtmCardItem(name=card_name, number=card_number, delivery_date=delivery_date, arrival_date=arrival_date, note=card_note, doc=doc)
                        new_item.save()
                    
                    # индекс следующей строки
                    i=i+1
            
        return HttpResponseRedirect("/edit_docs_atm/%s/" % doc.id)
    else:
        doc_form = DocForm()
        items = AtmCardItem.objects.filter(doc=doc).order_by("id")
    
    content = {
               "doc": doc,
               "doc_form": doc_form,
               "items": items,
               }
    
    return default_renderer(request, "atm_edit", content)

#------------------------------------------------------------------------------ 
def delete_doc(request, doc_id, model_name="Document"):
    "Delete both Documents and AtmDocuments"
    doc = eval(model_name).objects.get(pk=doc_id)
    doc.delete()
    return HttpResponseRedirect("/")

#------------------------------------------------------------------------------ 
def print_doc(request, doc_id, model_name="Document"):
    "Printing document"
    
    doc = eval(model_name).objects.get(pk=doc_id)
    items = doc.items.all().order_by("id") #CardItem.objects.filter(doc=doc).order_by("id")
    template = "print"
    if model_name == "AtmDocument":
       template = "atm_print"

    content = {
               "doc": doc,
               "items": items,
               }
    return default_renderer(request, template, content)

#------------------------------------------------------------------------------
def syncdb(request):
    ""
    from pysqlite2 import dbapi2 as sqlite
    
    db = sqlite.connect('carddeed.db')
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS "deed_atmdocument" (
                    "id" integer NOT NULL PRIMARY KEY,
                    "number" varchar(10) NOT NULL,
                    "doc_date" date NULL,
                    "enterprise_id" integer NULL
                   );""")
    cur.execute("""CREATE TABLE IF NOT EXISTS "deed_atmcarditem" (
                    "id" integer NOT NULL PRIMARY KEY,
                    "name" varchar(200) NOT NULL,
                    "number" varchar(16) NOT NULL,
                    "arrival_date" varchar(20) NOT NULL,
                    "delivery_date" varchar(20) NOT NULL,
                    "note" varchar(200) NOT NULL,
                    "doc_id" integer NOT NULL REFERENCES "deed_atmdocument" ("id")
                   );""")
    db.commit()
    
    return HttpResponse("<h1>ok</h1>")

#------------------------------------------------------------------------------ 
