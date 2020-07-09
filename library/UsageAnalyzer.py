#TODO: Patch potential bug, input check somewhere (main? outputStats?).


import json
import os
import re
import sys
from math import floor, ceil


filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__))))
#sets filelocation to be 2 directories above this file. Used to obtain banlists and other modules hidden in the folder. Equivalent to ../.. in Linux
	
f = open(os.path.join(filelocation, 'CONFIG.txt'))
#Accesses and opens up the CONFIG file. Self explanatory

directory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)
#Obtains the directory information from ROOT_DIRECTORY from config, and sets it to "directory". 

#a dictionary of all alternate forms that don't matter competitively.
altFormDict = {'Keldeo-Resolute': 'Keldeo',
	'Gastrodon-East': 'Gastrodon',
	'Vivillon-Archipelago': 'Vivillon',
	'Vivillon-Continental': 'Vivillon',
	'Vivillon-Elegant': 'Vivillon',
	'Vivillon-Fancy': 'Vivillon',
	'Vivillon-Garden': 'Vivillon',
	'Vivillon-Highplains': 'Vivillon',
	'Vivillon-Icysnow': 'Vivillon',
	'Vivillon-Jungle': 'Vivillon',
	'Vivillon-Pokeball': 'Vivillon',
	'Vivillon-Marine': 'Vivillon',
	'Vivillon-Meadow': 'Vivillon',
	'Vivillon-Modern': 'Vivillon',
	'Vivillon-Monsoon': 'Vivillon',
	'Vivillon-Ocean': 'Vivillon',
	'Vivillon-Polar': 'Vivillon',
	'Vivillon-River': 'Vivillon',
	'Vivillon-Sandstorm': 'Vivillon',
	'Vivillon-Savanna': 'Vivillon',
	'Vivillon-Sun': 'Vivillon',
	'Vivillon-Tundra': 'Vivillon',
	'Pikachu-Alola': 'Pikachu',
	'Pikachu-Hoenn': 'Pikachu',
	'Pikachu-Kalos': 'Pikachu',
	'Pikachu-Original': 'Pikachu',
	'Pikachu-Partner': 'Pikachu',
	'Pikachu-Sinnoh': 'Pikachu',
	'Pikachu-Unova': 'Pikachu',
	'Pikachu-Belle': 'Pikachu',
	'Pikachu-Cosplay': 'Pikachu',
	'Pikachu-Libre': 'Pikachu',
	'Pikachu-PhD': 'Pikachu',
	'Pikachu-Pop-Star': 'Pikachu',
	'Pikachu-Rock-Star': 'Pikachu',
	'Basculin-Blue-Striped': 'Pikachu',
	'Araquanid-Totem': 'Araquanid',
	'Gumshoos-Totem': 'Gumshoos',
	'Kommo-o-Totem': 'Kommo-o',
	'Lurantis-Totem': 'Lurantis',
	'Marowak-Alola-Totem': 'Marowak-Alola',
	'Mimikyu-Totem': 'Mimikyu',
	'Raticate-Alola-Totem': 'Raticate-Alola',
	'Salazzle-Totem': 'Salazzle',
	'Togedemaru-Totem': 'Togedemaru',
	'Vikavolt-Totem': 'Vikavolt',
	'Burmy-Sandy': 'Burmy',
	'Burmy-Trash': 'Burmy',
	'Shellos-East': 'Shellos',
	'Pichu-Spiky-eared': 'Pichu',
	'Raticate-Alola-Totem': 'Raticate-Alola',
	'Salazzle-Totem': 'Salazzle',
	'Togedemaru-Totem': 'Togedemaru',
	'Vikavolt-Totem': 'Vikavolt',
	'Burmy-Sandy': 'Burmy',
	'Burmy-Trash': 'Burmy',
	'Shellos-East': 'Shellos',
	'Pichu-Spiky-eared': 'Pichu',
	'Deerling-Summer': 'Deerling',
	'Deerling-Autumn': 'Deerling',
	'Deerling-Winter': 'Deerling',
	'Sawsbuck-Summer': 'Sawsbuck',
	'Sawsbuck-Autumn': 'Sawsbuck',
	'Sawsbuck-Winter': 'Sawsbuck',
	'Genesect-*': 'Genesect',
	'Genesect-Burn': 'Genesect',
	'Genesect-Chill': 'Genesect',
	'Genesect-Douse': 'Genesect',
	'Genesect-Shock': 'Genesect',
	'Flabébé-Ue': 'Flabébé',
	'Flabébé-Ange': 'Flabébé',
	'Flabébé-Ite': 'Flabébé',
	'Flabébé-Llow': 'Flabébé',
	'Floette-Blue': 'Floette',
	'Floette-Orange': 'Floette',
	'Floette-White': 'Floette',
	'Floette-Yellow': 'Floette',
	'Florges-Blue': 'Florges',
	'Florges-Orange': 'Florges',
	'Florges-White': 'Florges',
	'Florges-Yellow': 'Florges',	
	'Furfrou-Heart': 'Furfrou',
	'Furfrou-Star': 'Furfrou',
	'Furfrou-Diamond': 'Furfrou',
	'Furfrou-Debutante': 'Furfrou',	
	'Furfrou-Matron': 'Furfrou',
	'Furfrou-Dandy': 'Furfrou',
	'Furfrou-Lareine': 'Furfrou',
	'Furfrou-Kabuki': 'Furfrou',	
	'Furfrou-Pharaoh': 'Furfrou',
	'Minior-Blue': 'Minior',
	'Minior-Orange': 'Minior',
	'Minior-Green': 'Minior',
	'Minior-Yellow': 'Minior',
	'Alcremie-Rainbow-Swirl': 'Alcremie',
    	'Alcremie-Ruby-Cream': 'Alcremie',
    	'Alcremie-Mint-Cream': 'Alcremie',
    	'Alcremie-Matcha-Cream': 'Alcremie',
    	'Alcremie-Salted-Cream': 'Alcremie',
    	'Alcremie-Lemon-Cream': 'Alcremie',
    	'Alcremie-Ruby-Swirl': 'Alcremie',
    	'Alcremie-Caramel-Swirl': 'Alcremie',
    	'Alcremie-Vanilla-Cream': 'Alcremie',
    	'Toxtricity-Low-Key': 'Toxtricity',
    	'Polteageist-Antique': 'Polteageist',
    	'Zarude-Dada': 'Zarude',
}
	
