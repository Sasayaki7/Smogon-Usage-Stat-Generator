Smogon Tournament Usage Stat Analyzer:

v1.0

READ THIS DOCUMENT BEFORE USING THIS PACKAGE:

~~~~~~~~~~~~~~~~WARNINGS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This program has been adapted for Windows Use. Functionality with iOS and Linux is not Guaranteed.

Before starting anything, create a folder where you want all the Stats to be dumped, and enter the directory into ROOT_DIRECTORY under CONFIG.txt. 
Do not put a space after the = when doing so.

This program uses Python 3, and uses the following third-party library:
Requests. Can be downloaded here: https://2.python-requests.org/en/master/#

Note: This program scans the replay for Mega Pokemon, and if a Mega Pokemon is not found, will look at used items and mechanics (such as Knock Off) to make a best guess for a Mega. Therefore, it is possible that actual mega usage may deviate.
Currently only supports Doubles Formats
Currently, the banlist is updated manually. 
Currently cannot analyze threads with multiple tiers (i.e. DPL, SPL). 

~~~~~~~~~~~~~~~~~~~~~~~FUNCTIONALITY AND USE~~~~~~~~~~~~~~~~~~~~~

This program scrapes threads for replays, analyzes the replay for teams, megas and the winner, and saves the information into a JSON file with an appropriate title.
A second program takes the JSON files created in the first section, compiles the information, and outputs the Usage Stats into a readable format.

Python Scripts which you should be using.

For DUU: DUUShowdownRoundStatCalculator.py   Parameters: roundNumber
For DLT: DLTRoundStatCalculator.py           Parameters: roundNumber
For Seasonal: In Progress     				 Parameters: TBD

For Miscellaneous Single Thread Tournaments: SingleThreadAnalyzer.py           Parameters: ThreadURL, TournamentName, OutputFileName, TierOfTournament


~~~~~~~~~~~~~~~~~~~~~~REFERENCE INFO (DO NOT HAVE TO READ)~~~~~~~~~~~~~~~
UsageAnalyzer.py can be used to generate usage stats from existing JSON data.





