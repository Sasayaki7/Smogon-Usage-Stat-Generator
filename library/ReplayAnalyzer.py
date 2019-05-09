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

jsonFolder = os.path.dirname(__file__)
megaStoneJSON = open(os.path.join(jsonFolder, 'json/megaEvolves.json'), "r")
megaStoneToMegaPokemon = json.loads(megaStoneJSON.read())


megaList = {megaStoneToMegaPokemon[x][0]:megaStoneToMegaPokemon[x][1] for x in megaStoneToMegaPokemon}
banJSON = open(os.path.join(jsonFolder, 'json/banList.json'), "r")
banList = json.loads(banJSON.read())


	
gen7doublesoupriority = ['Beedrill', 'Sceptile','Manectric', 'Mawile', 'Charizard', 'Pidgeot', 'Ampharos', 'Banette', 'Medicham','Heracross', 'Altaria', 'Sharpedo', 'Steelix',
 'Houndoom', 'Lopunny', 'Aggron','Glalie', 'Alakazam', 'Sableye', 'Pinsir', 'Gengar', 'Gardevoir', 'Camerupt', 'Abomasnow',  'Swampert', 'Metagross', 'Salamence', 'Absol', 'Scizor', 'Aerodactyl', 'Slowbro','Gyarados', 'Audino', 'Blaziken', 'Venusaur', 'Blastoise', 'Gallade', 'Tyranitar', 'Diancie', 'Latias', 'Latios', 'Garchomp']
gen7doublesuupriority = ['Beedrill', 'Sceptile','Manectric', 'Mawile', 'Charizard', 'Venusaur', 'Pidgeot', 'Ampharos', 'Banette', 'Medicham','Heracross', 'Altaria', 'Sharpedo', 'Steelix', 'Houndoom', 'Lopunny', 'Aggron','Glalie', 'Alakazam', 'Sableye', 'Pinsir', 'Gardevoir', 'Abomasnow', 
'Absol', 'Scizor', 'Aerodactyl', 'Slowbro','Gyarados', 'Audino', 'Blaziken', 'Blastoise', 'Gallade', 'Latias', 'Latios', 'Garchomp']
def checkPriorities(megaL, format):
	if format == 'gen7doublesou':
		for mons in gen7doublesoupriority:
			if mons in megaL:
				if mons == 'Charizard':
					return 'Charizard-Mega-Y'
				else:
					return megaList[mons]
	elif format == 'gen7doublesuu':
		for mons in gen7doublesuupriority:
			if mons in megaL:
				if mons == 'Charizard':
					return 'Charizard-Mega-X'
				else:
					return megaList[mons]
	else:
		print('?')
		return

def smartMegaAnalyzer(team, text, format, player):
	candidateMega = []
	for mon in team:
		if mon[-5:] == '-Mega' or mon[-7:] == '-Mega-X' or mon[-7:] == '-Mega-Y':
			return team
		elif mon in megaList and (not (mon in banList[format+"BanList"])):
			candidateMega.append(mon)
	if len(candidateMega) == 0:
		return team
	else:
		filteredCandidates = []
		for mon in candidateMega:
			nickn = re.search('(?<=\|switch\|p'+str(player)+'.: )[^\|]+\|'+mon, text)
			if nickn:
				nickname = nickn.group(0).split('|')
				zcrystal = re.search('(?<=\-zpower\|p'+str(player)+'.: )'+nickname[0], text)
				if not zcrystal:
					item = re.search('(?<=\-enditem\|p'+str(player)+'.: )'+nickname[0], text)
					if not item:
						activeItem = re.search(nickname[0]+'\|[^\|]+\|\[from\] item:', text)
						if not activeItem:
							filteredCandidates.append(mon)
			else:
				filteredCandidates.append(mon)
		if len(filteredCandidates) == 0:
			return team
		elif len(filteredCandidates) == 1:
			t = []
			if filteredCandidates[0] == 'Charizard':
				if not (format in banList["Charizard-Mega-YBan"]):
					t = ['Charizard-Mega-Y' if mon == filteredCandidates[0] else mon for mon in team]
					return t
				else:
					t = ['Charizard-Mega-X' if mon == filteredCandidates[0] else mon for mon in team]
					return t
			else:
				t = [megaList[mon] if mon == filteredCandidates[0] else mon for mon in team]
				return t
		else:
			mega = checkPriorities(filteredCandidates, format)
			t = [mega if mon == mega[:len(mon)] else mon for mon in team]
			return t
	
def searchForMegas(replayText, team1, team2, tier):
	t1 = team1
	t2 = team2
	megaPokemons = megaRegex.findall(replayText)
	if len(megaPokemons) <= 1:
		t1, t2= smartMegaAnalyzer(team1, replayText, tier, 1), smartMegaAnalyzer(team2, replayText, tier, 2)
		return t1, t2
	else:
		for mon in megaPokemons:
			megaItem = re.search('[a-zA-Z ]+$',mon).group(0)
			plr = int(re.search('\d', mon).group(0))
			if plr == 1:
				t1 = [megaStoneToMegaPokemon[megaItem][1] if x == megaStoneToMegaPokemon[megaItem][0] else x for x in team1]
			elif plr == 2:
				t2 = [megaStoneToMegaPokemon[megaItem][1] if x == megaStoneToMegaPokemon[megaItem][0] else x for x in team2]
			else:
				print('cant identify plr for megastone')
		if t1 == [] or t2 == []:
			print('empty at searchForMegas else statement')
		return t1, t2

def replayAlgorithm(replaytext):
	replayInfo = {}
	replayDoesntExist = re.search("The battle you're looking for has expired. Battles expire after 15 minutes of inactivity unless they're saved.", replaytext)
	if replayDoesntExist:
		return
	teamStr = teamRegex.search(replaytext).group(0)
	winnerText = winnerRegex.search(replaytext).group(0)
	p1 = re.search('(?<=\|player\|p1\|).+?(?=\|)', replaytext).group(0)
	p2 = re.search('(?<=\|player\|p2\|).+?(?=\|)', replaytext).group(0)
	if p1==winnerText:
		replayInfo['winner'] = 1
	elif p2 == winnerText:
		replayInfo['winner'] = 2
	else:
		print('cannot find winner!')
	replayInfo['p1'] = p1
	replayInfo['p2'] = p2
	t1 = t1Regex.findall(teamStr)
	t2 = t2Regex.findall(teamStr)
	tier = re.search('(?<=value\=\").+?(?=\-[0-9])',replaytext).group(0)
	if tier[:10] == "smogtours-":
		tier = tier[10:]
	replayInfo['team1'], replayInfo['team2'] =searchForMegas(replaytext, t1, t2, tier)
	return replayInfo

	
def main(replayLink):
	r = requests.get(replayLink)
	replayAlgorithm(r.text)
	
	
if __name__ == "__main__":
	main(sys.argv[1])