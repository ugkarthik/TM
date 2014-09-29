from django.conf.urls import patterns, url

from tm.views import Home, ShoppingBag

urlpatterns = patterns('tm.views',
                       url(r'^$', Home.as_view(), name='home'),
                       url(r'^shopping-bag/$', ShoppingBag.as_view(), name='shopping-bag'))