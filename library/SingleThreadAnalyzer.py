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
#Imports other custom modules I made.


allReplays = []
#Empty array which contains the usage stats for each Pokemon

failedReplays = []
#Empty array which contains failed replays.

filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__))))
#Leads to directory two above.
	
f = open(os.path.join(filelocation, 'CONFIG.txt'))
#Leads to CONFIG.txt

directory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)
#Gets the directory where all usage stat files will be stored.

"""
Scans a single thread for all the replays for a given tier, and outputs the usage stats in a file.
Parameters: String thread (URL), String tourName, String fileName, String tiernameInReplayUrl
Returns: Nothing
"""
def main(thread=None, tourName=None, fileName=None, tiernameInReplayUrl=None):
	finalThread = thread
	finalTourName = tourName
	finalFileName = fileName
	finalTierName = tiernameInReplayUrl
	#Redefines parameters due to scopes and modifying variables
	
	if thread == None:
		#If the input contains none of this information, we prompt the user for this information
		finalThread = input("Paste Thread URL here")
		finalTourName = input("Enter Name of Tournament here")
		finalFileName = input("Enter Title of File here")
		finalTierName = input("Enter Tier Here (Generation and Tier)")
	
	
	counter = 0
	#Counter to track how many replays have been analyzed.
	
	print(tiernameInReplayUrl)
	#sanity check

	replays = SmogonRoundReplayScanner.getReplays(finalThread, finalTierName)
	#Gets the list of all the replays in the thread provided by the url and the tier name
	
	for replay in replays:
		#Iterates through the replays in the array.
		
		counter = counter+1
		sys.stdout.write("\rAnalyzed Replay %d of %d            " % (counter, len(replays)))
		sys.stdout.flush()
		#Outputs on the console the percentage complete
		
		r3 = requests.get('https:/'+replay)
		replayText = r3.text
		#Dummy variable that gets the replay in text format
		returnedMessage = ReplayAnalyzer.replayAlgorithm(replayText)
		if returnedMessage:
			allReplays.append(ReplayAnalyzer.replayAlgorithm(replayText))
		else:
			failedReplays.append(replay)
		#Gets the replay link, parses it to the replayAnalyzer and obtains a simplified version of the replay (with teams, winners).
		
	if not os.path.exists(directory+finalFileName+'\\'):
		os.mkdir(directory+finalFileName+'\\')
		#If the directory where the replays will be stored does not exist; create one
	
	round_file = open(directory+finalFileName+'\\tournamentTeam.txt', "w+")
	json.dump(allReplays, round_file)
	#Outputs and creates the file that contains all the replays from  the team
	round_file.close()
	if len(failedReplays) > 0:
        print()
		print(f'{len(failedReplays)} replays failed to load! Failed links:' )
		for failedReplay in failedReplays:
			print(failedReplay)
	UsageAnalyzer.outputStats(finalTourName, finalFileName)
	#Creates the usage stat document from the replays of the thread
	
	
#To be able to be called from the terminal.
if __name__ == "__main__":
	if len(sys.argv) == 1:
		main()
	elif len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print("Invalid parameter length")
