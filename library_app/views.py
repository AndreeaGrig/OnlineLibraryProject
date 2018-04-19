# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, CreateView, DetailView, DeleteView)
from models import Book
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


class BookListView(ListView):
    template_name = 'home.html'
    model = Book
    context_object_name = 'books'


class DetailsListView(DetailView):
    template_name = 'book.html'
    model = Book
    context_object_name = 'book'



