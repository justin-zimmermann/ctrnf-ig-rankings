import requests
import json

class Reader():

    def __init__(self, platform, mode, maxsize):
        self.platform = platform
        self.mode = mode
        self.maxsize = maxsize
        if platform in ['xbl', 'switch']:
            self.maxsize = maxsize / 2

    def read_ig_rankings(self, callback):

        page = 1

        while True:

            address = "https://my.callofduty.com/api/papi-client/leaderboards/v2/title/ctr/platform/" + self.platform + \
                      "/time/alltime/type/1/mode/" + str(self.mode) + "/page/" + str(page)

            r = requests.get(address)
            try:
                if r.json()['status'] != 'success' or page > self.maxsize:
                    callback(self.platform, 'STOP', 999999.9, 'STOP', 'STOP')
                    break
            except json.decoder.JSONDecodeError:
                print("Trouble connecting to the Activision API. Check your Internet connection.")

            if page%10 == 0:
                print("%s pages done out of %s (%s, %s)" % (page, r.json()['data']['totalPages'], self.platform, self.mode))

            for i in range(20):

                username = r.json()['data']['entries'][i]['username']
                time = r.json()['data']['entries'][i]['values']['time']
                rank = r.json()['data']['entries'][i]['rank']
                days_since_record = r.json()['data']['entries'][i]['updateTime']/(24*3600.)

                callback(self.platform, username, time, rank, days_since_record)

            page += 1
