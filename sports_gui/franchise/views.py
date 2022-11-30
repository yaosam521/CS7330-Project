from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

import sys
sys.path.append('../')
from back_end.Project7330_Fct import *


def index(request):
    init_date()
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render())

def league(request):
    template = loader.get_template('league/league.html')
    return HttpResponse(template.render())

def leagueResult(request):
    lname = request.GET.get('lName')
    Cname = request.GET.get('cName')
    CSSN = request.GET.get('SSN')
    teams = request.GET.get('Teams')
    teams_arr = teams.split(',')
    inLeagues = {"lName": lname,"Comissioner": {"cName": Cname, "SSN": CSSN}, "Teams":teams_arr}
    sdate = request.GET.get('startDate')
    edate = request.GET.get('endDate')
    gnum = request.GET.get('gNumber')
    max = request.GET.get('maxGames')
    win = request.GET.get('wins')
    draw = request.GET.get('draw')
    loss = request.GET.get('loss')
    inSeasons = {"lName": lname, "sDate": sdate,"eDate": edate, "gNumber": int(gnum), "sRules": {"win":int(win), "draw": int(draw), "lose":int(loss)}}
    ai = request.GET.get('gameSchedule')
    if ai ==1 :
        autoInsertion=True
    else:
        autoInsertion= False
    params = {'result': insert_league(inLeagues,inSeasons,autoInsertion,maxPerDay=int(max))}
    return render(request, 'league/leagueResult.html', params)

def manual_insert_teams(request):
    lname = request.GET.get('lName')
    Cname = request.GET.get('cName')
    CSSN = request.GET.get('SSN')
    teams = request.GET.get('Teams')
    print(teams)
    teams_arr = teams.split(',')
    print(teams_arr)
    inLeagues = {"lName": lname,"Comissioner": {"cName": Cname, "SSN": CSSN}, "Teams":teams_arr}
    sdate = request.GET.get('startDate')
    edate = request.GET.get('endDate')
    gnum = request.GET.get('gNumber')
    max = request.GET.get('maxGames')
    win = request.GET.get('wins')
    draw = request.GET.get('draw')
    loss = request.GET.get('loss')
    inSeasons = {"lName": lname, "sDate": sdate,"eDate": edate, "gNumber": int(gnum), "sRules": {"win":int(win), "draw": int(draw), "lose":int(loss)}}
    ai = request.GET.get('gameSchedule')
    if ai ==1 :
        autoInsertion=True
    else:
        autoInsertion= False
        
    sets = get_season_sets(int(gnum),teams=teams_arr)
    params = {'result':lname,'pairs':sets,'length':len(sets)}
    return render(request, 'manual_insert_teams.html', params)

def mit_2(request):
    lname = request.GET.get('lName')
    print(lname)
    params = {'res': lname}
    return render(request, 'mit_2.html', params)


def teamResult(request):
    tname = request.GET.get('tName')
    city = request.GET.get('City')
    state = request.GET.get('State')
    field = request.GET.get('Field')
    rating = request.GET.get('Rating')
    inTeams={"tName":tname,"City":city, "State":state, "Field":field, "Rating":rating}
    params = {'result': insert_team(inTeams)}
    return render(request, 'league/teamResult.html', params)

def date(request):
    params = {'date':get_date()}
    return render(request, 'date/date.html', params)

def date2(request):
    newdate = request.GET.get('newdate')
    print(newdate)
    params = {'date':change_date(newdate)}
    return render(request, 'date/date2.html', params)

def season(request):
    template = loader.get_template('season/season.html')
    return HttpResponse(template.render())

def seasonCreated(request):
    lname = request.GET.get('lName')
    sdate = request.GET.get('sDate')
    edate = request.GET.get('eDate')
    ai = request.GET.get('gameSchedule')
    if ai =="1" :
        autoInsertion=True
    else:
        autoInsertion= False
    gnum = request.GET.get('gNumber')
    max = request.GET.get('maxGames')
    win = request.GET.get('wins')
    loss = request.GET.get('loss')
    draw = request.GET.get('draw')
    inSeasons={"lName": lname, "sDate": sdate,"eDate": edate, "gNumber": int(gnum), "sRules": {"win":int(win), "draw":int(draw), "lose":int(loss)}}
    params = {'result': insert_season(inSeasons,autoInsertion,maxPerDay=int(max),inGames={})}

    return render(request, 'season/seasonCreated.html', params)


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

def tq_result(request):
    tName = request.GET.get('teamQuery', 'default')
    print(tName)
    params = {'result': team_info_query(tName)}
    return render(request, 'queryResults/tq_result.html', params)

def lq_result(request):
    lq = request.GET.get('leagueQuery')
    params = {'result':league_info_query(lq)}
    return render(request, 'queryResults/lq_result.html', params)

def gq_result(request):
    t1 = request.GET.get('team1')
    t2 = request.GET.get('team2')
    print(t1, t2)
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
    t1 = request.GET.get('team1')
    t1s = request.GET.get('team1Score')
    t2 = request.GET.get('team2')
    t2s = request.GET.get('team2Score')
    t1rating = request.GET.get('team1Rating')
    t2rating = request.GET.get('team2Rating')
    re = request.GET.get('forceUpdate')
    if re == "1":
        replace = True
    else:
        replace = False
        
    if t1rating == "":
        t1rating = None
    else:
        t1rating = int(t1rating)
    if t2rating == "":
        t2rating = None
    else:
        t2rating = int(t2rating)
    params = {'result':insert_game_res(t1, int(t1s), t2, int(t2s), replace=replace, t1Rating=t1rating, t2Rating=t2rating)}
    return render(request, 'resultsEntered/resultsEntered.html', params)


def lq_champ_result(request):
    lName = request.GET.get('leagueQuery')
    res=league_champians_query(lName)
    params = {'champion': res}
    return render(request, "queryResults/lq_champ_result.html", params)

def tq_records_result(request):
    tname = request.GET.get('teamQuery')
    params = {'records': team_records_query(tname)}
    return render(request, "queryResults/tq_records_result.html", params)

def insert_games(request):
    template = loader.get_template('insert_games.html')
    return HttpResponse(template.render())

def game_result(request):
    lName = request.GET.get('lName')
    sDate = request.GET.get('sDate')
    eDate = request.GET.get('eDate')
    max = request.GET.get('#')
    params = {'result':insert_games_info(lName, sDate, eDate, True, inGames={}, maxPerDay=100)}
    return render(request, 'game_result.html', params)

def move_teams_2(request):
    team = request.GET.get('team')
    cL = request.GET.get('currentLeague')
    nL = request.GET.get('newLeague')
    date = request.GET.get('date')
    params = {'result': move_team(team,cL,nL,date)}
    return render(request, 'move_teams_2.html', params)