#constants that define the length of a tab and the max name length a pokemon can have
tabLength = 4 #Smogon Code tabs out at 4 spaces .
maxNameLength = 22 #Longest pokemon name that aren't contained in altFormDict is 18 characters long.



#adds tabs based on tabLength; defaults to max name length for a pokemon
#Parameters: String item, integer maxSpace (optional)
#Returns a string with appropriate numbers of spaces after Parameter String item. 
def autoAddSpaces(item, maxSpace=maxNameLength):
	maxNeededSpaces = ceil(maxSpace+1)
	return item+' '*ceil(maxNeededSpaces-len(item))
	
	
	
	
"""opens and creates a json of file content with the title stored in the variable @file
Parameters: String file, String statList
statlist is a massive array of all stripped down replaysidentified in the tournament round files, saved as a dictionary file. This method appends all the stripped down replays contained in @file and appends it to statList, then returns statlist.
"""
def readFile(file, statlist):
	
	data = open(file, 'r+')
	#opens up @file
	
	readData = json.load(data)
	#The data should be saved in a .json format, so we unpack the .json
	
	statlist.extend(readData)
	#statList now contains all the pokemon from the file, and returns statList to the caller
	
	return statlist
	
	
	
	
"""Searches all the files titled for given @tourType from round @startingRound to @endingRound, analyzes the stripped down replays, and returns the list of all teams used in @tourType
#Parameters: String tourType, boolean rounds, int startingRound, int endingRound
#tourType identifies the directory relating to tournament titled @tourType.
#rounds should be set to True if the tournament occurs across multiple threads. Usually reserved for seasonals.
If we only want part of a mutliple-thread tournament, the startingRound and endingRound can be specified. Default starts at 1, and ends at final round.
returns array stats which contains the list of all the teams and pokemon, along with which team.
"""
def cumulativeStats(tourType, rounds=False, startingRound=1, endingRound = None):
	stats = []
	#Initialize stats with an empty array
	
	tourDirectory = directory+tourType+'\\'
	#Identifies the folder where all the teams and winners for the tournament are stored.
	
	if rounds:
		#If this is a multi-thread tournament, we check that the rounds are within the range of endingRound and startingRound, if specified.
		
		fileList = os.listdir(tourDirectory)
		#Gets a list of all the files stored in the folder, and iterates through
		for files in fileList:
			
			round = int(re.search("\d+", files).group(0))
			#Gets the round number which is stored by default at the end of each file to compare with @startingRound and @endingRound
