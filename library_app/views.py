# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import warnings

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin, deprecate_current_app
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.deprecation import RemovedInDjango21Warning
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import (TemplateView, ListView, CreateView, DetailView, DeleteView, FormView)

from OnlineLibrary import settings
from library_app.forms import SignupForm
from library_app.tokens import account_activation_token
from models import Book
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .forms import ReviewForm

from models import Book, Purchase
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
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

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['romance'] = len(Book.objects.filter(category=5))
        context['art'] = len(Book.objects.filter(category=1))
        context['bio'] = len(Book.objects.filter(category=3))
        context['child'] = len(Book.objects.filter(category=7))
        context['fantasy'] = len(Book.objects.filter(category=2))
        context['hist'] = len(Book.objects.filter(category=8))
        context['religion'] = len(Book.objects.filter(category=6))
        context['science'] = len(Book.objects.filter(category=4))
        return context


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


class MyBooksView(ListView):
    template_name = 'mybooks.html'
    model = Purchase
    context_object_name = 'books'


class CategoryListView(ListView):
    template_name = 'category.html'
    model = Book

    def get_queryset(self):
        return Book.objects.filter(category=self.kwargs['category'])


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

    else:
        return HttpResponse('Activation link is invalid!')


def add_review_to_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.id_book = book
            review.id_user = request.user
            review.save()
            return redirect(reverse(
                "book_details",
                kwargs={
                    "pk": book.pk
                }
            ))
    else:
        form = ReviewForm()
        return render(request, 'addreview.html', {'form': form})


class RecommendationListView(ListView):
    model = Book
    template_name = 'book.html'
    context_object_name = 'rbooks'

    def get_queryset(self):
        id_book = self.kwargs['pk']
        current_book = Book.objects.get(pk=id_book)
        others = Book.objects.all()
        books = []
        scored_books = []
        for other in others:
            if str(other.pk) != str(id_book):
                match = [(tag1, tag2) for tag1 in current_book.tag_set.all() for tag2 in other.tag_set.all() if tag1.tag_name == tag2.tag_name]
                scored_books.append((other, len(match)))
        scored_books = sorted(scored_books, key=lambda tup: (tup[1]), reverse=True)
        books = [book for (book, score) in scored_books][:6]
        return books

    def get_context_data(self, *args, **kwargs):
        context = super(RecommendationListView, self).get_context_data(*args, **kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['pk'])
        return context