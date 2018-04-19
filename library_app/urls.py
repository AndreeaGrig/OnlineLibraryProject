from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.MyTemplateView.as_view(), name='home'),
    ]