"""			#Potential bug if tourType also contains numbers; need to address using anchors"""
			
			if endingRound:
			#Differentiates if @endingRound is defined or not.
			
				if round <= endingRound and round >= startingRound:
					stats = readFile(tourDirectory+files, stats)
					#Extends stats by the information stored in files
		
			else: 
				if round >= startingRound:
					stats = readFile(tourDirectory+files, stats)	
					#Extends stats by the information stored in files					
	else:
		#If this is a single thread tournament, or if we simply want all the files, we just get all the teams stored in the directory.
		fileList = os.listdir(tourDirectory)
		
		for files in fileList:
			#Grab all the files, put all the teams into array stats, and return all the pokemon/teams stored in the files as array stats
			stats = readFile(tourDirectory+files, stats)
			
	return stats
	
	
	
	
"""Tallies up all the teammates on @team for a given @mon in Dictionary @dictionary and returns @dictionary
Useful for TeamAnalysis files
Parameters: String mon, Array team, Dictionary dictionary
Returns Dictionary dictionary
"""
def addPartners(mon, team, dictionary):
	for pkmn in team:
		#Iterates through all the pokemon in the team
	
		if pkmn != mon:
			#A pokemon cannot be a partner of itself (unless species claus is busted ofc, but lets not think about that.)
		
			if pkmn in dictionary:
				#If pkmn is already defined in the dictionary, we increment the counter by 1 
				dictionary[pkmn] = dictionary[pkmn]+1
			
			else:
				#Otherwise we initialize the total teammate count for pkmn to 1.
				dictionary[pkmn] = 1
	
	return dictionary
	
	
	
	
