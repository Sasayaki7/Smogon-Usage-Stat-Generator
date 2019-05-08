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

filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(filelocation, 'CONFIG.txt'))
directory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)

	
def main(tourType=None, tourFileTitle=None):
	if tourType == None:
		tourType = input("Enter name of tournament that you would like usage stats on.")
		tourFileTitle = input("Enter Filename for the usage stats")
	tourType = tourType.lower().replace(" ", "-")
	lot = SmogonTournamentPageScanner.getAllThreads(tourType)

	for round in lot:
		lorp = SmogonRoundReplayScanner.getReplays(domain+round)
		regexGroup = re.search('(?<=-round)s?\-[\-\d]+', round)
		if len(lorp) > 0:
			if regexGroup:
				roundAndReplays[regexGroup.group(0)] = lorp
			else:
				print("regex failed to identify round")
			
	for round in roundAndReplays:
		roundReplayList=[]
		counter = 0
		for replay in roundAndReplays[round]:
			counter = counter+1
			sys.stdout.write("\rAnalyzing round%s. Analyzed Replay %d of %d            " % (round, counter, len(roundAndReplays[round])))
			sys.stdout.flush()
			r3 = requests.get("https:/"+replay)
			replayText = r3.text
			checkLink = ReplayAnalyzer.replayAlgorithm(replayText) #blame Croven for this line, makes sure there aren't any invalid replays
			if checkLink:	#and this line
				roundReplayList.append(checkLink)
		usageStats[round]=roundReplayList
		print()

	if not os.path.exists(directory+tourFileTitle+'\\'):
		os.mkdir(directory+tourFileTitle+'\\')
	print("Replay analysis complete.")
	for i in usageStats:
		sys.stdout.write("\rWriting to file: "+directory+tourFileTitle+"\\round%s" % i)
		sys.stdout.flush()
		round_file = open(directory+tourFileTitle+'\\round'+i+'.txt', "w+")
		json.dump(usageStats[i], round_file)
		round_file.close()
	print("Completed Writing Teams")
	UsageAnalyzer.outputStats(tourType, tourFileTitle)
	UsageAnalyzer.outputStats(tourType, tourFileTitle, True, 4)
	UsageAnalyzer.outputStats(tourType, tourFileTitle, True, 6)
	UsageAnalyzer.outputStats(tourType, tourFileTitle, True, 8)

if __name__=="__main__":
	if len(sys.argv) == 1:
		main()
	elif len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])