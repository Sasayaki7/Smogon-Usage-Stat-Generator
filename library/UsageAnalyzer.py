import json
import os
import re
import sys
from math import floor, ceil


filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__))))
	
f = open(os.path.join(filelocation, 'CONFIG.txt'))

directory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)

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
}
	
#constants that define the length of a tab and the max name length a pokemon can have
tabLength = 4
maxNameLength = 18

#adds tabs based on tabLength; defaults to max name length for a pokemon
def autoAddSpaces(item, maxSpace=maxNameLength):
	maxNeededSpaces = ceil(maxSpace+1)
	return item+' '*ceil(maxNeededSpaces-len(item))
	
#opens and creates a json of file content with title 'file'
#statlist is the megalist of all the pokemon uses so far
def readFile(file, statlist):
	data = open(file, 'r+')
	readData = json.load(data)
	statlist.extend(readData)
	return statlist
	
def cumulativeStats(tourType, rounds=False, startingRound=1, endingRound = None):
	stats = []
	tourDirectory = directory+tourType+'\\'
	if rounds:
		fileList = os.listdir(tourDirectory)
		highestRound = startingRound
		for files in fileList:
			round = int(re.search("\d+", files).group(0))
			if endingRound:
				if round <= endingRound and round >= startingRound:
					stats = readFile(tourDirectory+files, stats)
			else: 
				if round >= startingRound:
					stats = readFile(tourDirectory+files, stats)		
	else:
		fileList = os.listdir(tourDirectory)
		for files in fileList:
			stats = readFile(tourDirectory+files, stats)
	return stats
	
def addPartners(mon, team, dictionary):
	for pkmn in team:
		if pkmn != mon:
			if pkmn in dictionary:
				dictionary[pkmn] = dictionary[pkmn]+1
			else:
				dictionary[pkmn] = 1
	return dictionary
	
def compileStats(tourType, rounds=False, startingRound=1, endingRound=None):
	stats = cumulativeStats(tourType, rounds, startingRound, endingRound)
	usageStats = {}
	for replay in stats:
		t1 = [altFormDict[x] if x in altFormDict else x for x in replay['team1']]
		t2 = [altFormDict[x] if x in altFormDict else x for x in replay['team2']]
		if replay['winner'] == 1:
			for pokemon in t1:
				if pokemon in usageStats:
					use = usageStats[pokemon]
					use['usage'] = use['usage']+1
					use['W']=use['W']+1
					use['partners'] = addPartners(pokemon, t1, use['partners'])
					if pokemon in t2:
						use['mirror'] = use['mirror']+1
				else:
					usageStats[pokemon] = {'usage': 1, 'W': 1, 'mirror':0, 'partners' : addPartners(pokemon, t1, {})}
					if pokemon in t2:
						usageStats[pokemon]['mirror'] = 1
			for pokemon in t2:
				if pokemon in usageStats:
					use = usageStats[pokemon]
					use['usage'] = use['usage']+1
					usageStats[pokemon]['partners'] = addPartners(pokemon, t2, use['partners'])
				else:
					usageStats[pokemon] = {'usage': 1, 'W': 0, 'mirror':0,'partners' : addPartners(pokemon, t2, {})}
		else:
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

