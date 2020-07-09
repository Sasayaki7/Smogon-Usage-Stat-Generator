import requests
import re
import unicodedata
import sys

domain = "https://www.smogon.com"

roundPagePat = re.compile('/replay.pokemonshowdown.com/[0-9a-zA-Z\-]+')
pageRegex = re.compile('(?<=js-pageJumpPage" value="\d"  min="\d" max=")\d+')
#Creates regex to be used later. Can be ignored


"""
Gets all the replays for a given tier on a page, if applicable.
Parameters: int page, String tier
Returns: Array tempList, which contains a list of replays for a given tier on the page
"""
def findReplays(page, tier=None):
	if tier:
		#If tier is specified, parse the tier into a replay-regex compatible format
		tier = getTierUrl(tier)
	
	#A temporary list which contains all the replays in a given page
	tempList = roundPagePat.findall(page)
	
	if tier:
		#If tier is specified, we need to remove the replays that are not for the given tier.
		
		#Makes a second list to iterate through.
		listclone = [i for i in tempList]
		
		for i in listclone:
			#iterates through the list for replays.

			#If the tier specified and the replay is not for that tier, remove the replay from the list
			if not re.search(tier, i):			
				tempList.remove(i)
				
	return tempList



"""Gets all the replays for all the threads given.
Parameters: Array repList
Returns: Array listOfReplays which contains an array of all the replays
"""
def getAllReplays(repList):
	listOfReplays = []
	#Initalizes the listOfReplays
	
	#Counter which tracks the thread that is currently being checked
	counter = 0
	
	#Iterates through all the threads given in repList
	for link in repList:
		counter = counter+1
		sys.stdout.write("\rObtaining Replays... Searching thread %i of "+str(len(repList)) % counter)
		sys.stdout.flush()
		#Prints out the current thread being analyzed.

		listOfReplays.extend(getReplays(link))
		#Iterates through each thread for replays.
				
	listOfReplays = list(set(listOfReplays))
	#This is to remove duplicate replays so that each replay is only accounted for once.
	
	print("Obtained "+str(len(listOfReplays))+" replays")
	#Sanity Check
	
	return listOfReplays
	
	
	
"""Takes an arbitrary tier specification and converts it into the tier format specified in the replay link
i.e. "SM DOU" -> "gen7doublesou"
Parameters: String tier
Returns: String finalTier
"""
def getTierUrl(tier):
	finalTier = "gen7"
	#Set default to gen7 (or the latest gen)
	t = tier.lower()
	#Lower case to avoid complications
	
	#First check the generation, which we typically put at the beginning.
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
   	elif t[:2] == 'ss' or t[:4] == "gen8" or t[:5] == "gen 8":
   	   	finalTier = "gen8"
	else:
		print("Generation not found; Assuming Current Gen (Default Gen 8)")
		finalTier = "gen8"
	
	#Append the tier to the generation			
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
	
	
"""
Gets all the replays for a single thread.
Parameter: String thread, String tier
Returns: Array listOfReplays with all the replays in a simplified format.
"""


def getReplays(thread, tier=None):
	listOfReplays = []
	print(thread)
	
	r2 = requests.get(thread+"/page-1")		
	replayList = findReplays(r2.text)
	#Starts on Page 1 of the thread, and gets the replays from page 1 of the thread.
		
		if len(replayList) > 0:
			listOfReplays.extend(replayList)
			#If the list returned has replays, we add on to the replayList.
			
		pagematchObj = pageRegex.search(r2.text)
		if pagematchObj:
			#If there are additional pages, we check the next pages for additional replays.
			
			pageNum = int(pagematchObj.group(0))
			for i in range(pageNum-1):
				#Keep iterating until the final page.
				r2 = requests.get(thread+"/page-"+str(i+2))
				
				#Add on all replays found into listOfReplays
				listOfReplays.extend(findReplays(r2.text, tier))
				
	#Eliminates duplicate replays.
	listOfReplays = list(set(listOfReplays))
	return listOfReplays
	
