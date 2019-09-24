# ctrnf-ig-rankings

in order to run this script you need Python 3.0 or higher.

You also need the library "requests" (type: "pip install requests" in the terminal once you've installed python)

To fetch all rankings from activision database, go in the terminal, move into the directory of the project
and type "python write_ranking.py". The rankings for each track will be written into a .csv file in the folder
"output" which you created. Note that this will take a long time to execute.

To calculate af once you have the rankings, run "python af.py". The result will be in a .csv file in the output folder.

To get matchups vs several other players, run "python matchups.py "player1" "player2" "etc..."" replacing playerX with the usernames of the players you want to compare. This is especially useful to gauge the strength of an online lobby.

To get a player's last records, in the order they were made from most recent to oldest, run "python last_records.py "player"", replacing player with the username of the player you want the times of.

Note the "" are not necessary unless the player has a whitespace character in his username, which can only happen on xbox. If there are no whitespaces, you can just run: "python matchups.py player1 player2 etc..." and "python last_records.py player"

I'm working on improving the af.py file to be more user friendly and automatically restarting time fetching in case of server connection failure.