"""
Turns all the team stats for a given tournament @tourType, and returns a dictionary @usageStats containing # of uses, # of wins, # of mirrors for each pokemon for the given tournament, starting from @startingRound up to @endingRound
@usageStats takes the form {pokemonName: {'usage': integer, 'W': integer, 'mirror': integer, 'partners': {dictionaryOfAllTeammates}}}
If the tournament has rounds, outputs usage stats starting from round 4, 6, and 8 as well, if valid
Parameters: String tourType, boolean rounds, int startingRound, int endingRound
Returns Dictionary usageStats which contains all the uses, wins and mirrors for all pokemon used in tournament, and the total number of matches as an integer.
"""
def compileStats(tourType, rounds=False, startingRound=1, endingRound=None):
	stats = cumulativeStats(tourType, rounds, startingRound, endingRound)
	#Takes all of the stripped down replays from all the files relating to tourType.
	
	usageStats = {}
	#Initialize a blank dictionary usageStats which holds a Dictionary of all the wins, mirrors, and uses for each pokemon. 
	#Dictionary Format is {PokemonName: DictionaryOfStats}
	#DictionaryOfStats is defined for each pokemon, and has four keys: 'usage', 'W', 'mirror', 'partners'.
	#usage, W, and mirror are all integers, while partners is another dictionary.
	#W stands for Wins.
	
	for replay in stats:
		#Iterates through every stripped down replay contained in stats
		
		t1 = [altFormDict[x] if x in altFormDict else x for x in replay['team1']]
		t2 = [altFormDict[x] if x in altFormDict else x for x in replay['team2']]
		#The raw teams from the replay are parsed in this loop to ensure alternate forms which have no competitive significance aren't counted as different pokemon in usage stats.
		#t1 and t2 are arrays which contain the pokemon that player1 and player2, respectively, used in the replay
		
		if replay['winner'] == 1:
			#Because the 'W' stat is affected by who won the match, we distinguish between who won the match. 1 is the case where Player1 wins the match
			
			for pokemon in t1:
				#For each pokemon in team1, we increment its usage, winrate, and increment each teammate for that pokemon. 
				
				if pokemon in usageStats:
				#Make sure that @pokemon is defined in usageStats.
					
					use = usageStats[pokemon]
					#@use is a local variable that holds the dictionary of stats for each pokemon.
					use['usage'] = use['usage']+1
					use['W']=use['W']+1
					
					use['partners'] = addPartners(pokemon, t1, use['partners'])
					#Increments the teammate counter for each teammate by 1.
					
					if pokemon in t2:
					#If both players used the pokemon, increase the mirror counter. This is not repeated in the second loop so we don't double count mirror matchups 
						use['mirror'] = use['mirror']+1
				else:
					#If @pokemon does not yet exist in @usageStats, we initialize it with 1 usage, 1 W, and all its partners set to 1.
					usageStats[pokemon] = {'usage': 1, 'W': 1, 'mirror':0, 'partners' : addPartners(pokemon, t1, {})}
			
					if pokemon in t2:
						#Make sure to account for mirrors here too.
						usageStats[pokemon]['mirror'] = 1
		
			for pokemon in t2:
			#Repeat above steps for team 2, except we don't double-count mirrors and don't give player2's pokemons a win, since they lost.
				if pokemon in usageStats:
					use = usageStats[pokemon]
					use['usage'] = use['usage']+1
					usageStats[pokemon]['partners'] = addPartners(pokemon, t2, use['partners'])
				else:
					usageStats[pokemon] = {'usage': 1, 'W': 0, 'mirror':0,'partners' : addPartners(pokemon, t2, {})}
	
		else:
			#If player2 won the battle, we repeat the same steps, except we give player2's pokemons a win and not player1's.
			for pokemon in t2:
				if pokemon in usageStats:
					use = usageStats[pokemon]
					use['usage'] = use['usage']+1
					use['W']=use['W']+1
					use['partners'] = addPartners(pokemon, t2, use['partners'])
					if pokemon in t1:
						use['mirror'] = use['mirror']+1
				else:
					usageStats[pokemon] = {'usage': 1, 'W': 1, 'mirror':0,'partners' : addPartners(pokemon, t2, {})}
					if pokemon in t1:
						usageStats[pokemon]['mirror']=1
			for pokemon in t1:
				if pokemon in usageStats:
					use = usageStats[pokemon]
					use['usage'] = use['usage']+1
					usageStats[pokemon]['partners'] = addPartners(pokemon, t1, use['partners'])
				else:
					usageStats[pokemon] = {'usage': 1, 'W': 0, 'mirror':0, 'partners' : addPartners(pokemon, t1, {})}
	print("Compiled stats")
	return usageStats, len(stats)*2
	#stats should be the number of replays. Each replay has 2 teams, so the total number of teams would be twice the number of replays.



