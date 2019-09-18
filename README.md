# ctrnf-ig-rankings

in order to run this script you need Python 3.0 or higher.

You also need the library "requests" (type: "pip install requests" in the terminal once you've installed python)

To fetch all rankings from activision database, go in the terminal, move into the directory of the project
and type "python write_ranking.py". The rankings for each track will be written into a .csv file in the folder
"output" which you created. Note that this will take a long time to execute.

To calculate af once you have the rankings, run "python af.py". The result will be in a .csv file in the output folder.

I'm working on including player matchups, total points, and improving the interface.