def writeStats(fileTitle, tourname, statArray, totalTeams, rounds = None, startingRound=1, endingRound=None):
	testList = sorted(statArray.items(), key=lambda kv: (kv[1]['usage'], kv[1]['W']), reverse = True)
	titleOfFile = fileTitle
	fileHeader = tourname+' Usage Stats'
	if rounds and int(startingRound) > 1:
		titleOfFile = fileTitle+'-From-Round-'+str(startingRound)
		fileHeader = fileHeader+' (From Round '+str(startingRound)+')'
	teamFile = titleOfFile+'-Team-Analysis'
	teamFileHeader = fileHeader+' Team Analysis'
	cumulativeStats = open(directory+'\\Usage Stats\\'+titleOfFile+'.txt', 'w+')
	cumulativeStats.write(fileHeader+'\n\n\n')
	cumulativeStats.write(autoAddSpaces('Rank', 4)+autoAddSpaces('Pokemon')+autoAddSpaces('Uses', 4)+autoAddSpaces('Use %', 8)+autoAddSpaces('Wins', 4)+autoAddSpaces('Win %', 8)+autoAddSpaces('Mirrors',7)+autoAddSpaces('Win % w/o Mirrors')+'\n')
	#cumulativeStats.write(autoAddSpaces('Rank', 4)+autoAddSpaces('Pokemon')+autoAddSpaces('Uses', 4)+autoAddSpaces('Use %', 8)+autoAddSpaces('Wins', 4)+autoAddSpaces('Win %', 8)+'Mirrors'+'\n')
	totalMons = 0
	lastRank = 0
	lastW = 0
	lastUsage = 0
	for i in range(len(testList)):
		if testList[i][1]['usage'] == lastUsage and testList[i][1]['W'] == lastW:
			cumulativeStats.write(autoAddSpaces(str(lastRank), 4))
		else:
			cumulativeStats.write(autoAddSpaces(str(i+1), 4))
			lastRank = i+1
			lastW = testList[i][1]['W']
			lastUsage = testList[i][1]['usage']
		#cumulativeStats.write(autoAddSpaces(testList[i][0])+autoAddSpaces(str(testList[i][1]['usage']), 4)+autoAddSpaces(str(round(testList[i][1]['usage']/totalTeams*100, 3))+'%', 8)+autoAddSpaces(str(testList[i][1]['W']), 4)+autoAddSpaces(str(round(testList[i][1]['W']/testList[i][1]['usage']*100, 3))+'%', 8)+str(testList[i][1]['mirror'])+'\n')
		cumulativeStats.write(autoAddSpaces(testList[i][0])+autoAddSpaces(str(testList[i][1]['usage']), 4)+autoAddSpaces(str(round(testList[i][1]['usage']/totalTeams*100, 3))+'%', 8)+autoAddSpaces(str(testList[i][1]['W']), 4)+autoAddSpaces(str(round(testList[i][1]['W']/testList[i][1]['usage']*100, 3))+'%', 8)+autoAddSpaces(str(testList[i][1]['mirror']), 7))
		usageWithoutMirrors = testList[i][1]['usage']-testList[i][1]['mirror']*2
		if usageWithoutMirrors == 0:
			cumulativeStats.write('N/A\n')
		else:
			cumulativeStats.write(str(round((testList[i][1]['W']-testList[i][1]['mirror'])/(testList[i][1]['usage']-testList[i][1]['mirror']*2)*100, 3))+'%\n')
		totalMons = totalMons+int(testList[i][1]['usage'])
	print("Stats written. Total Pokemon: "+str(totalTeams*12)+". Total teams: "+str(totalTeams))
	cumulativeStats.close()

def writeTeamStats(titleOfFile, tourname, statArray, totalTeams, rounds = None, startingRound = 1, endingRound = None):
	testList = sorted(statArray.items(), key=lambda kv: (kv[1]['usage'], kv[1]['W']), reverse = True)
	teamFile = titleOfFile+'-Team-Analysis'
	teamFileHeader = tourname+' Team Analysis'
	teamAnalysis = open(directory+'\\Usage Stats\\'+teamFile+'.txt', 'w+')
	teamAnalysis.write(teamFileHeader+'\n\n\n'+autoAddSpaces('')+'Common Partners\n')
	teamAnalysis.write(autoAddSpaces('Pokemon')+autoAddSpaces('#1')+autoAddSpaces('#2')+autoAddSpaces('#3')+autoAddSpaces('#4')+autoAddSpaces('#5')+autoAddSpaces('#6')+autoAddSpaces('#7')+autoAddSpaces('#8')+autoAddSpaces('#9')+autoAddSpaces('#10')+'\n')
	for i in range(len(testList)):
		usageRanking = sorted(testList[i][1]['partners'].items(), key=lambda kv: kv[1], reverse = True)
		teamAnalysis.write(autoAddSpaces(testList[i][0]))
		usageLength = len(usageRanking)
		for iterator in range(min(usageLength, 10)):
			teamAnalysis.write(autoAddSpaces(usageRanking[iterator][0]))
		teamAnalysis.write('\n'+autoAddSpaces(str(testList[i][1]['usage'])+' uses'))
		for iterator in range(min(usageLength, 10)):
			teamAnalysis.write(autoAddSpaces(str(round(usageRanking[iterator][1]/testList[i][1]['usage']*100, 2))+'%'))
		teamAnalysis.write('\n\n')
	teamAnalysis.close()
	
def outputStats(tourname, fileTitle, rounds=False, startingRound=1, endingRound=None):
	finalStats, totalTeams = compileStats(fileTitle, rounds, startingRound, endingRound)
	writeStats(fileTitle, tourname, finalStats, totalTeams, rounds, startingRound, endingRound)
	writeTeamStats(fileTitle, tourname, finalStats, totalTeams, rounds, startingRound, endingRound)

	
def main(fileTitle, tourname, rounds = False, startingRound=1, endingRound=None):
	outputStats(tourname, fileTitle, rounds or False, startingRound or 1, endingRound)
	
if __name__ == "__main__":
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		main(sys.argv[1], sys.argv[2], sys.argv[3])
		main(sys.argv[1], sys.argv[2], sys.argv[3], 4)
		main(sys.argv[1], sys.argv[2], sys.argv[3], 6)
		main(sys.argv[1], sys.argv[2], sys.argv[3], 8)
	elif len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	elif len(sys.argv)>6:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
	elif len(sys.argv) < 3:
		print('insufficient parameters, need at least 2')