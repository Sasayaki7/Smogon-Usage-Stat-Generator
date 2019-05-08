Smogon Tournament Usage Stat Analyzer:

v1.0

READ THIS DOCUMENT BEFORE USING THIS PACKAGE:

Before starting anything, create a folder where you want all the Stats to be dumped, and enter the directory into ROOT_DIRECTORY under CONFIG.txt. Do not put a space after the = when doing so.

This program uses Python 3, and uses the following third-party library:
Requests. Can be downloaded here: https://2.python-requests.org/en/master/#
Regex.


Python Scripts which you should be using.

For DUU: DUUShowdownRoundStatCalculator.py   Parameters: roundNumber
For DLT: DLTRoundStatCalculator.py           Parameters: roundNumber
For Seasonal: In Progress     				 Parameters: TBD

For Miscellaneous Single Thread Tournaments: SingleThreadAnalyzer.py           Parameters: ThreadURL, TournamentName, OutputFileName, TierOfTournament