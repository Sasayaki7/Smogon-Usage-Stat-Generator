#TODO: Check searcForMegas function to see if we can improve functionality.

import requests
import re
import unicodedata
import sys
import json
import os

winnerRegex = re.compile('(?<=\|win\|).+')
teamRegex = re.compile('(?<=clearpoke\n).+?(?=teampreview)', re.DOTALL)
t1Regex = re.compile('(?<=p1\|).+?(?=[,\|])')
t2Regex = re.compile('(?<=p2\|).+?(?=[,\|])')
megaRegex = re.compile('(?<=\|\-mega\|p)\d.:[^\|]+\|[^\|]+\|[^\|]+')
#Bunch of regex to distinguish key information from the replay text. winner shows player 1 or player 2, team shows the team at team preview, which is further divided into team 1 and team 2.
#Mega regex shows which pokemon is the mega Pokemon, if applicable


jsonFolder = os.path.dirname(__file__)
#Accesses the directory above this module for the JSON data.

megaStoneJSON = open(os.path.join(jsonFolder, 'json/megaEvolves.json'), "r")
#JSON file which contains the list of all the Mega Pokemon and their corresponding Mega Stones.

megaStoneToMegaPokemon = json.loads(megaStoneJSON.read())
#JSON file which contains the Mega Pokemon associated with each Mega Stone.

megaList = {megaStoneToMegaPokemon[x][0]:megaStoneToMegaPokemon[x][1] for x in megaStoneToMegaPokemon}
#Takes the JSON list and converts it into a dictionary for easier use.

banJSON = open(os.path.join(jsonFolder, 'json/banList.json'), "r")
banList = json.loads(banJSON.read())
#JSON list which contains all the banned pokemon in each Doubles Tier.

	
gen7doublesoupriority = ['Beedrill', 'Sceptile','Manectric', 'Mawile', 'Charizard', 'Pidgeot', 'Ampharos', 'Banette', 'Medicham','Heracross', 'Altaria', 'Sharpedo', 'Steelix',
 'Houndoom', 'Lopunny', 'Aggron','Glalie', 'Alakazam', 'Sableye', 'Pinsir', 'Gengar', 'Gardevoir', 'Camerupt', 'Abomasnow',  'Swampert', 'Metagross', 'Salamence', 'Absol', 'Scizor', 'Aerodactyl', 'Slowbro','Gyarados', 'Audino', 'Blaziken', 'Venusaur', 'Blastoise', 'Gallade', 'Tyranitar', 'Diancie', 'Latias', 'Latios', 'Garchomp']
gen7doublesuupriority = ['Beedrill', 'Sceptile','Manectric', 'Mawile', 'Charizard', 'Venusaur', 'Pidgeot', 'Ampharos', 'Banette', 'Medicham','Heracross', 'Altaria', 'Sharpedo', 'Steelix', 'Houndoom', 'Lopunny', 'Aggron','Glalie', 'Alakazam', 'Sableye', 'Pinsir', 'Gardevoir', 'Abomasnow', 
'Absol', 'Scizor', 'Aerodactyl', 'Slowbro','Gyarados', 'Audino', 'Blaziken', 'Blastoise', 'Gallade', 'Latias', 'Latios', 'Garchomp']
#Based on anecdotal evidence if multiple potential megas are on the field, which ones are likely to be mega and which ones arent. Order may not be accurate.


"""If no pokemon Mega Evolved during a battle and it isn't obvious which pokemon has the Mega Stone, we reference the above list for which pokemon is the likely mega (could be inaccurate)
Takes a list of potential Megas in a team if the replay doesn't reveal the mega in any other way, and returns the most likely mega pokemon for the given tier/format.
Parameters: Array megaL, String format
Returns: String for a name of Pokemon that is likely to be the mega pokemon in the team, or Nothing if some weird error occurs.
"""
def checkPriorities(megaL, format):
	if format == 'gen7doublesou':
		#Distinguishes between Doubles OU and Doubles UU because each have different viable megas.
		for mons in gen7doublesoupriority:
			#Iterates through all the potential candidates in order, and checks if there is a match in megaL. Immediately returns the Mega if a match is found.
			
			if mons in megaL:
				#We hardcode Zard-Y for Doubles OU. What are the odds this is going to be wrong? Since Mewtwo is DUbers, we don't worry about him and return the corresponding mega for other candidates.
				if mons == 'Charizard':
					return 'Charizard-Mega-Y'
				else:
					return megaList[mons]
	elif format == 'gen7doublesuu':
		#Same thing for Doubles UU, except Zard-Y is banned so we hard-code Zard-X in the program
		for mons in gen7doublesuupriority:
			if mons in megaL:
				if mons == 'Charizard':
					return 'Charizard-Mega-X'
				else:
					return megaList[mons]
	else:
		print('?')
		#If you ever see a '?' in the console, please come back to me.... This is an issue.
		return


