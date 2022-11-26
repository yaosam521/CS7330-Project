from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())

def league(request):
    template = loader.get_template('league/league.html')
    return HttpResponse(template.render())

def date(request):
    template = loader.get_template('date/date.html')
    return HttpResponse(template.render())
