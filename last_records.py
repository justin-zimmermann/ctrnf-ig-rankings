"""plan:
1) combine 3 console rankings into single ranking for each track, redoing the positions
1a) the algorithm is to compare all 3 times and take the lowest each time, can use queue and threading
1b) 3 queues send times from each console (reading the api pages in a loop) and another thread receives 3 times
1c) simultaneously
1d) data structure is a list of 34 lists of names, a list of 34 lists of times, a list of 34 lists of characters,
a list of 34 lists of console used (position is already the index because the list will be ordered)
1e) while this is going on make a list of each username/console combo
2) for each name in the username/console list, check if they appear in all 34 lists. if yes calculate AF and
total times and add to a new list
2a) once af and tt are complete, reorder the list by ascending order (lowest first)
"""

import sys
from itertools import chain
import requests
import re


class AggregateRankingCalculator():

    def __init__(self, player, order):
        self.user_list = [[] for _ in range(34)]
        self.time_list = [[] for _ in range(34)]
        self.days_since_record_list = [[] for _ in range(34)]
        self.platform_list = [[] for _ in range(34)]
        self.all_users = {}  # set of all different users
        self.limits = []
        self.player = player
        self.order = order

    def run(self):
        mode_list = list(chain(range(1, 36, 2), range(39, 64, 2), range(77, 82, 2))) #list skipping even numbers (relic races)
        for mode_index, mode in enumerate(mode_list):
            self.fetch_rankings_from_csv(mode_index, mode)

        self.get_all_users()
        self.get_player(self.player)

    def track_names(self, i):
        name = {0: "Crash Cove",
                1: "Roo Tubes",
                2: "Mystery Caves",
                3: "Sewer Speedway",
                4: "Slide Coliseum",
                5: "Turbo Track",
                6: "Coco Park",
                7: "Tiger Temple",
                8: "Papu Pyramid",
                9: "Dingo Canyon",
                10: "Blizzard Bluff",
                11: "Dragon Mines",
                12: "Polar Pass",
                13: "Tiny Arena",
                14: "Ngin Labs",
                15: "Cortex Castle",
                16: "Hot Air Skyway",
                17: "Oxide Station",
                18: "Inferno Island",
                19: "Jungle Boogie",
                20: "Tiny Temple",
                21: "Meteor George",
                22: "Barin Ruins",
                23: "Deep Sea Driving",
                24: "Out Of Time",
                25: "Clockwork Wumpa",
                26: "Thunderstruck",
                27: "Assembly Lane",
                28: "Android Alley",
                29: "Electron Avenue",
                30: "Hyper Spaceway",
                31: "Twilight Tour",
                32: "Prehistoric Playground",
                33: "Spyro Circuit"}
        return name[i]

    def get_track_limits(self):
        res = requests.get(r"https://crashteamranking.com/nfrecords/")
        html = str(res.content)
        limits = re.findall("[0-9]:[0-9]{2}.[0-9]{2}", html)[:35]
        limits = [int(limit[0])*60 + int(limit[2:4]) + float(limit[5:7])/100. for limit in limits]
        limit_correct_order = {0:0,
                               1:1,
                               2:4,
                               3:6,
                               4:16,
                               5:17,
                               6:3,
                               7:2,
                               8:8,
                               9:7,
                               10:5,
                               11:9,
                               12:10,
                               13:12,
                               14:14,
                               15:11,
                               16:13,
                               17:15,
                               18:18,
                               19:19,
                               20:20,
                               21:21,
                               22:22,
                               23:23,
                               24:24,
                               25:25,
                               26:26,
                               27:27,
                               28:28,
                               29:29,
                               30:30,
                               31:32,
                               32:33,
                               33:34}
        return [limits[value] for key, value in limit_correct_order.items()]

    def get_glitched_positions(self):
        glitched_positions = []
        for track in range(len(self.time_list)):
            for i in range(len(self.time_list[track])):
                if self.time_list[track][i] >= self.limits[track]:
                    glitched_positions.append(i)
                    break
        return glitched_positions

    def fetch_rankings_from_csv(self, mode_index, mode):
        with open("output/%s.csv" % str(mode), "r") as mode_ranking:
            lines = [line.replace("\n","").split(";") for line in mode_ranking if line.count(";") == 4]
            self.user_list[mode_index] = [line[2] for line in lines]
            self.time_list[mode_index] = [float(line[1])-1. for line in lines]
            self.platform_list[mode_index] = [line[3] for line in lines]
            self.days_since_record_list[mode_index] = [float(line[4]) for line in lines]
            #print(len(self.user_list[mode_index]))

    def get_all_users(self):
        self.all_users = set([(self.user_list[0][i], self.platform_list[0][i]) for i in range(
            len(self.platform_list[0]))])
        for j in range(1, 34):
            self.all_users = self.all_users.union(set([(self.user_list[j][i], self.platform_list[j][i]) for i in range(
            len(self.platform_list[j]))]))
            #

    def format_time(self, time):
        if time - (int(time) // 60)*60 < 10:
            return "%d:0%.3f" % (int(time) / 60, time - (int(time) // 60)*60)
        else:
            return "%d:%.3f" % (int(time) / 60, time - (int(time) // 60) * 60)

    def get_player(self, player):
        order = []
        lines = []
        if (player, "psn") not in self.all_users and (player, "xbl") not in self.all_users and (
                player, "switch") not in self.all_users:
            print("Error: %s is not in the player database. Exiting program." % player)
            return None
        for track in range(len(self.user_list)):
            tr = "\n%s:" % self.track_names(track)
            for position in range(len(self.user_list[track])):
                if self.user_list[track][position] == player:
                    lines.append("%s %s (Rank %d, done %.3f days ago)" % (tr, self.format_time(self.time_list[track][position]),
                                                  position + 1, self.days_since_record_list[track][position]))
                    if self.order == "date":
                        order.append(self.days_since_record_list[track][position])
                    else:
                        order.append(position + 1)
        lines = [line for _,line in sorted(zip(order,lines))]
        print("Player: %s" % player)
        print("Track: Time (Rank, Days since record)")
        for line in lines:
            print(line)
        return None

def main():
    if len(sys.argv) != 3:
        print("correct usage: python %s [player] [orderby:date/ranking]" % sys.argv[0])
        exit()

    player = sys.argv[1]
    order = sys.argv[2]
    if order != "ranking":
        order = "date"

    af_calc = AggregateRankingCalculator(player, order)

    af_calc.run()

if __name__ == '__main__':
    main()