"""
If the replay does not reveal a mega pokemon for one side, we use the smart Mega analyzer to narrow down the potential Mega Pokemon on a given team.
Assumes one Mega pokemon DOES exist per pokemon team.
Checks for knocked off items, activated items, Z crystals, etc.
Parameters: Array team, String replaytext, String format, int player
Returns: Array team with mega pokemon instead of nonmega Pokemon
"""
def smartMegaAnalyzer(team, replaytext, format, player):
	candidateMega = []
	#Initialize all potential Mega Pokemon here
	
	for mon in team:
		#Iterates through all Pokemon on a team.
		
		#If a Mega Pokemon is already in the team, then return the team since we already know the Mega; keeping in mind X and Y Megas exist.
		if mon[-5:] == '-Mega' or mon[-7:] == '-Mega-X' or mon[-7:] == '-Mega-Y':
			return team
		
		#Otherwise, if a Pokemon has a potential to be a Mega and the Mega isn't banned in that format (which we check against the megaList), add it into the candidate.
		elif mon in megaList and (not (mon in banList[format+"BanList"])):
			candidateMega.append(mon)
			
	#If no candidate Megas exist, then no point in analyzing the team any further; this team is megaLess.		
	if len(candidateMega) == 0:
		return team
		
	#Otherwise, we scrutinize the replay to see if we can rule out any or all of the potential Megas.
	else:
		filteredCandidates = []
		#Create an array of Mega pokemon candidates that make it through each test.
		
		for mon in candidateMega:
			#Iterate through each potential Mega.
			
			nickn = re.search('(?<=\|switch\|p'+str(player)+'.: )[^\|]+\|'+mon, replaytext)
			#Puts the Pokemon Name in question compatible with the replay and regex. This assumes the pokemon was brought into the game.
			
			if nickn:
				nickname = nickn.group(0).split('|')
				#Don't touch this line.
				
				zcrystal = re.search('(?<=\-zpower\|p'+str(player)+'.: )'+nickname[0], replaytext)
				#Checks to see if the pokemon has a Z-Crystal. If not, we continue the search. If we find it, the pokemon doesn't get appended to the filteredCandidates array.
				if not zcrystal:
				
				
					item = re.search('(?<=\-enditem\|p'+str(player)+'.: )'+nickname[0], replaytext)
					#We see if the pokemon had an item knocked off or bitten or flung. If not, we continue the search. If we find it, pokemon doesn't get added to the filteredCandidates array.
					if not item:
					
						activeItem = re.search(nickname[0]+'\|[^\|]+\|\[from\] item:', replaytext)
						#We see if a pokemon activated an item, like seeds, berries, weakness policies, etc. If not, then we can't rule out the pokemon and the pokemon is still a candidate.
						if not activeItem:
							filteredCandidates.append(mon)
			
			#If the pokemon was never brought in, we can't assume anything so we keep it as a candidate.
			else:
				filteredCandidates.append(mon)
			
		#If there are no pokemon after the initial check, then the team has no Mega, and we return the team as is.	
		if len(filteredCandidates) == 0:
			return team
			
		#If after the check, we have only 1 potential mega, then we assume the pokemon is a mega, and return the Mega form of the pokemon.	
		elif len(filteredCandidates) == 1:
			t = []
			
			#Checks whether Zard-Y is banned in a given format, because X/Y megas are dumb.
			if filteredCandidates[0] == 'Charizard':
				if not (format in banList["Charizard-Mega-YBan"]):
					t = ['Charizard-Mega-Y' if mon == filteredCandidates[0] else mon for mon in team]
					#Iterates through the team and swaps out Zard for Zard-Y; otherwise the team is unchanged and return it.
					return t
				else:
					t = ['Charizard-Mega-X' if mon == filteredCandidates[0] else mon for mon in team]
					#Iterates through the team and swaps out Zard for Zard-X; otherwise the team is unchanged and return it.
					return t
					
			else:
				t = [megaList[mon] if mon == filteredCandidates[0] else mon for mon in team]
				#Iterates through the team and swaps out the potential Mega with the appropriate Mega; otherwise the team is unchanged and return it.
				return t
		
		#If there are still 2+ pokemon who can be a mega, we consider the meta and the context in which the pokemon exists (for instance, would I ever use a nonmega Beedrill in DOU? Probably not.)
		else:
			mega = checkPriorities(filteredCandidates, format)
			
			#Iterates through the team and swaps out the potential Mega with the appropriate Mega; otherwise the team is unchanged and return it.
			t = [mega if mon == mega[:len(mon)] else mon for mon in team]
			return t
	
	
	
	
	
