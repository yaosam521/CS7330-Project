# Lib
from Project7330_Fct import *
# Lib End

inLeagues={"lName": "test League","Comissioner": {"cName": "test commisioner", "SSN": 123456789}, "Teams":["A","B", "c", "D", "E", "F"]}
inLeagues2={"lName": "test League2","Comissioner": {"cName": "test commisioner", "SSN": 123456789}, "Teams":["B", "c", "D", "E", "F"]}

inTeams=[{"tName":"A","City": "testcity", "State": "testState", "Field": "A Home Field", "Rating": 12},
{"tName":"c","City": "testcity2", "State": "testState2", "Rating": -12.23},
{"tName":"B","City": "testcity2", "State": "testState2", "Rating": 3334},
{"tName":"D","City": "testcity2", "State": "testState2", "Rating": -34211.4},
{"tName":"E","City": "testcity2", "State": "testState2", "Rating": -34211.4},
{"tName":"F","City": "testcity2", "State": "testState2", "Rating": -34211.4}]

inSeasons={"lName": "test League", "sDate": "2020-10-01","eDate": "2020-06-20", "gNumber": 2, "sRules": {"win":3, "draw": 1, "lose":0}}
inSeasonsManu={"lName": "test League", "sDate": "2020-07-01","eDate": "2020-08-20", "gNumber": 2, "sRules": {"win":3, "draw": 1, "lose":0}}

inGames=[{"Record":{"A": None, "B": None}, "Field": "testfield", "Date":"2020-01-01"},
		 {"Record":{"C": None, "D": None}, "Field": "testfield", "Date":"2020-01-01"},
		 {"Record":{"A": None, "D": None}, "Field": "testfield", "Date":"2020-01-02"},
		 {"Record":{"B": None, "C": None}, "Field": "testfield", "Date":"2020-01-02"}]     # this should be maintained by the GUI to have a consistant data

autoInsertion= True

init_date()
	
for team in inTeams:
	insert_team(team)

#insert_league(inLeagues2)
insert_league(inLeagues, inSeasons, autoInsertion)

insert_season(inSeasons, autoInsertion, maxPerDay= 3, inGames=inGames)
#insert_season(inSeasonsManu, False, maxPerDay= 3)
insert_game_res("E", -12, "D", 0, t1Rating=-34211.4, replace=True)

move_team("A", "test League", "test League2", "2020-07-23")
season_info_query("test League", "2020-01-01", "2020-06-20")

game_info_query("c", "B")

team_info_query("c")


team_records_query("E")
league_info_query("test League")
league_champians_query("test League2")
rating_query("test League","2020-01-01","2020-06-20")
get_season_sets("test League12", 2)
get_date()
change_date("2022-1-30")