"""
Takes a dictionary of pokemon usage stats returned by the compileStats function in parameter @statArray, and outputs a file of usageStats titled @fileTitle.
Parameters: String fileTitle, string header, Dictionary statArray, int totalTeams, boolean rounds, int startingRound, int endingRound
Returns Nothing.
Get mished Yoda2798
@fileTitle is the name of the output file.
@header is the First line written in the File 
@statArray is a dictionary returned by the compileStats function.
@totalTeams is the total number of teams contained in @statArray.
@rounds, @startingRound, and @endingRound are optional parameters to be set if the tournament is a multi-thread tournament, and only interested in certain rounds of a multithread tournament, such as a seasonal. 
"""
def writeStats(fileTitle, header, statArray, totalTeams, rounds = None, startingRound=1, endingRound=None):
	testList = sorted(statArray.items(), key=lambda kv: (kv[1]['usage'], kv[1]['W']), reverse = True)
	#Creates an array of keys for the Dictionary @statArray, sorted by use, followed by Win rate, in descending order (i.e. Most used pokemon with highest winrate is first, least used pokemon with lowest winrate comes last)

	titleOfFile = fileTitle
	#Why did I do this.

	fileHeader = header+' Usage Stats'
	#Defines fileHeader to be @header with Usage Stats appended on. 

	if rounds and int(startingRound) > 1:
		#@titleOfFile and @fileHeader becomes different depending on the round.
		titleOfFile = fileTitle+'-From-Round-'+str(startingRound)
		fileHeader = fileHeader+' (From Round '+str(startingRound)+')'

	#Creates new file titled @titleOfFile in directory/UsageStats, and write in the header, 3 open lines, and the Usage stat titles.
	#autoAddSpaces helps space outs the columns nicely.
	
	#Checks to make sure file doesn't already exist.... We don't want to unintentionally overwrite existing data.
	if os.path.isfile(directory+'\\Usage Stats\\'+titleOfFile+'.txt'): 
	
		overwrite = "n"
		#Declaring here to avoid variable not being defined.
	
		#While loop in case the new title also exists. Keeps looping until new filename doesn't exist or overwriting is permitted.
		while os.path.isfile(directory+'\\Usage Stats\\'+titleOfFile+'.txt') and overwrite != "y":
			overwrite = input(directory+'\\Usage Stats\\'+titleOfFile+'.txt already exists. Overwrite? (Y/N): ')
			#Get user input on if we are allowed to proceed or not.
			
			#If we don't want to overwrite file, we rename to something else.
			if overwrite.lower() != "y":
				titleOfFile = titleOfFile+"(1)"
				print("New file Name: "+ titleOfFile)
			
	cumulativeStats = open(directory+'\\Usage Stats\\'+titleOfFile+'.txt', 'w+')
	cumulativeStats.write(fileHeader+'\n\n\n')
	cumulativeStats.write(autoAddSpaces('Rank', 4)+autoAddSpaces('Pokemon')+autoAddSpaces('Uses', 4)+autoAddSpaces('Use %', 8)+autoAddSpaces('Wins', 4)+autoAddSpaces('Win %', 8)+autoAddSpaces('Mirrors',7)+autoAddSpaces('Win % w/o Mirrors')+'\n')
	#cumulativeStats.write(autoAddSpaces('Rank', 4)+autoAddSpaces('Pokemon')+autoAddSpaces('Uses', 4)+autoAddSpaces('Use %', 8)+autoAddSpaces('Wins', 4)+autoAddSpaces('Win %', 8)+'Mirrors'+'\n')
	
	totalMons = 0
	#Tally of total number of Pokemon
	
	lastRank = 0
	#Variable that keeps track of the ranking in case of same usage stats with same winrate
	
	lastW = 0
	#Variable that keeps track of the # of wins the previous iteration pokemon had.	
	
	lastUsage = 0
	#Variable that keeps track of the # of uses the previous iteration pokemon had.	


	#The machinery starts here. Iterates through all the keys in @testList in chronological order, and writes the usage stat onto a file.
	for i in range(len(testList)):
		
		#First thing that we spit out is the ranking on the usage stats. Makes sure that the usage stat and winrate arent the exact same as the previous pokemon.
		if testList[i][1]['usage'] == lastUsage and testList[i][1]['W'] == lastW:
			#If usage stat and winrate are the exact same as the previous pokemon, we rank the pokemon the same as the previous pokemon.
			cumulativeStats.write(autoAddSpaces(str(lastRank), 4))
			
		else:
			#Otherwise, we rank the pokemon normally.
			cumulativeStats.write(autoAddSpaces(str(i+1), 4))
			
			#Updates lastRank, lastW and lastUsage accordingly, in case the next pokemon has the same usage stats and winrate.
			lastRank = i+1			
			lastW = testList[i][1]['W']
			lastUsage = testList[i][1]['usage']
			
		#cumulativeStats.write(autoAddSpaces(testList[i][0])+autoAddSpaces(str(testList[i][1]['usage']), 4)+autoAddSpaces(str(round(testList[i][1]['usage']/totalTeams*100, 3))+'%', 8)+autoAddSpaces(str(testList[i][1]['W']), 4)+autoAddSpaces(str(round(testList[i][1]['W']/testList[i][1]['usage']*100, 3))+'%', 8)+str(testList[i][1]['mirror'])+'\n')
		cumulativeStats.write(autoAddSpaces(testList[i][0])+autoAddSpaces(str(testList[i][1]['usage']), 4)+autoAddSpaces(str(round(testList[i][1]['usage']/totalTeams*100, 3))+'%', 8)+autoAddSpaces(str(testList[i][1]['W']), 4)+autoAddSpaces(str(round(testList[i][1]['W']/testList[i][1]['usage']*100, 3))+'%', 8)+autoAddSpaces(str(testList[i][1]['mirror']), 7))
		#Outputs the Pokemon name, # of uses, Usage %, # of wins, Win %, and # of Mirrors.
		
		#Calculates the win rate if mirrors did not exist.
		usageWithoutMirrors = testList[i][1]['usage']-testList[i][1]['mirror']*2
		
		#Prevents divide by zero errors
		if usageWithoutMirrors == 0:
			cumulativeStats.write('N/A\n')
		
		#Otherwise output the win rate if mirrors didn't exist normally.
		else:
			cumulativeStats.write(str(round((testList[i][1]['W']-testList[i][1]['mirror'])/(testList[i][1]['usage']-testList[i][1]['mirror']*2)*100, 3))+'%\n')
			
		#Updates the total number of pokemon that were used.	
		totalMons = totalMons+int(testList[i][1]['usage'])
		
	#Outputs on console the number of pokemon and number of teams in this iteration.
	print("Stats written. Total Pokemon: "+str(totalTeams*12)+". Total teams: "+str(totalTeams))
	
	cumulativeStats.close()
	#Make sure to close out the file.



