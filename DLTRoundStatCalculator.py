import sys
sys.path.insert(0, 'library')

import SmogonUsageStatSubtracter as suss
import SingleThreadAnalyzer as sta


#--------------------------------------------------------------------------------------------------------
#This program uses previous usage stats and subtracts out the previous usage stat from the current usage stat in order to calculate the current round usage stats.

#--------------------EDIT ONLY THIS SECTION FOR GUARANTEED SUCCESS--------------------------------------
thread = "https://www.smogon.com/forums/threads/duu-spring-showdown-ii-top-8-on-post-69-lol.3649001" 
#URL OF THREAD. DOES NOT NEED TO BE UPDATED EVERY TITLE CHANGE BUT TAKE OFF THE FINAL SLASH IN URL. 
#BAD EXAMPLE: "https://smogon.com/forums/threads/potatoes-are-good.37123712/"  ->  GOOD EXAMPLE: "https://smogon.com/forums/threads/potatoes-are-good.37123712"  

headerOfFile = "DLT 2019"
#Line 1 Header. Does not need to be updated every round, but needs to be updated every new Ladder Tournament.

filePrefix = "usum-dlt-2019-round-"
#Name of File. Do not change throughout the course of the tournament.


format = "gen7doublesou"
#Obviously needs to change in new generation



#--------------------------END EDIT SECTION------------------------------


prevFile = ""
fileName = ""

def main(r=None):
	round = r
	if round == None:
		round = input("Please enter round number as an integer. (1, 2, 3):  ")
	ft = ""
	if int(round) == 1:
		ft = headerOfFile+"1"
		fileName = filePrefix+"1"
	elif int(round) > 1:
		ft = headerOfFile+"1-"+str(round)
		fileName = filePrefix+"1to"+str(round)
	else:
		raise Exception("Invalid round input: {}. round must be an integer greater than 1".format(round))
	sta.main(thread, ft, fileName, format)
	if int(round) > 1:
		if int(round) > 2:
			prevFile = filePrefix+"1to"+str(int(round)-1)
		else:
			prevFile = filePrefix+"1"
		suss.subtractStats(fileName+".txt", prevFile+".txt", filePrefix+str(round), headerOfFile+str(round))
		print(fileName, prevFile)
	
if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	elif len(sys.argv) == 1:
		main()
	else:
		print("Error: DUUShowdownRoundStatCalculator only takes up to 1 parameter")