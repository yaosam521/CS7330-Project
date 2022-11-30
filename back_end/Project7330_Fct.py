# Lib
import pymongo
from collections import defaultdict
from datetime import datetime, timedelta 													#used to modify/compare dates for games insertion
# Lib End 	

client = pymongo.MongoClient('localhost', 27017) 																# connect to client [localhost]
mydb=client["pp"]																			# Create Db called P1_T1

Leagues=mydb["Leagues"]																		# create a collection named Leagues
mydb.Leagues.create_index([('lName', pymongo.ASCENDING)], unique=True)						# create an index on lName

Teams=mydb["Teams"]																			# create a collection named Teams
mydb.Teams.create_index([('tName', pymongo.ASCENDING)], unique=True)						# create an index on tName

Seasons=mydb["Seasons"]																		# create a collection named Seasons
mydb.Seasons.create_index([('lName', pymongo.ASCENDING)], unique=False)						# create an index on lName (optimize queries)

Games=mydb["Games"]																			# create a collection named Games

Dates=mydb["Dates"]	

graph=defaultdict(list)
# what i have to do
# function to return pairs for sam manual games, fix insert games to work alone, merge the two insert season and league together
def insert_league(inLeagues, inSeasons, autoInsertion, inGames={}, maxPerDay=100, checkForTeams=False):# Done 
	# Start working on Leagues collection---------------------------------------------------------------------------------------------------
	if checkForTeams:
		for team in inLeagues["Teams"]:											
			if Teams.find_one({"tName":team}) == None:										# if one of the teams doesn't exist then abort
				print("insert_league: no such team called: ",team)
				___res="no such team called: "+team
				return ___res
				#return False

		if not Leagues.find_one({"Teams":{ "$in":inLeagues["Teams"]}}) == None:				# if one of the teams is already assigned then abort
			print("insert_league: already assigned team in collection")
			___res="already assigned team in collection"
			return ___res
			#return False																	# HINT: this check can be added to the previous loop to know which team is assigned

	try:
		LeagueId=Leagues.insert_one(inLeagues)	
		if insert_season(inSeasons, autoInsertion, inGames={}, maxPerDay=100, inTeamCall=True) == True:
			print("insert_league: League succ insertion")
			___res= "League succ insertion"
			#return True
		else:
			Leagues.delete_one({"_id":LeagueId.inserted_id})
			print("insert_league: Season problem, insertion aborted")
			___res= "Season problem"
			#return True
		
	except pymongo.errors.DuplicateKeyError:												# hundling the DuplicateKeyError exception
		print("insert_league: DuplicateKeyError handled Succecefully")
		___res="Duplicate League Name detected"
		return ___res
		#return False

def insert_team(inTeams):# Done
	# Start working on Teams collection-----------------------------------------------------------------------------------------------------

	try:
		Teams.insert_one(inTeams)	
		print("insert_team: Team succ insertion")
		___res="Team succ insertion"
		return  ___res
		#return True
	except pymongo.errors.DuplicateKeyError:												# hundling the DuplicateKeyError exception
		print("insert_team: DuplicateKeyError handled Succecefully")
		___res= "Duplicate Team Name detected"
		return ___res
		#return False

