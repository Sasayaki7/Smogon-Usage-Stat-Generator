import requests
import re

domain = "https://www.smogon.com"

	
def getAllThreads(threadType):
	print("Getting all relevant threads...")
	tournamentpagePat = re.compile('/forums/threads/'+threadType+'[^/]+(?!latest)(?!preview)')
	started = False
	finished = False
	listOfThreads = []
	counter = 1
	while not (started and finished):
		r = requests.get(domain+"/forums/forums/smogon-metagames-circuits.474/page-"+str(counter))		
		newList = (tournamentpagePat.findall(r.text))
		if len(newList) > 0:
			started = True
		elif started and len(newList) == 0:
			finished = True
		listOfThreads.extend(newList)
		counter = counter+1	
	listOfThreads = list(set(listOfThreads))
	return listOfThreads