# ctrnf-ig-rankings

in order to run this script you need a Python 3 installation.

You also need the library "requests" (type: 
```shell
pip install requests
```
in the terminal once you've installed python)

To fetch all rankings from activision database, go in the terminal, move into the directory of the project
and type 
```shell
python write_ranking.py
```
The rankings for each track will be written into a .csv file in the folder
"output" which you created. 

Note that this will overwrite any ranking you had in the output folder! To keep both your old rankings and the new one you want to fetch, create a new output folder and rename the old one!

Also please note that this will take a long time to execute.

To calculate af once you have the rankings, run 
```shell
python af.py
```
You will be prompted to enter values to specify which kind of ranking you want (total times/average finish, with/without glitched times, minimum number of submissions to appear in the ranking). Type the value you want and press Enter each time.
The result of the script will be in a .csv file in the output folder.

To get matchups vs several other players, run 
```shell
python matchups.py "player1" "player2" "etc..."
```
replacing player1,2,... with the usernames of the players you want to compare. This is especially useful to gauge the strength of an online lobby.

To get a player's last records, in the order they were made from most recent to oldest, run 
```shell
python last_records.py "player" date
```
, replacing player with the username of the player you want the times of.
If instead you want records in the order from best to worst ranking, run 
```shell
python last_records.py "player" ranking
```


Note the "" are not necessary unless the player has a whitespace character in his username, which can only happen on xbox. If there are no whitespaces, you can just run: 
```shell
python matchups.py player1 player2 etc...
```
and 
```shell
python last_records.py player date/ranking
```
I'm working on adding points ranking, asking the user for permission to overwrite files, and automatically restarting time fetching in case of server connection failure.
