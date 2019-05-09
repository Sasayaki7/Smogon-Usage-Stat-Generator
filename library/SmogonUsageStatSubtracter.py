import json
import os
import sys
import re
import UsageAnalyzer

pokemonName = re.compile("[a-zA-Z].+?(?=  )")
usewinsmirrors = re.compile("(?<=  )\d+(?= )")

filelocation = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(os.path.dirname(__file__))))
	
f = open(os.path.join(filelocation, 'CONFIG.txt'))

rootdirectory = re.search("(?<=ROOT_DIRECTORY=).+", f.read()).group(0)
directory = rootdirectory+'Usage Stats\\'

def readFileContents(fileName):
	pokemonDict = {}
	with open(directory+fileName, "r") as f:
		for line in f:
			nums = re.search("\d%", line) 
			if nums != None:
				pokemon = pokemonName.search(line).group(0)
				usewinmirror = usewinsmirrors.findall(line)
				use = usewinmirror[0]
				win = usewinmirror[1]
				mirror = usewinmirror[2]
				pokemonDict[pokemon] = {"W": int(win), "usage": int(use), "mirror": int(mirror)}
	return pokemonDict


def subtractStats(cumulativeStatFile, prevCumulativeStatFile, fileTitle, tourName):
	cumulativeList = readFileContents(cumulativeStatFile)
	prevCumulativeList = readFileContents(prevCumulativeStatFile)
	total = 0
	for pokemon in prevCumulativeList.keys():
		if pokemon in cumulativeList:
			uselist = cumulativeList[pokemon]
			oldList = prevCumulativeList[pokemon]
			uselist["W"] = uselist["W"]-oldList["W"]
			uselist["usage"] = uselist["usage"]-oldList["usage"]
			total = total+uselist["usage"]
			uselist["mirror"] = uselist["mirror"]-oldList["mirror"]
			if cumulativeList[pokemon]["usage"] == 0:
				del cumulativeList[pokemon]
	total = total/6
	UsageAnalyzer.writeStats(fileTitle, tourName, cumulativeList, total)
	

def main(cumulativeStatFile, prevCumulativeStatFile, fileTitle, tourName):	
	subtractStats(cumulativeStatFile, prevCumulativeStatFile, fileTitle, tourName)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])