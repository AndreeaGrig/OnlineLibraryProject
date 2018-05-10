# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.test import TestCase
from django.test.client import Client


# Create your tests here.
from django.urls import reverse

from library_app.models import Review, Book


class MyTest(TestCase):
    def test_login(self):
        c = Client()
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)
        user = User.objects.create(username="myuser", password="parolamyuser!")
        self.client.login(username="myuser", password="parolamyuser!")
        response = c.post('/login/', {'username': 'myuser', 'password': 'parolamyuser!'})
        self.assertEqual(response.status_code, 200)

    def test_review_add(self):
        user = User.objects.create(username="myuser", password="parolamyuser!")
        self.client.login(username="myuser", password="parolamyuser!")
        book = Book.objects.create(title="Book1", author="Auth1", pdf="pdf1", pub_date=datetime.now(), add_date=datetime.now(), pub_house="ABC", category=1, type=1, price=0)
        review = Review.objects.create(text="This is a test review!", id_user=user,id_book=book, posted=datetime.now())
        data = {'text': "This is a test review!", 'posted': datetime.now(), 'id_book': book, 'id_user': user}
        response = self.client.post(reverse('add_review_to_book', kwargs={'pk': book.pk}), **data)
        self.assertEqual(response.status_code, 200)