"""
Takes a dictionary of pokemon usage stats returned by the compileStats function in parameter @statArray, and outputs a file of Pokemon and its common partners titled @titleOfFile.
Parameters: String titleOfFile, string header, Dictionary statArray, int totalTeams, boolean rounds, int startingRound, int endingRound
Returns Nothing.
Get mished Yoda2798
@fileTitle is the name of the output file.
@header is the First line written in the File 
@statArray is a dictionary returned by the compileStats function.
@totalTeams is the total number of teams contained in @statArray.
@rounds, @startingRound, and @endingRound are optional parameters to be set if the tournament is a multi-thread tournament, and only interested in certain rounds of a multithread tournament, such as a seasonal. 
"""
def writeTeamStats(titleOfFile, header, statArray, totalTeams, rounds = None, startingRound = 1, endingRound = None):
	
	testList = sorted(statArray.items(), key=lambda kv: (kv[1]['usage'], kv[1]['W']), reverse = True)
	#Creates an array of keys for the Dictionary @statArray, sorted by use, followed by Win rate, in descending order (i.e. Most used pokemon with highest winrate is first, least used pokemon with lowest winrate comes last)

	teamFile = titleOfFile+'-Team-Analysis'
	teamFileHeader = header+' Team Analysis'
	#Defines file title and header for the teamAnalysis file. 

	#Creates teamAnalysis file and appends header and title, as well as the top 10 columns
	teamAnalysis = open(directory+'\\Usage Stats\\'+teamFile+'.txt', 'w+')
	teamAnalysis.write(teamFileHeader+'\n\n\n'+autoAddSpaces('')+'Common Partners\n')
	teamAnalysis.write(autoAddSpaces('Pokemon')+autoAddSpaces('#1')+autoAddSpaces('#2')+autoAddSpaces('#3')+autoAddSpaces('#4')+autoAddSpaces('#5')+autoAddSpaces('#6')+autoAddSpaces('#7')+autoAddSpaces('#8')+autoAddSpaces('#9')+autoAddSpaces('#10')+'\n')
	
	#The machinery starts here. Iterates through all the keys in @testList in chronological order, and writes the most common partners onto file @teamAnalysis.
	for pokemon in range(len(testList)):
	
		usageRanking = sorted(testList[pokemon][1]['partners'].items(), key=lambda kv: kv[1], reverse = True)
		#Sorts the @partners parameter in order from most used partner to least used partner
		
		teamAnalysis.write(autoAddSpaces(testList[pokemon][0]))
		#Outputs the name of the Pokemonin question
		
		usageLength = len(usageRanking)
		#Obtains the number of other pokemon that this pokemon was used with. 
		
		for iterator in range(min(usageLength, 10)):
			#Due to file length, limited to top 10 pokemon
			
			teamAnalysis.write(autoAddSpaces(usageRanking[iterator][0]))
			#Adds space after Pokemon
			
		teamAnalysis.write('\n'+autoAddSpaces(str(testList[pokemon][1]['usage'])+' uses'))
		#Writes top 10 pokemon (or max # of pokemon used as partners.) 
		
		for iterator in range(min(usageLength, 10)):
			teamAnalysis.write(autoAddSpaces(str(round(usageRanking[iterator][1]/testList[pokemon][1]['usage']*100, 2))+'%'))
			#Writes Percentage that the partner appears alongside pokemon 
			
		teamAnalysis.write('\n\n')
	teamAnalysis.close()
	#Make sure to close out the teamAnalysis file




	
