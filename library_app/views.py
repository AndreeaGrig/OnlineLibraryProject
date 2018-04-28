# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.views import View
from django.views.generic import (TemplateView, ListView, CreateView, DetailView, DeleteView)

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


class DetailsListView(DetailView):
    template_name = 'book.html'
    model = Book
    context_object_name = 'book'


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


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')

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