def insert_season(inSeasons, autoInsertion, inGames={}, maxPerDay=100, inTeamCall=False):# until insert games is done
	# Start working on Seasons collection---------------------------------------------------------------------------------------------------
	leagueInfo=Leagues.find_one({"lName":inSeasons["lName"]})

	if leagueInfo == None:																	# check that lName is correct
		print("insert_season: no such league")
		if inTeamCall== True:
			return False
		else:
			___res="no such league"
			return ___res

	c1, c2, c3=[{"$gte": inSeasons["sDate"]},{"$gte": inSeasons["eDate"]},{"$lt": inSeasons["sDate"]}] # Check for conflicts
	conflict= Seasons.find_one({"lName": inSeasons["lName"], "$nor": [{"$or": [{"$and":[{"sDate":c1},{"sDate":c2}]},{"$and":[{"sDate":c3},{"eDate":c3}]}]}]})
 	
	if conflict==None:																		# if no conflict then
		standingInitiator={}
		for team in leagueInfo["Teams"]:												# create the standing key/value
			standingInitiator.update({team: 0})	
		inSeasons.update({"Standing":standingInitiator})								# add it to our inSeason dict
		if autoInsertion==True or inGames != {}:
			inSeasons.update({"gInserted": True})
		else:
			inSeasons.update({"gInserted": False})
		SeasonId=Seasons.insert_one(inSeasons)											# insert season and retreive the id to rollback if prob in games										
		if insert_games(Seasons.find_one({"_id":SeasonId.inserted_id}), autoInsertion, inGames, leagueInfo["Teams"], maxPerDay, inSeasonCall=True) == True:
			print("insert_season: Season succ insertion")
			if inTeamCall== True:
				return True
			else:
				___res= "Season succ insertion"
				return ___res
			
		else: 																			# if games prob then remove the inserted season.
			Seasons.delete_one({"_id":SeasonId.inserted_id})
			if inTeamCall== True:
				return True
			else:
				___res="games problem"
				return ___res
	
	else:
		print("insert_season: Seasons Conflict Detected", end= ' ')
		print("already inserted Season between : %s -- %s " %(conflict["sDate"], conflict["eDate"]))
		if inTeamCall== True:
			return False
		else: 
			___res="insert_season: Seasons Conflict Detected "+"already inserted Season between : "+conflict["sDate"]+" -- "+conflict["eDate"]
			return ___res

def insert_games(Season_dict, autoInsertion, inGames={}, CompetingTeams=None, maxPerDay=100, inSeasonCall=False): 	# try to rearange your parameters/ remove the default for some
	# Start working on Games collection-----------------------------------------------------------------------------------------------------

	if autoInsertion == False :																	# requested Manual insertion.
		if inGames == {}:
			print("insert_game: user can't go to further then this date: %s without games insertion ;p" %(Season_dict["sDate"]))
			if inSeasonCall== True:
				return True
			else:
				___res="no game inserted"+"user can't go to further then this date:"+Season_dict["sDate"]+"without games insertion"
				return ___res

		for game in inGames:
			game.update({"SeasonId":Season_dict["_id"]})
		Games.insert_many(inGames)																# GUI responsibility to maintain the consistency
		print("insert_game: games succ insertion")
		if inSeasonCall== True:
			return True
		else:
			___res="games succ insertion"
			return ___res
	else:
		schedule={"1":[]}
		reqDays=1
		for gNumber in range(0,Season_dict["gNumber"]):											# start building the most compact schedule
			for i in range(0,len(CompetingTeams)):
				for j in range(i+1,len(CompetingTeams)):
					inserted=0
					for daynum in range(1,reqDays+1):
						if all(gameTeam not in schedule[str(daynum)] for gameTeam in [CompetingTeams[i],CompetingTeams[j]]) and len(schedule[str(daynum)])<(2*maxPerDay):
							schedule[str(daynum)].append(CompetingTeams[i])
							schedule[str(daynum)].append(CompetingTeams[j])
							inserted=1
							break
						
					if inserted==0:
						reqDays+=1
						schedule.setdefault(str(reqDays), [CompetingTeams[i],CompetingTeams[j]])# schedule builted succ
																								
		format = '%Y-%m-%d' 
		new_sDate=datetime.strptime(Season_dict["sDate"], format)								# those two lines are req to check available days number
		new_eDate=datetime.strptime(Season_dict["eDate"], format)
		if (new_eDate - new_sDate + timedelta(days=1)) > timedelta(days=reqDays):				# if we have enough
			AutoinGames=[]																		# prepare the overall dict
			SearchField= Teams.find_one({"tName":{"$in": CompetingTeams}, "Field":{"$exists": True}})
			if SearchField == None:
				AutoField="Auto Gen Field"
			else:
				AutoField=SearchField["Field"]
			for deltaDays, teamSets in schedule.items():
				for i in range(0,len(teamSets),2):
					AutoinGames.append( {"SeasonId":Season_dict["_id"],							# which field should we insert ... ask proff
					"Record":{teamSets[i]:None, teamSets[i+1]:None}, "Field": AutoField, "Date":str((new_sDate+timedelta(days=(int(deltaDays)-1))).date())} )
			
			Games.insert_many(AutoinGames)														# then inserte it 
			print("insert_game: games succ insertion")
			if inSeasonCall== True:
				return True
			else:
				___res="games succ insertion"
				return ___res
		else:																					# else if we don't have much days
			print("insert_game: No Solution -- add more days or increase the maxPerDay req")
			if inSeasonCall== True:
				return False
			else:
				___res="No Solution -- add more days or increase the maxPerDay req"
				return ___res

