from django.conf.urls import url, include
from social import extra

from . import views
from library_app import views as core_views

urlpatterns = [
    url(r'^$',
        views.BookListView.as_view(), name='home'),

    url(r'^book/(?P<pk>[0-9]+)/$',
        views.RecommendationListView.as_view(), name='book_details'),

    url(r'^login',
        views.login_view,
        name="login"),

    url(r'^auth/',
        include('social_django.urls', namespace='social')),


    url(r'^logout/$',
        views.logout_view,
        name="logout"),


    url(r'^signup/$',
        views.signup,
        name='signup'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate,
        name='activate'),

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
