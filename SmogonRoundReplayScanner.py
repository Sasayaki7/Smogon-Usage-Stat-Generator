import requests
import re
import unicodedata
import sys

domain = "https://www.smogon.com"

roundPagePat = re.compile('/replay.pokemonshowdown.com/[0-9a-zA-Z\-]+')
pageRegex = re.compile('(?<=js-pageJumpPage" value="\d"  min="\d" max=")\d+')


def findReplays(page, tier=None):
	if tier:
		tier = getTierUrl(tier)
	tempList = roundPagePat.findall(page)
	listclone = [i for i in tempList]
	if tier:
		for i in listclone:
			print(i, tier)
			if not re.search(tier, i):			
				print('removed')
				tempList.remove(i)
	return tempList
	
def getAllReplays(repList):
	listOfReplays = []
	counter = 0
	for link in repList:
		counter = counter+1
		sys.stdout.write("\rObtaining Replays... Searching thread %i of "+str(len(repList)) % counter)
		sys.stdout.flush()
		r2 = requests.get(link+"/page-1")
		replayList = findReplays(r2.text)
		if len(replayList) > 0:
			listOfReplays.extend(replayList)
		pagematchObj = pageRegex.search(r2.text)
		if pagematchObj:
			pageNum = int(pagematchObj.group(0))
			for i in range(pageNum-1):
				r2 = requests.get(link+"/page-"+str(i+2))
				listOfReplays.extend(findReplays(r2.text))
	listOfReplays = list(set(listOfReplays))
	print("Obtained "+str(len(listOfReplays))+" replays")
	return listOfReplays
	
def getTierUrl(tier):
	finalTier = "gen7"
	t = tier.lower()
	if t[:2] == 'xy' or t[:4] == 'oras' or t[:4] == "gen6" or t[:5] == "gen 6":
		finalTier = "gen6"
	elif t[:4] == "usum" or t[:3] == "usm" or t[:2] == "sm" or t[:4] == "gen7" or t[:5] == "gen 7":
		finalTier = "gen7"
	elif t[:2] == "bw" or t[:4] == "b2w2" or t[:4] == "gen5" or t[:5] == "gen 5":
		finalTier = "gen5"
	elif t[:3] == "dpp" or t[:2] == "dp" or t[:4] == "gen4" or t[:5] == "gen 4" or t[:4] =="hgss":
		finalTier = "gen4"
	elif t[:3] == "adv" or t[:3] == "rse" or t[:4] == "frlg" or t[:4] == "gen3" or t[:5] == "gen 3":
		finalTier = "gen3"
	elif t[:3] == "gsc" or t[:4] == "gen2" or t[:5] == "gen 2":
		finalTier = "gen2"
	elif t[:3] == "rby" or t[:4] == "gen1" or t[:5] == "gen 1":
		finalTier = "gen1"
	else:
		print("Generation not found; Assuming Current Gen (Default Gen 7)")
		finalTier = "gen7"
	if t[-9:] == "doublesou":
		finalTier = finalTier+"doublesou"
	elif t[-9:] == "doublesuu":
		finalTier = finalTier+"doublesuu"
	elif t[-12:] == "doublesubers":
		finalTier = finalTier+"doublesubers"
	elif t[-9:] == "doubleslc":
		finalTier = finalTier+"doubleslc"
	elif t[-2:]=="ru":
		finalTier = finalTier+"ru"
	elif t[-2:]=="nu":
		finalTier = finalTier+"nu"
	elif t[-2:]=="uu":
		finalTier = finalTier+"uu"
	elif t[-2:]=="ou":
		finalTier = finalTier+"ou"
	elif t[-2:]=="pu":
		finalTier = finalTier+"pu"
	elif t[-2:] == "lc":
		finalTier = finalTier+"lc"
	return finalTier
		
def getReplays(rep, tier=None):
	listOfReplays = []
	print(rep)
	r2 = requests.get(rep+"/page-1")
	replayList = findReplays(r2.text, tier)
	if len(replayList) > 0:
		listOfReplays.extend(replayList)
	pagematchObj = pageRegex.search(r2.text)
	if pagematchObj:
		pageNum = int(pagematchObj.group(0))
		for i in range(pageNum-1):
			r2 = requests.get(rep+"/page-"+str(i+2))
			listOfReplays.extend(findReplays(r2.text, tier))
	listOfReplays = list(set(listOfReplays))
	print("Obtained "+str(len(listOfReplays))+" replays")
	return listOfReplays
	
