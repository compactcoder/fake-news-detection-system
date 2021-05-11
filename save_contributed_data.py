import csv
import os
import re
from datetime import datetime

class GetDateTime():
    def __init__(self):
        self.dt = datetime
    def get_current_date(self):
        dtNow = self.dt.now()
        curr_date = dtNow.date().strftime('%d/%m/%Y')
        return curr_date
    def get_current_time(self):
        dtNow = self.dt.now()
        curr_time = dtNow.time().strftime('%H:%M:%S')
        return curr_time

class CheckURL():
    def __init__(self):
        self.regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        self.url_list = None

    def is_url(self, string):
        self.url_list = re.findall(self.regex, string)
        # print(self.url_list)
        if len(self.url_list) >= 1:
            return True
        else:
            return False

    def get_url(self):
        return [x[0] for x in self.url_list][0]

class Contribution():
    def __init__(self,csvpath):
        self.DT = GetDateTime()
        self.csv_path = csvpath
        self.sno = 1
        if not os.path.isfile(self.csv_path):
            file = open(self.csv_path, 'x+', newline='')
            writer = csv.writer(file)
            writer.writerow(['Sno', 'News', 'Label', 'Source', 'Date', 'Time', 'ip'])
            file.close()
            print("file created")

    def open_csv(self):
        self.file = open(self.csv_path, 'a+', newline='')
        self.writer = csv.writer(self.file)
        print("csv opened")

    def close_csv(self):
        self.file.close()
        self.writer = None
        self.reader = None

    def add_to_csv(self,news,label,source,ip):
        current_date = self.DT.get_current_date()
        current_time = self.DT.get_current_time()
        self.writer.writerow([self.sno, news, label, source, current_date, current_time, ip])
        # print("data added successfully")
        self.sno +=1
        # if not self.sno%10:
        #     self.close_csv()
        #     print("data added successfully")
        # self.open_csv()

class Fetching():
    def __init__(self,csvpath):
        self.csv_path = csvpath
        self.sno = 1

    def open_csv(self):
        self.file = open(self.csv_path, 'r', newline='')
        self.reader = csv.reader(self.file)
        next(self.reader)

    def get_next_records(self):
        fetched_data = next(self.reader)
        return fetched_data
        # for r in self.reader:
        #     print(r)
    def close_csv(self):
        self.file.close()
        self.writer = None
        self.reader = None
