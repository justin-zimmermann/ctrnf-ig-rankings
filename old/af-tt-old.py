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
import time
import queue
import threading
from itertools import chain
import read_from_activision_server


class AggregateRankingCalculator():

    def __init__(self, maxsize):
        self.maxsize = int(maxsize)
        self.platform = ["psn", "switch", "xbl"]
        self.queue = [{} for _ in range(33)]
        self.thread = [{} for _ in range(33)]
        for i in range(len(self.queue)):
            for platform in self.platform:
                self.queue[i][platform] = queue.Queue()
        self.user_list = [[] for _ in range(33)]
        self.time_list = [[] for _ in range(33)]
        self.days_since_record_list = [[] for _ in range(33)]
        self.platform_list = [[] for _ in range(33)]
        self.all_users = {}  # set of all different users

    def put_to_queue(self, platform, username, time, rank, days_since_record, mode_index):
        self.queue[mode_index][platform].put((username, float(time), rank, days_since_record))

    def read_from_server(self, platform, mode, mode_index):
        reader = read_from_activision_server.Reader(platform, mode, mode_index, self.maxsize)
        reader.read_ig_rankings(self.put_to_queue)

    def run(self):
        mode_list = list(chain(range(1, 36, 2), range(39, 64, 2), range(77, 80, 2))) #list skipping even numbers (relic races)
        thread_list = []
        for mode_index, mode in enumerate(mode_list):
            thread_list.append(threading.Thread(target=self.run_mode, args=(mode_index, mode)))
            thread_list[-1].start()
        for t in thread_list:
            t.join()

        self.get_all_users()
        self.write_af()

    def run_mode(self, mode_index, mode):
        start = time.time()
        for platform in self.platform:
            self.thread[mode_index][platform] = threading.Thread(target=self.read_from_server, args=(platform, mode, mode_index))
            self.thread[mode_index][platform].start()
            print("Starting thread (%s, %s)" % (platform, mode))

        reading_thread = threading.Thread(target=self.read_from_queues, args=(mode, mode_index))
        reading_thread.start()
        reading_thread.join()
        for platform in self.platform:
            self.thread[mode_index][platform].join()
        finish = time.time()
        print("All reading for mode %s done in %.2f seconds" % (mode, finish - start))

        self.write_aggregate_rankings(mode, mode_index)

    def read_from_queues(self, mode, mode_index):
        print("Starting reading from queues (%s)" % mode)
        empty_queues = 0
        username = {}
        times = {}
        rank = {}
        days_since_record = {}
        for platform in self.platform:
            while self.queue[mode_index][platform].empty():
                time.sleep(1)
                sys.stdout.write("-")
                sys.stdout.flush()
            username[platform], times[platform], rank[platform], days_since_record[platform] = self.queue[mode_index][
                platform].get(False)
        while True:
            next_platform = min(times, key=times.get)
            self.user_list[mode_index].append(username[next_platform])
            self.time_list[mode_index].append(times[next_platform])
            self.platform_list[mode_index].append(next_platform)
            self.days_since_record_list[mode_index].append(days_since_record[next_platform])
            while self.queue[mode_index][next_platform].empty():
                time.sleep(1)
                sys.stdout.write(".")
                sys.stdout.flush()
            username[next_platform], times[next_platform], rank[next_platform], days_since_record[
                next_platform] = self.queue[mode_index][next_platform].get(False)
            if rank[next_platform] == 'STOP':
                times[next_platform] = 9999999.
                empty_queues += 1
                print("%s empty queues in %s" % (empty_queues, mode))
            if empty_queues == 3:
                break

    def write_aggregate_rankings(self, mode, mode_index):
        print("Writing rankings to file")
        with open("output/%s.csv" % str(mode), 'w') as out:
            for i in range(len(self.time_list[mode_index])):
                out.write("%s;%.5f;%s;%s;%s\n" % (
                    str(i+1), self.time_list[mode_index][i], self.user_list[mode_index][i],
                    self.platform_list[mode_index][i], self.days_since_record_list[mode_index][i]))

    def get_all_users(self):
        self.all_users = set([(self.user_list[0][i], self.platform_list[0][i]) for i in range(
            len(self.platform_list[0]))])
        for j in range(1, 33):
            self.all_users = self.all_users.union(set([(self.user_list[j][i], self.platform_list[j][i]) for i in range(
            len(self.platform_list[0]))]))

    def write_af(self):
        af=[]
        for user in self.all_users:
            has_af = True
            sum_position = 0
            for track in range(33):
                has_pos = False
                for position, user2 in enumerate(self.user_list[track]):
                    if user[0] == user2 and user[1] == self.platform_list[track]:
                        sum_position += position + 1
                        has_pos = True
                        break
                if has_pos == False:
                    has_af = False
                    break
            if has_af == True:
                sum_position /= 33.0
                af.append((sum_position, user))
        af.sort()
        print("Writing AF to file")
        with open("output/af.csv", 'w') as out:
            for entry in af:
                print("%s;%s;%s" % (entry[0], entry[1][0], entry[1][1]))
                out.write("%s;%s;%s\n" % (entry[0], entry[1][0], entry[1][1]))

def main():
    if len(sys.argv) != 2:
        print("correct usage: python %s [maxsize]" % sys.argv[0])
        exit()
    maxsize = sys.argv[1] #number of records taken from server

    af_calc = AggregateRankingCalculator(maxsize=maxsize)

    af_calc.run()

if __name__ == '__main__':
    main()