def insert_game_res(team1, score1, team2, score2, date, replace=False, t1Rating=None, t2Rating=None): # team info should be str and score/rating should be int "GUI" dateFormat= "%Y-%m-%d"
	game= Games.find_one({"Record."+team1: { "$exists": True }, "Record."+team2: { "$exists": True }, "Date":date})
	if game==None:
		print("insert_game_res: no such game")
		___res="no such game"
		return ___res
		#return False
	else:
		season= Seasons.find_one({'_id':game["SeasonId"]})										# to update the standing
		rollbackT1Stand, rollbackT2Stand= (0, 0)
		if game["Record"][team1]!= None:																	# if game already updated
			if replace == False:																# no replace cmd
				print("insert_game_res: game res already updated")
				___res="game res already updated"
				return ___res
				#return False
			else:																				# with replace cmd
				if game["Record"][team1] > game["Record"][team2]:													# prepare to rollback the previous standing
					rollbackT1Stand, rollbackT2Stand= (season["sRules"]["win"], season["sRules"]["lose"])
				elif game["Record"][team1] < game["Record"][team2]:
					rollbackT1Stand, rollbackT2Stand= (season["sRules"]["lose"], season["sRules"]["win"])
				else:
					rollbackT1Stand, rollbackT2Stand= (season["sRules"]["draw"], season["sRules"]["draw"])															
		flt={"_id": game["_id"]}
		newValue={ "$set": {"Record":{ team1: score1, team2: score2}} }
		Games.update_one(flt, newValue)																# either replacing of fresh insertion of G_res
		
		if score1 > score2 :																		# calculate the new added standing
			addedT1Stand, addedT2Stand= (season["sRules"]["win"], season["sRules"]["lose"])
		elif score1 < score2 :
			addedT1Stand, addedT2Stand= (season["sRules"]["lose"], season["sRules"]["win"])
		else:
			addedT1Stand, addedT2Stand= (season["sRules"]["draw"], season["sRules"]["draw"])

		standing=season["Standing"]																# fetch previous standing
		standing.update({team1: (standing[team1] +addedT1Stand -rollbackT1Stand), team2: (standing[team2] +addedT2Stand -rollbackT2Stand)}) # update it
		flt={"_id": season["_id"]}
		newValue={ "$set": {"Standing": standing} }
		Seasons.update_one(flt, newValue)														# write updates to the disk
		print("insert_game_res: game result inserted and standing updated")
		___res="game result inserted and standing updated "

		if t1Rating != None:																	# update T1 rating if desired 
			temp= Teams.find_one({"tName": team1})
			flt={"_id": temp["_id"]}
			Teams.update_one(flt, { "$set": {"Rating": t1Rating} })
			print("insert_game_res: team1 rating updated succ")
			___res+="team1 rating updated succ"

		if t2Rating != None:																	# update T2 rating if desired 
			temp= Teams.find_one({"tName": team2})
			flt={"_id": temp["_id"]}
			Teams.update_one(flt, { "$set": {"Rating": t2Rating} })
			print("insert_game_res: team2 rating updated succ")
			___res+="team2 rating updated succ"

		return ___res
		#return True																				# Fct ended succ

