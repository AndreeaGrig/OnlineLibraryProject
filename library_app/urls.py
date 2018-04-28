from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.BookListView.as_view(), name='home'),

    url(r'^book/(?P<pk>[0-9]+)/$',
        views.DetailsListView.as_view(), name='book_details'),

    url(r'^login',
        views.login_view,
        name="login"),

    url(r'^logout/$',
        views.logout_view,
        name="logout"),

    url(r'^mybooks/(?P<pk>[0-9]+)/$',
        views.MyBooksView.as_view(),
        name="my_books"),

    url(r'^category/(?P<category>[1-8]{1})/$',
        views.CategoryListView.as_view(),
        name='category_list'),

    url(r'^book/(?P<pk>[0-9]+)/review/$',
        views.add_review_to_book,
        name='add_review_to_book'),
    ]
