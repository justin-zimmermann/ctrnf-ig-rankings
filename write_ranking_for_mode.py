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

    def __init__(self, maxsize, mode):
        self.maxsize = int(maxsize)
        self.platform = ["psn", "switch", "xbl"]
        self.queue = {}
        self.thread = {}
        for platform in self.platform:
            self.queue[platform] = queue.Queue()
        self.user_list = []
        self.time_list = []
        self.days_since_record_list = []
        self.platform_list = []
        self.all_users = {}  # set of all different users
        self.mode = mode

    def put_to_queue(self, platform, username, time, rank, days_since_record):
        self.queue[platform].put((username, float(time), rank, days_since_record))

    def read_from_server(self, platform):
        reader = read_from_activision_server.Reader(platform, self.mode, self.maxsize)
        reader.read_ig_rankings(self.put_to_queue)

    def run(self):
        start = time.time()
        for platform in self.platform:
            self.thread[platform] = threading.Thread(target=self.read_from_server, args=(platform,))
            self.thread[platform].start()
            print("Starting thread (%s, %s)" % (platform, self.mode))

        reading_thread = threading.Thread(target=self.read_from_queues)
        reading_thread.start()
        reading_thread.join()
        for platform in self.platform:
            self.thread[platform].join()
        finish = time.time()
        print("All reading for mode %s done in %.2f seconds" % (self.mode, finish - start))

        self.write_aggregate_rankings()

    def read_from_queues(self):
        print("Starting reading from queues (%s)" % self.mode)
        empty_queues = 0
        username = {}
        times = {}
        rank = {}
        days_since_record = {}
        for platform in self.platform:
            while self.queue[platform].empty():
                time.sleep(1)
                sys.stdout.write("-")
                sys.stdout.flush()
            username[platform], times[platform], rank[platform], days_since_record[platform] = self.queue[
                platform].get(False)
        while True:
            next_platform = min(times, key=times.get)
            self.user_list.append(username[next_platform])
            self.time_list.append(times[next_platform])
            self.platform_list.append(next_platform)
            self.days_since_record_list.append(days_since_record[next_platform])
            while self.queue[next_platform].empty():
                time.sleep(1)
                sys.stdout.write(".")
                sys.stdout.flush()
            username[next_platform], times[next_platform], rank[next_platform], days_since_record[
                next_platform] = self.queue[next_platform].get(False)
            if rank[next_platform] == 'STOP':
                times[next_platform] = 9999999.
                empty_queues += 1
                print("%s empty queues in %s" % (empty_queues, self.mode))
            if empty_queues == 3:
                break

    def write_aggregate_rankings(self):
        print("Writing rankings to file")
        with open("output/%s.csv" % str(self.mode), 'w') as out:
            for i in range(len(self.time_list)):
                out.write("%s;%.5f;%s;%s;%s\n" % (
                    str(i+1), self.time_list[i], self.user_list[i],
                    self.platform_list[i], self.days_since_record_list[i]))

def main(maxsize, mode):
    af_calc = AggregateRankingCalculator(maxsize=maxsize, mode=mode)
    af_calc.run()

if __name__ == '__main__':
    main()