"""
Checks for a Mega Evolution in the Replay, and returns an updated team with the Mega Evolution instead of the base form.
Parameters: String replayText, Array team1, Array team2, String tier
Returns: Array team
"""
def searchForMegas(replayText, team1, team2, tier):
	t1 = team1
	t2 = team2
	#Because we will be modifying the teams, better put it as a new variable.
	
	megaPokemons = megaRegex.findall(replayText)
	#Searches the replay for any signs of Mega Evolutions
	
	#If there are less than 2 instances of Mega Evolution, we have to perform a deep dive into each team to see what the Mega Pokemon is.
	if len(megaPokemons) <= 1:
		"""Investigate if it is possible to get the Mega for the team which DOES contain the mega evolution instead of putting both teams through the smartMegaAnalyzer	(improves accuracy)"""
		t1, t2= smartMegaAnalyzer(team1, replayText, tier, 1), smartMegaAnalyzer(team2, replayText, tier, 2)
		#Puts both teams through the smartMegaAnalyzer to determine the Mega Pokemon.
		return t1, t2
		
	#If both teams have a Mega Pokemon, the search becomes a lot simpler.	
	else:
		for mon in megaPokemons:
		#megaPokemons should be an array; therefore we just iterate through to see which player has which mega Pokemon.
			megaItem = re.search('[a-zA-Z ]+$',mon).group(0)
			
			plr = int(re.search('\d', mon).group(0))
			#Searches for the player corresponding to each mega Pokemon
			
			if plr == 1:
				t1 = [megaStoneToMegaPokemon[megaItem][1] if x == megaStoneToMegaPokemon[megaItem][0] else x for x in team1]
				#Replace the base Pokemon with the identified mega Pokemon for team 1.
				
			elif plr == 2:
				t2 = [megaStoneToMegaPokemon[megaItem][1] if x == megaStoneToMegaPokemon[megaItem][0] else x for x in team2]
				#Replace the base Pokemon with the identified mega Pokemon for team 2.

			else:
				print('cant identify plr for megastone')
				#This shouldn't happen, but if it does, we know.
				
		if t1 == [] or t2 == []:
			print('empty at searchForMegas else statement')
			#For debug purposes.
			
		return t1, t2
		


"""
Takes the raw replay string and extracts out the teams and players who used the team, and the winner of the battle as a dictionary.
Parameters: String replaytext
Returns: Dictionary replayInfo with keys team1, team2, winner, p1, p2, where p1 and p2 are the names of the player.
"""
def replayAlgorithm(replaytext):
	replayInfo = {}
	#Dictionary of the info contained in the replayInfo
	
	#If the replay wasn't saved properly, we return None. We don't want to raise an exception.
	replayDoesntExist = re.search("The battle you're looking for has expired. Battles expire after 15 minutes of inactivity unless they're saved.", replaytext)
	if replayDoesntExist:
		return
	
	#Extracts the team Preview from the replay.
	teamStr = teamRegex.search(replaytext).group(0)
	
	#Extracts the winner of the battle from the replay.
	winnerText = winnerRegex.search(replaytext).group(0)

	#Extracts Players 1 and 2, respectively, from the replay.
	p1 = re.search('(?<=\|player\|p1\|).+?(?=\|)', replaytext).group(0)
	p2 = re.search('(?<=\|player\|p2\|).+?(?=\|)', replaytext).group(0)
	
	#Determines the winner from the replay.
	if p1==winnerText:
		replayInfo['winner'] = 1
	elif p2 == winnerText:
		replayInfo['winner'] = 2
		
	#In case stuff like KennyJ vs Mint16 happen.
	else:
		print('cannot find winner!')
		
	#Stores the Player names into the dictionary.
	replayInfo['p1'] = p1
	replayInfo['p2'] = p2
	
	#Obtains team 1 and team 2.
	t1 = t1Regex.findall(teamStr)
	t2 = t2Regex.findall(teamStr)
	
	#Obtains the tier the game was played in.
	tier = re.search('(?<=value\=\").+?(?=\-[0-9])',replaytext).group(0)
	if tier[:10] == "smogtours-":
		tier = tier[10:]
		
	#Takes the team and parses the mega evolutions (this is what makes my version better!)
	replayInfo['team1'], replayInfo['team2'] =searchForMegas(replaytext, t1, t2, tier)
	return replayInfo


"""
Parses the replayLink and turns it into raw Text that replayAlgorithm can intake.
Parameters: String replayLink 
Return: Dictionary replayInfo
"""
def main(replayLink):	
	r = requests.get(replayLink)
	return replayAlgorithm(r.text)
	
	
#To be able to be called from the Terminal
if __name__ == "__main__":
	main(sys.argv[1])
	