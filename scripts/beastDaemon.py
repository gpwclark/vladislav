#!/usr/bin/python3

import sys
import os
import time
import shutil
import datetime
from time import mktime
from pathlib import Path
from datetime import datetime
from datetime import timedelta


class theBeast:
    def __init__(self, path_to_watch, dest_path):
        self.path_to_watch = path_to_watch
        self.dest_path = dest_path
        self.sleep_time = 60
        self.file_sleep_time = 5
        self.wait_tolerance = 12
        self.datetimefmt = '%Y-%m-%d-%H-%M-%S'
        self.temp_file = "/var/tmp/THE_BEAST_FILEBOT_LOG.txt"
        if not os.path.isfile(self.temp_file):
            self.writeNewTimestamp()
        if not self.path_to_watch.endswith("/"):
            print("first argument must end with a '/'")
            exit()

    def timeStamped(self):
        return datetime.now().strftime(self.datetimefmt)

    def timeStructToTimeObj(self, timestruct):
        return datetime.fromtimestamp(mktime(timestruct))

    def getTimeStruct(self, timestr):
        return time.strptime(timestr, self.datetimefmt)

    def hourSinceLastRun(self):
        # Precondition is that file exists because it is created in init.
        with open(self.temp_file, 'r') as f:
            data = f.read()
            lastrun = self.getTimeStruct(data)

            anhour = timedelta(hours=1)

            lastrun_plus_anhour = self.timeStructToTimeObj(lastrun) + anhour
            currtime = self.timeStructToTimeObj(self.getTimeStruct(self.timeStamped()))

            return (lastrun_plus_anhour < currtime)

    def writeNewTimestamp(self):
        with open(self.temp_file, 'a+') as f:
            f.seek(0)
            f.write(self.timeStamped())
            f.truncate()

    def runFilebot(self):
        #once filebot command is working.
        pass

    def xferFinished(self, file_name):
        shutil.move(file_name, self.dest_path)

    def get_size(self, filePath):
        total_size = os.path.getsize(filePath)
        if os.path.isfile(filePath):
            return total_size
        else:
            for item in os.listdir(filePath):
                itempath = os.path.join(filePath, item)
                if os.path.isfile(itempath):
                    total_size += os.path.getsize(itempath)
                elif os.path.isdir(itempath):
                    total_size += self.get_size(itempath)
        return total_size

    def waitForXfer(self, filepath):
        same_count = 0
        before = self.get_size(filepath)

        while (same_count < self.wait_tolerance):
            time.sleep(self.file_sleep_time);
            after = self.get_size(filepath)
            if before == after:
                same_count = same_count + 1
            else:
                same_count = 0
            before = after
        return True


    # monitor() runs in a while (True) loop. If no files are in the
    # path_to_watch, then it waits 1 minute until it scans the path again. When
    # it finds files in the path it processes them one at a time. First it makes
    # sure the file is done transferring (files are copied into
    # path_to_watch folder so they could theoretically still be copying), and
    # then it moves those files to the dest_path.
    # when files are finished downloading I need to see if it has been an hour
    # (you aren't supposed to call filebot too much),
    # if it has been more than an hour since filebot was last run then I need
    # to run filebot and then write to the file the current time. If it has not
    # been more than an hour then continue
    def monitor(self):

        while (True):
            dirs = os.listdir(self.path_to_watch)

            if not dirs:
                time.sleep(self.sleep_time)
            else:
                dirs = os.listdir(self.path_to_watch)
                for item in dirs:
                    path = self.path_to_watch + item
                    self.waitForXfer(path)
                    self.xferFinished(path)
                if self.hourSinceLastRun():
                    self.runFilebot()
                    self.writeNewTimestamp()

if __name__ == "__main__":
    beast = theBeast(path_to_watch = sys.argv[1], dest_path = sys.argv[2])
    beast.monitor()
