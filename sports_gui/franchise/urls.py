from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('league/', views.league, name = 'league'),
    path('date/', views.date, name = 'date'),
    path('date2/', views.date2, name = 'date2'),
    path('season/', views.season, name = 'season'),
    path('seasonCreated/', views.seasonCreated, name = 'seasonCreated'),
    path('league_query/',views.league_query, name='league_query'),
    path('team_query/',views.team_query, name='team_query'),
    path('game_query/',views.game_query, name='game_query'),
    path('ratings_query/',views.ratings_query, name='ratings_query'),
    path('season_query/',views.season_query, name='season_query'),
    path('results/',views.results, name='results'),
    path('move_teams/',views.move_teams, name='move_teams'),
    
    path('resultsEntered/', views.resultsEntered, name = 'resultsEntered'),
    path('leagueResult/', views.leagueResult, name = 'leagueResult'),
    path('teamResult/', views.teamResult, name = 'teamResult'),
    path('manual_insert_teams/',views.manual_insert_teams, name='manual_insert_teams'),
    path('manual_result/', views.manual_result, name = 'manual_result'),
    path('insert_games/', views.insert_games, name = 'insert_games'),
    path('game_result/', views.game_result, name = 'game_result'),
    path('move_teams_2/', views.move_teams_2, name = 'move_teams_2'),
    #query URLS
    path('tq_result/', views.tq_result, name = 'tq_result'),
    path('lq_result/', views.lq_result, name = 'lq_result'),
    path('gq_result/', views.gq_result, name = 'gq_result'),
    path('sq_result/', views.sq_result, name = 'sq_result'),
    path('tq_records_result/', views.tq_records_result, name = 'tq_records_result'),
    path('lq_champ_result/', views.lq_champ_result, name = 'lq_champ_result'),
    path('rq_result/', views.rq_result, name = 'rq_result')
]