#TODO: Consider non-scan issues due to failed round identification

import requests
import re
import unicodedata
import SmogonTournamentPageScanner
import SmogonRoundReplayScanner
import ReplayAnalyzer
import UsageAnalyzer
import json
import os
import sys


r = requests.get("https://www.smogon.com/forums/forums/smogon-metagames-circuits.474/")
counter = 1

domain = "https://www.smogon.com"
usageStats = {}
roundAndReplays = {}
#Dictionaries to store replays and rounds

filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__))))
f = open(os.path.join(filelocation, 'CONFIG.txt'))
directory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)

"""Generates the Usage stat for multi-thread Tournaments that start with given name @tourType
Parameters: String tourType, String tourFileTitle
Returns: Nothing
"""
def main(tourType=None, tourFileTitle=None):
	if tourType == None:
		#If no input, we prompt the user to enter the input as well as the file name
		tourType = input("Enter name of tournament that you would like usage stats on.")
		tourFileTitle = input("Enter Filename for the usage stats")
	
	#Because of how Thread titles are converted into the URL, we replace all spaces with "-"
	tourType = tourType.lower().replace(" ", "-")
	
	#Get a list of Threads that start with @tourType, and call it @lot
	lot = SmogonTournamentPageScanner.getAllThreads(tourType)

	#Iterate through the threads in lot.
	for thread in lot:
	
		lorp = SmogonRoundReplayScanner.getReplays(domain+thread)
		#Gets the replays from the thread
		
		regexGroup = re.search('(?<=-round)s?\-[\-\d]+', thread)
		#Gets the round # from the thread title.
		
		#If there are replays in the thread
		if len(lorp) > 0:
		
			#If we can identify the round, we associate the round with a set of replays.
			"""This may cause entire threads to be ignored.... Address later"""
			if regexGroup:
				roundAndReplays[regexGroup.group(0)] = lorp
			else:
				print("regex failed to identify round")
			
	#Iterate through every round in the roundAndReplays Dictionary and analyze the replay.
	for round in roundAndReplays:
		
		roundReplayList=[]
		#Local Array
		
		counter = 0
		#Tracks the number of replays analyzed
		
		for replay in roundAndReplays[round]:
			#Iterate through all the replays in each thread.
			counter = counter+1
			
			sys.stdout.write("\rAnalyzing round%s. Analyzed Replay %d of %d            " % (round, counter, len(roundAndReplays[round])))
			sys.stdout.flush()
			#Output the current status of the analysis.
			
			r3 = requests.get("https:/"+replay)
			replayText = r3.text
			#Converts the replay link into a raw text.
			
			checkLink = ReplayAnalyzer.replayAlgorithm(replayText) 
			#blame Croven for this line, makes sure there aren't any invalid replays, but also strips down the replay into a simplified format.
			if checkLink:	#Fuck Croven
				roundReplayList.append(checkLink)
				#Add all simplified replays into a list.
				
		usageStats[round]=roundReplayList
		#Associates the list of simplified replays with a round number.
		print()

	if not os.path.exists(directory+tourFileTitle+'\\'):
		os.mkdir(directory+tourFileTitle+'\\')
		#Makes sure the directory that we are trying to output into exists 
		
	print("Replay analysis complete.")
	
	#Iterate through every round and output a file holding all the replays.
	for round in usageStats:
		sys.stdout.write("\rWriting to file: "+directory+tourFileTitle+"\\round%s" % round)
		sys.stdout.flush()
		#Prints out What file we are currently outputting.
		
		round_file = open(directory+tourFileTitle+'\\round'+round+'.txt', "w+")
		json.dump(usageStats[round], round_file)
		round_file.close()
		#Actually outputting the file
		
	print("Completed Writing Teams")
	UsageAnalyzer.outputStats(tourType, tourFileTitle)
	UsageAnalyzer.outputStats(tourType, tourFileTitle, True, 4)
	UsageAnalyzer.outputStats(tourType, tourFileTitle, True, 6)
	UsageAnalyzer.outputStats(tourType, tourFileTitle, True, 8)
	#Creates usage stats for Rounds 4+, 6+, and 8+ as well as the entire tournament.

if __name__=="__main__":
	if len(sys.argv) == 1:
		main()
	elif len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])