def move_team(team, fromLeague, toLeague, CurrentDate):	#Done										# parameters should be str dayFormat= "%Y-%m-%d"
	if Leagues.find_one({"lName": fromLeague, "Teams":  team}) == None or Leagues.find_one({"lName": toLeague}) == None: # check this record exist
		print("move_team: Move aborted: Wrong Info")
		___res= "Move aborted: Wrong Info"
		return ___res
		#return False

	if not Seasons.find_one({"lName":{"$in":[fromLeague, toLeague]}, "sDate":{"$lte": CurrentDate}, "eDate":{"$gte": CurrentDate}}) == None:
		print("move_team: Move aborted: in Season Conflict")
		___res= "Move aborted: in Season Conflict"
		return ___res
		#return False

	Leagues.update_one({"lName": fromLeague}, {"$pull":{"Teams": team}})
	Leagues.update_one({"lName": toLeague}, {"$push":{"Teams": team}})
	print("move_team: team moved Succecefully")
	___res="team moved Succecefully"
	return ___res
	#return True

#-----------------------------------------------------Added insertion------------------------------------------------------------------------------
def init_date():
	if Dates.find_one()==None:
		Dates.insert_one({"Current":"2022/01/01"})

def change_date(newDate):
	dateDict=Dates.find_one()
	if dateDict["Current"] > newDate :
		___res="you can't go backwards"
		print(___res)
		return ___res
	for noGSeason in Seasons.find({"gInserted": False}):
		if noGSeason["sDate"] < newDate:
			___res="conflict detected please insert games results for League: "+noGSeason["lName"]+" with season in: "+noGSeason["sDate"]+"---"+noGSeason[""]
			return ___res

	Dates.update_one({"_id":dateDict["_id"]}, {dateDict["Current"]: newDate})


#-----------------------------------------------------Added insertion------------------------------------------------------------------------------

#----------------------------------------------------------Querys----------------------------------------------------------------------------------

def season_info_query(league, sDate, eDate):	#Done												# parameters should be str dayFormat= "%Y-%m-%d"
	season=Seasons.find_one({"lName":league, "sDate":sDate, "eDate":eDate})
	if (season == None):
		print("season_query: No such season")
		___res="No such season"
		return ___res
		#return False

	sortedStanding= sorted(season["Standing"].items(), key=lambda x:x[1], reverse=True)			# this is the important var to be displayed into the GUI
	print("season_query: ", sortedStanding)							
	return sortedStanding	
	#return True

def game_info_query(team1, team2):																	# team1/2 should be str
	gQueryOrgnizer={}
	matchCondition={"$match": {"Record."+team1:{"$exists": 1}, "Record."+team2:{"$exists": 1}}}
	groupCondition={"$group": { "_id": "$SeasonId", "Games":{"$addToSet": {"game":(str('$'+"Record."+team1),str('$'+"Record."+team2),"$Date")}} }}
	for group in Games.aggregate([matchCondition, groupCondition]):									# Games are grouped per season here 
		season=Seasons.find_one({"_id":group["_id"]})
		gQueryOrgnizer.setdefault(season["lName"], [])
		for array in group["Games"]:								#array["game"][0]= t1Score, array["game"][1]= t2Score, array["game"][2]= Date
			gQueryOrgnizer[season["lName"]].append({array["game"][2]:[array["game"][0], array["game"][1]]})

	if gQueryOrgnizer == {}:
		print("game_query: No Such record")
		___res="No Such record"
		return ___res
		#return False
	else:
		print("game_query: ", gQueryOrgnizer)
		return gQueryOrgnizer
		#return True
			
def team_info_query(tName):
	team=Teams.find_one({"tName":tName})
	if team==None:
		print("team_info_query: No such record")
		___res="No such record"
		return ___res
		#return False
	else:
		team.pop("_id")
		print("team_info_query: ", team)
		return team
		#return True

