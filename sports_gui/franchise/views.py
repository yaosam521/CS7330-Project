from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())

def league(request):
    template = loader.get_template('league/league.html')
    return HttpResponse(template.render())

def date(request):
    template = loader.get_template('date/date.html')
    return HttpResponse(template.render())

def season(request):
    template = loader.get_template('season/season.html')
    return HttpResponse(template.render())
