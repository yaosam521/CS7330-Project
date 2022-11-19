from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('league/index.html')
    return HttpResponse(template.render())

def league(request):
    return HttpResponse("Welcome to the league page.")