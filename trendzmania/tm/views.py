from django.shortcuts import render
from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = 'tm/home.html'

class ShoppingBag(TemplateView):
    template_name = 'tm/shopping-bag.html'
