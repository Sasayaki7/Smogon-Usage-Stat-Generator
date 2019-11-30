import sys
sys.path.insert(0, 'library')

import SmogonUsageStatSubtracter as suss
import SingleThreadAnalyzer as sta


#--------------------------------------------------------------------------------------------------------
#This program uses previous usage stats and subtracts out the previous usage stat from the current usage stat in order to calculate the current round usage stats.

#--------------------EDIT ONLY THIS SECTION FOR GUARANTEED SUCCESS--------------------------------------
thread = "https://www.smogon.com/forums/threads/doubles-ladder-tournament-2019-won-by-smb.3648614" 
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
	ft = ""
	#variable to be used; set here because scopes
	
	if round == None: 
		#if round parameter wasn't given in initial call, prompt it here
		round = input("Please enter round number as an integer. (1, 2, 3):  ")

	if int(round) == 1: 
		#if it's the first round, we set the title of the file and the header accordingly.
		ft = headerOfFile+"1"
		fileName = filePrefix+"1"
		
	elif int(round) > 1:
		#if it's later than the first round, we title the file 1-to-@round so that it is clear for the program in future rounds
		ft = headerOfFile+"1-"+str(round)
		fileName = filePrefix+"1to"+str(round)
		
	else:
		raise Exception("Invalid round input: {}. round must be an integer greater than 1".format(round))
		#We don't want invalid inputs messing up the program.
		
	sta.main(thread, ft, fileName, format)
		#parses the parameters to the main function in SingleThreadAnalyzer, which analyzes all the replays contained in the thread with given url, 
		#compiles teams and winners into a separate file, and derives the Cumulative usage stats from the saved teams. 
	
	#Section below relates to outputting current round's usage stats if it is beyond round 1
	
	if int(round) > 1:
		#If the given round is greater than 1, to obtain the usage stat, we subtract out the previous round's cumulative usage stat from this round's cumulative usage stat
		if int(round) > 2:
			#Because the previous round's cumulative usage stat filename differs between round 1 and round 2 onwards, we note the difference in filename here 
			prevFile = filePrefix+"1to"+str(int(round)-1)
			
		else:
			prevFile = filePrefix+"1"
			
		suss.subtractStats(fileName+".txt", prevFile+".txt", filePrefix+str(round), headerOfFile+str(round))
		#Takes the filenames of the cumulative usage stats of this round and previous rounds, and subtracts the previous round from this round, and outputs the file.
		
		print(fileName, prevFile)
		#print the file names of the previous round's cumulative usage stat and this week's cumulative usage stat as a sanity check
		
if __name__ == "__main__":
	#Required if calling directly from the terminal. Overloaded, so can run with both an argument (roundName) or None. If no roundName, we prompt for it in the main function
	if len(sys.argv) == 2:
		main(sys.argv[1])
	elif len(sys.argv) == 1:
		main()
	else:
		print("Error: DLTRoundStatCalculator only takes up to 1 parameter")
		#Alerts user if there is multiple parameters