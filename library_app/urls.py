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
    ]