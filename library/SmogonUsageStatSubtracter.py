import json
import os
import sys
import re
import UsageAnalyzer

pokemonName = re.compile("[a-zA-Z].+?(?=  )")
usewinsmirrors = re.compile("(?<=  )\d+(?= )")
#Regex to identify Pokemon names and Uses and mirrors and wins.

filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__))))
f = open(os.path.join(filelocation, 'CONFIG.txt'))
rootdirectory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)
directory = rootdirectory+'Usage Stats\\'
#Get directory access to saved usage stats



"""Scans usageStat files and turns it into a dictionary of wins, usage, and mirrors, like the original.
Parameters: String fileName
Returns: Dictionary pokemonDict
"""
def readFileContents(fileName):
	pokemonDict = {}
	#Creates dictionary.
	
	with open(directory+fileName, "r") as f:
		for line in f:
		#Opens up fileName and goes through each line
		
			nums = re.search("\d%", line) 
			if nums != None:
			#Scans and checks to see if there are any pecentages in that line (This should ignore title and headers)
			
				pokemon = pokemonName.search(line).group(0)
				usewinmirror = usewinsmirrors.findall(line)
				#Finds all the numbers in that line without %s or in a pokemon name (because Porygon2 exists)
				
				use = usewinmirror[0]
				win = usewinmirror[1]
				mirror = usewinmirror[2]
				#Usage, wins, and mirrors should be found in that order
				
				pokemonDict[pokemon] = {"W": int(win), "usage": int(use), "mirror": int(mirror)}
				#Formats it into a dictionary where key is the pokemon name
				
	return pokemonDict



"""Subtracts the usageStat of @prevCumulativeStatFile from @cumulativeStatFile, and outputs result as a usageStat file titled @fileTitle.
Parameters: String cumulativeStatFile, String prevCumulativeStatFile, String fileTitle, String tourName
Returns Nothing
"""
def subtractStats(cumulativeStatFile, prevCumulativeStatFile, fileTitle, tourName):
	cumulativeList = readFileContents(cumulativeStatFile)
	#Gets the Dictionary of useful data from @cumulativeStatFile
	
	prevCumulativeList = readFileContents(prevCumulativeStatFile)
	#Gets the Dictionary of useful data from @prevCumulativeStatFile
	
	total = 0
	#Tracks the total pokemon used
	
	for pokemon in cumulativeList.keys():
	#Iterates through all the pokemon found in @prevCumulativeList
	
		if pokemon in prevCumulativeList:
			#If the pokemon is found in @cumulativeList, we subtract out the usage, win, and mirrors from @cumulativeList
			
			#Temp variable to store the Dictionary in the given key @pokemon
			uselist = cumulativeList[pokemon]
			oldList = prevCumulativeList[pokemon]
			
			
			uselist["W"] = uselist["W"]-oldList["W"]
			uselist["usage"] = uselist["usage"]-oldList["usage"]
			total = total+uselist["usage"]
			uselist["mirror"] = uselist["mirror"]-oldList["mirror"]
			#Subtraction
			
		else:
			total = total+cumulativeList[pokemon]["usage"]
            
            
	#Number of teams.
	total = total/6
    
	array = dict()
	for pokemon in cumulativeList.keys():
		if cumulativeList[pokemon]["usage"] != 0:
			array[pokemon] = cumulativeList[pokemon]
			
	#Output the usageStat file 
	UsageAnalyzer.writeStats(fileTitle, tourName, cumulativeList, total)
	
#Exists purely to be able to be called directly from the terminal
def main(cumulativeStatFile, prevCumulativeStatFile, fileTitle, tourName):	
	subtractStats(cumulativeStatFile, prevCumulativeStatFile, fileTitle, tourName)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
