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


usageStats = []

filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__))))
	
f = open(os.path.join(filelocation, 'CONFIG.txt'))

directory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)


def main(thread=None, tourName=None, fileName=None, tiernameInReplayUrl=None):
	finalThread = thread
	finalTourName = tourName
	finalFileName = fileName
	finalTierName = tiernameInReplayUrl
	if thread == None:
		finalThread = input("Paste Thread URL here")
		finalTourName = input("Enter Name of Tournament here")
		finalFileName = input("Enter Title of File here")
		finalTierName = input("Enter Tier Here (Generation and Tier)")
	
	counter = 0
	print(tiernameInReplayUrl)
	replays = SmogonRoundReplayScanner.getReplays(finalThread, finalTierName)
	for replay in replays:
		counter = counter+1
		sys.stdout.write("\rAnalyzed Replay %d of %d            " % (counter, len(replays)))
		sys.stdout.flush()
		r3 = requests.get('https:/'+replay)
		replayText = r3.text
		usageStats.append(ReplayAnalyzer.replayAlgorithm(replayText))
	if not os.path.exists(directory+finalFileName+'\\'):
		os.mkdir(directory+finalFileName+'\\')
	
	round_file = open(directory+finalFileName+'\\tournamentTeam.txt', "w+")
	json.dump(usageStats, round_file)
	round_file.close()
	UsageAnalyzer.outputStats(finalTourName, finalFileName)
	
if __name__ == "__main__":
	if len(sys.argv) == 1:
		main()
	elif len(sys.argv) == 5:
		main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print("Invalid parameter length")