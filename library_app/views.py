# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import View
from django.views.generic import (TemplateView, ListView, CreateView, DetailView, DeleteView)


from models import Book, Purchase
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from forms import LoginForm


def login_view(request):
    context = {}
    if request.method == 'GET':
        form = LoginForm
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                login(request=request,
                      user=user)
                return redirect('home')
            else:
                context['error_message'] = 'Wrong username or password!'
    context['form'] = form
    return render(request, 'login.html', context)


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')


class BookListView(ListView):
    template_name = 'home.html'
    model = Book
    context_object_name = 'books'


class DetailsListView(DetailView):
    template_name = 'book.html'
    model = Book
    context_object_name = 'book'


class MyBooksView(ListView):
    template_name = 'mybooks.html'
    model = Purchase
    context_object_name = 'books'


class CategoryListView(ListView):
    template_name = 'category.html'
    model = Book

    def get_queryset(self):
        return Book.objects.filter(category=self.kwargs['category'])

