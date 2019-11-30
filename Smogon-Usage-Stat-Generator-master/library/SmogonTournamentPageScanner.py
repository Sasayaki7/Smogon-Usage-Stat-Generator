import requests
import re

domain = "https://www.smogon.com"

"""
Gets all the threads with a given thread title
Parameters: String threadType
Returns: Array listOfThreads with all the Threads in an array.
"""
def getAllThreads(threadType):
	print("Getting all relevant threads...")
	
	tournamentpagePat = re.compile('/forums/threads/'+threadType+'[^/]+(?!latest)(?!preview)')
	#Gets all the threads from the Tournaments page with the common title @threadType
	
	started = False
	#Boolean indicators to see if a thread has been found yet.

	finished = False
	#Boolean indicators to see if there are no more threads left.
	
	listOfThreads = []
	
	
	counter = 1
	#aka Page Number
	
	#If a thread has not yet been found, or if there are still more threads on the current page, search the next page for more threads.
	while not (started and finished):
		r = requests.get(domain+"/forums/forums/smogon-metagames-circuits.474/page-"+str(counter))
		#Gets the next page of tournaments
		
		newList = (tournamentpagePat.findall(r.text))
		#Searches the entire page for threads with the common title.
		
		if len(newList) > 0:
			started = True
			#If first thread is found, we tick the started indicator
			
		elif started and len(newList) == 0:
			#If we have already found a thread and there are no new threads on this page.
			finished = True
			
		listOfThreads.extend(newList)
		#Keep adding in new threads to the @listOfThreads
		
		counter = counter+1	
		#Ticks the next page
		
	listOfThreads = list(set(listOfThreads))
	#Remove duplicate threads just in case.
	
	return listOfThreads