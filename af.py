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


class AggregateRankingCalculator():

    def __init__(self):
        self.user_list = [[] for _ in range(34)]
        self.time_list = [[] for _ in range(34)]
        self.days_since_record_list = [[] for _ in range(34)]
        self.platform_list = [[] for _ in range(34)]
        self.all_users = {}  # set of all different users

    def run(self):
        mode_list = list(chain(range(1, 36, 2), range(39, 64, 2), range(77, 82, 2))) #list skipping even numbers (relic races)
        for mode_index, mode in enumerate(mode_list):
            self.fetch_rankings_from_csv(mode_index, mode)

        self.get_all_users()
        self.write_af(exclude_glitched_tracks=True, total_times=True)

    def fetch_rankings_from_csv(self, mode_index, mode):
        with open("output/%s.csv" % str(mode), "r") as mode_ranking:
            lines = [line.replace("\n","").split(";") for line in mode_ranking if line.count(";") == 4]
            self.user_list[mode_index] = [line[2] for line in lines]
            self.time_list[mode_index] = [float(line[1]) for line in lines]
            self.platform_list[mode_index] = [line[3] for line in lines]
            self.days_since_record_list[mode_index] = [float(line[4]) for line in lines]
            print(len(self.user_list[mode_index]))

    def get_all_users(self):
        self.all_users = set([(self.user_list[0][i], self.platform_list[0][i]) for i in range(
            len(self.platform_list[0]))])
        for j in range(1, 34):
            self.all_users = self.all_users.union(set([(self.user_list[j][i], self.platform_list[j][i]) for i in range(
            len(self.platform_list[j]))]))
            print(len(self.all_users))

    def write_af(self, exclude_glitched_tracks=False, exclude_glitched_times=False, total_times=False):
        af=[]
        if total_times == True:
            filename = "tt"
        else:
            filename = "af"
        if exclude_glitched_tracks == True:
            track_list = list(chain(range(0, 1), range(2, 5), range(10, 14), range(15, 16), range(18, 25), range(
                27, 29), range(30, 31)))
            print(track_list)
            extra = "_no_glitched_tracks"
        else:
            track_list = list(range(34))
            extra = ""
        n_tracks = len(track_list)
        for user in self.all_users:
            has_af = True
            sum_position = 0
            sum_days = 0
            for track in track_list:
                has_pos = False
                for position in range(len(self.user_list[track])):
                    if user[0] == self.user_list[track][position] and user[1] == self.platform_list[track][position]:
                        if total_times == False:
                            sum_position += position + 1
                        else:
                            sum_position += self.time_list[track][position]
                        if user[0] == "ctr4ever-Justin":
                            print(position + 1)
                        sum_days += self.days_since_record_list[track][position]
                        has_pos = True
                        break
                if has_pos == False:
                    has_af = False
                    break
            if has_af == True:
                if total_times == False:
                    sum_position /= float(n_tracks)
                sum_days /= float(n_tracks)
                af.append((sum_position, user, sum_days))
        af.sort()
        print("Writing AF to file")
        with open("output/%s%s.csv" % (filename, extra), 'w') as out:
            for i, entry in enumerate(af):
                #print("%s;%s;%s;%s;%s" % (i+1, entry[0], entry[1][0], entry[1][1], entry[2]))
                out.write("%s;%s;%s;%s;%s\n" % (i+1, entry[0], entry[1][0], entry[1][1], entry[2]))

def main():
    if len(sys.argv) != 1:
        print("correct usage: python %s" % sys.argv[0])
        exit()

    af_calc = AggregateRankingCalculator()

    af_calc.run()

if __name__ == '__main__':
    main()
