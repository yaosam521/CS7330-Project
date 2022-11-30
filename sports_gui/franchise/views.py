from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

import sys
sys.path.append('../')
from back_end.Project7330_Fct import *


def index(request):
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())

def league(request):
    template = loader.get_template('league/league.html')
    return HttpResponse(template.render())

def leagueResult(request):
    abc = request.GET.get('lName', 'cName', 'SSN', 'Teams')
    # lname = request.GET.get('lName', 'default')
    # Cname = request.GET.get('cName', 'default')
    # CSSN = request.GET.get('SSN', 'default')
    # teams = request.GET.get('Teams', 'default')
    # params = {'lName':lname, 'CName': Cname, 'SSN': CSSN, 'teams' : teams}
    params = {'result': insert_league(abc)}     # dispute here.
    return render(request, 'league/leagueResult.html', params)

def date(request):
    template = loader.get_template('date/date.html')
    return HttpResponse(template.render())

def season(request):
    template = loader.get_template('season/season.html')
    return HttpResponse(template.render())

def league_query(request):
    template = loader.get_template('queries/league_query.html')
    return HttpResponse(template.render())

def team_query(request):
    template = loader.get_template('queries/team_query.html')
    return HttpResponse(template.render())

def game_query(request):
    template = loader.get_template('queries/game_query.html')
    return HttpResponse(template.render())

def ratings_query(request):
    template = loader.get_template('queries/ratings_query.html')
    return HttpResponse(template.render())

def season_query(request):
    template = loader.get_template('queries/season_query.html')
    return HttpResponse(template.render())

def results(request):
    template = loader.get_template('results.html')
    return HttpResponse(template.render())

def move_teams(request):
    template = loader.get_template('move_teams.html')
    return HttpResponse(template.render())

def teamEntry(request):
    tName = request.GET.get('teamQuery', 'default')
    print(tName)
    params = {'result': team_info_query(tName)}
    return render(request, 'queryResults/teamEntry.html', params)

def lq_result(request):
    lq = request.GET.get('leagueQuery')
    params = {'result':league_info_query(lq)}
    return render(request, 'queryResults/lq_result.html', params)

def gq_result(request):
    t1 = request.GET.get('team1')
    t2 = request.GET.get('team2')
    params = {'result':game_info_query(t1,t2)}
    return render(request, 'queryResults/gq_result.html', params)
    
def sq_result(request):
    name = request.GET.get('lName')
    sdate = request.GET.get('sDate')
    edate = request.GET.get('eDate')
    params = {'result':season_info_query(name, sdate, edate)}
    return render(request, 'queryResults/sq_result.html', params)

def rq_result(request):
    name = request.GET.get('lName')
    sdate = request.GET.get('sDate')
    edate = request.GET.get('eDate')
    params = {'result':rating_query(name,sdate,edate)}
    return render(request, 'queryResults/rq_result.html', params)

def resultsEntered(request):
    teamName1 = request.GET.get('team1', 'default')
    teamScore1 = request.GET.get('team1Score', 'default')
    teamName2 = request.GET.get('team2', 'default')
    teamScore2 = request.GET.get('team2Score', 'default')
    params = {'team1':teamName1, 'team1Score':teamScore1, 'team2':teamName2, 'team2Score':teamScore2}
    print(teamName1, teamScore1, teamName2, teamScore2)
    return render(request, 'resultsEntered/resultsEntered.html', params)

def manual_insert_teams(request):
    template = loader.get_template('manual_insert_teams.html')
    return HttpResponse(template.render())

def insert_games(request):
    template = loader.get_template('insert_games.html')
    return HttpResponse(template.render())

def move_teams_2(request):
    team = request.GET.get('team')
    cL = request.GET.get('currentLeague')
    nL = request.GET.get('newLeague')
    date = request.GET.get('date')
    params = {'result': move_team(team,cL,nL,date)}
    return render(request, 'move_teams_2.html', params)