"""
Function that links the compileStats function to the writeStats and writeTeamStats functions
Obtains the returned values from the compileStats function and outputs usage stat files and team analysis.
Parameters: String tourname, string fileTitle, boolean rounds, int startingRound, int endingRound
Returns nothing.
"""	
def outputStats(tourname, fileTitle, rounds=False, startingRound=1, endingRound=None):
	finalStats, totalTeams = compileStats(fileTitle, rounds, startingRound, endingRound)
	writeStats(fileTitle, tourname, finalStats, totalTeams, rounds, startingRound, endingRound)
	writeTeamStats(fileTitle, tourname, finalStats, totalTeams, rounds, startingRound, endingRound)




"""
main function exists purely so it can be called directly from the terminal. Functionally identical to outputStats function 
"""
def main(fileTitle, tourname, rounds = False, startingRound=1, endingRound=None):
	outputStats(tourname, fileTitle, rounds or False, startingRound or 1, endingRound)
	
	
"""
Overloading functions when this function is called via terminal
"""
if __name__ == "__main__":
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	
	elif len(sys.argv) == 4:
		#When the rounds value is anything besides False, and no other parameters are given, we assume usage stats for an entire seasonal is desired.
		#For seasonals, we output stats for the entire seasonal, from Round 4 (early rounds may have teams that can be discounted), from Round 6 and Round 8 (to account for more prestigous games)
		main(sys.argv[1], sys.argv[2], sys.argv[3])
		main(sys.argv[1], sys.argv[2], sys.argv[3], 4)
		main(sys.argv[1], sys.argv[2], sys.argv[3], 6)
		main(sys.argv[1], sys.argv[2], sys.argv[3], 8)
		
	elif len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	elif len(sys.argv)>6:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
		#Function can only take a maximum of 6 parameters
	
	elif len(sys.argv) < 3:
		#Because @fileTitle and @tourname are required parameters, we call an error if less parameters are given.
		print('insufficient parameters, need at least 2')
