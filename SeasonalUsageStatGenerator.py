import SmogonUsageStats as tourUsage

#--------------------------------------------------------------------------------------------------------
#This program scans the Smogon Circuit Tournament Page and Looks for Threads with the same prefix, and compiles them into a single usage stat.

#--------------------EDIT ONLY THIS SECTION FOR GUARANTEED SUCCESS--------------------------------------
seasonalName = "USUM Doubles Spring Seasonal" 
#Name of Seasonal Tournament

headerOfFile = "USUM Doubles OU Spring Seasonal 2019"
#Line 1 Header. Does not need to be updated every round, but needs to be updated every new Ladder Tournament.

fileName = "usum-dou-spring-seasonal-2019"
#Name of File. Do not change throughout the course of the tournament.


format = "gen7doublesou"
#Obviously needs to change in new generation



#--------------------------END EDIT SECTION------------------------------


tourUsage.main(seasonalName, filePrefix)