def team_records_query(tName):																	# tName should be str
	tQueryOrgnizer={}
	matchCondition={"$match": {"Record."+tName:{"$ne": None}}}
	groupCondition={"$group": { "_id": "$SeasonId", "Games":{"$addToSet": "$Record"}, "count": {"$sum": {}} }}
	groupedPerSeason=Games.aggregate([matchCondition, groupCondition])
	adeedFields={"nWins": 0, "nDraws":0, "nLoses":0, "scoreSum":0, "opScoreSum":0}
	noRes=1
	for group in groupedPerSeason:																# Games are grouped per season here 
		if noRes==1: noRes=0
		group.update(adeedFields)
		season= Seasons.find_one({"_id": group["_id"]})											# to give a proper name for the dict _ids
		group.update({"_id":(season["lName"]+" "+season["sDate"]+"---"+season["eDate"]), "points":season["Standing"][tName]})
		for i in range(0,len(group["Games"])):													# in this loop we are seting info about the season games
			Scores=group['Games'].pop()															# pop one game scores								
			tScore=Scores.pop(tName)															# pop indexed team score
			opScore=list(Scores.values())[0]													# assign op score
			group["scoreSum"]+=tScore
			group["opScoreSum"]+=opScore
			if tScore > opScore:
				group["nWins"]+=1
			elif tScore == opScore:
				group["nDraws"]+=1
			else:
				group["nLoses"]+=1

		group.pop("Games")																		# Games should be empty so remove it
		print("team_records_query: ",group)

	if noRes==1:
		print("team_records_query: no played Games record")
		___res="no played Games record"
		return ___res
		#return False
	else:
		return group
		#return True


def league_info_query(lName):																	# lName should be str
	league=Leagues.find_one({"lName":lName})
	if league==None:
		print("league_info_query: No such record")
		___res="No such record"
		return ___res
		#return False
	else:
		league.pop("_id")
		league["SeasonsCount"]=Seasons.count_documents({"lName":lName})
		print("league_info_query: ", league)
		return league
		#return True

def league_champians_query(lName):																# lName should be str
	seasonsRes=Seasons.find({"lName":lName},{"sDate":1, "eDate":1, "Standing":1})
	noRes=1
	for season in seasonsRes:
		if noRes==1: noRes=0
		season["_id"]=season["sDate"]+"---"+season["eDate"]										# replace _id with appropriate date
		season.pop("sDate")																		# rmv both dates
		season.pop("eDate")
		champions= [{ key: value} for key, value in season["Standing"].items() if value == max(season["Standing"].values())]
		season.pop("Standing")
		season["Champions"]=champions															# insert Champians record to dict
		print("league_champians_query: ",season)
	if noRes==1:
		print("league_champians_query: no such record")
		___res="no such record"
		return ___res
		#return False
	else:
		return season
		#return True 
	
def RQ_longest_path(start, sequence):
	localSeq=sequence.copy()
	updated=0
	if start in graph.keys():																	# we still have edges to test
		for nextTeam in graph[start]: 
			if not nextTeam in localSeq:
				sequence=localSeq.copy()
				sequence.append(nextTeam)
				updatedSequence=RQ_longest_path(nextTeam, sequence)
				if updated==0:
					if len(updatedSequence) > len(localSeq): 
						updated=1
						nextSequance=updatedSequence
				else:
					if len(updatedSequence) > len(nextSequance):
						nextSequance=updatedSequence
		if updated == 1:
			return nextSequance																	# updated value return
		else:
			return localSeq																		# already mentioned
	else:
		return sequence 																		# no edge record in the graph
																				 
	

def rating_query(league, sDate, eDate):
	season=Seasons.find_one({"lName":league, "sDate":sDate, "eDate":eDate})
	if season==None:
		print("rating_query: No Such Season")
		___res="No Such Season"
		return ___res
	teamsCurrentRating={}
	for team in season["Standing"].keys():
		teamsCurrentRating[team]=Teams.find_one({"tName":team})["Rating"]						# get all teams current ratings
	
	graph.clear()
	for game in Games.find({"SeasonId":season["_id"]},{"Record":1}):
		record=list(game["Record"].items())
		team1, score1 = record[0]
		team2, score2 = record[1]
		if not score1== None:
			if score1 > score2 and teamsCurrentRating[team1] <= teamsCurrentRating[team2]:
				graph[team1].append(team2) 
			elif score1 < score2 and teamsCurrentRating[team1] >= teamsCurrentRating[team2]:
				graph[team2].append(team1)
	
	finalSequence=[]
	for team in graph.keys():
		sequence=RQ_longest_path(team, [team])
		if len(sequence) > len(finalSequence):
			finalSequence=sequence

	print("rating_query: ",finalSequence)
	return finalSequence
	#return True


