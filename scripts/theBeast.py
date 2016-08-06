#!/usr/bin/python3
import sys
import re
import os
import time
import requests

# The Beast's job is to take the name of the torrent and monitor
# the path_to_watch for that torrent's corresponding download. When the
# torrent's corresponding download is finished scp-ing to the path_to_watch
# (New files are scp-ed to the path_to_watch when a given torrent has finished
# downloading) this program issues an api request to IFTTT so the IFTTT bot
# can tell vlad the file is ready to be moved to the appropriate folder.

###############################################################################
#################################### order ####################################
###############################################################################
#
# 1.EVENT: torrent file uploaded to dropbox
#       TRIGGERS: vlad remem "{{Filename}}" is downloading
#           |-> "{{Filename}}" stored in robot-brain
#       TRIGGERS: vlad awaken the beast {{Filename}} has been uploaded to dropbox.
#           |-> theBeast.py runs waiting for {{Filename}}
# 2. EVENT: torrent file appears in /home/emby/movies/torrents/
#       TRIGGERS:
#
#
#TODO make sure we send slack messages if something goes poorly.

class theBeast:
    def __init__(self, m_file, ifttt_api_key, path_to_watch):
        self.subset_tolerance = .5
        self.time_to_wait = 2160
        self.path_to_watch = path_to_watch
        self.m_file = m_file
        self.m_file_as_set = self.stringToSet(m_file)
        self.ifttt_api_key = ifttt_api_key
        self.api_endpoint = "https://maker.ifttt.com/trigger/torrent_ready/with/key/" + self.ifttt_api_key
        self.api_endpoint_talk = "https://maker.ifttt.com/trigger/talk_to_vlad/with/key/" + self.ifttt_api_key
        payload = {'value1': "vlad remem " + "\"" + self.m_file + "\"" + " is downloading"}
        r = requests.post(self.api_endpoint_talk, data=payload)

    def stringToSet(self, string):
        tokenSet = set()
        alphanumericWords = re.split(r'\W+', string, flags=re.IGNORECASE)
        for word in alphanumericWords:
            tokenSet.add(word)
        return tokenSet

    # The self.m_file is the torrent file. A potential match (as in a
    # downloaded file that appears in path_to_watch)in the added list
    # will not have the exact same name as the self.m_file but it will
    # be more or less a subset, e.g.
    # self.m_file: Alex G - EASY - 2011 (WEB - MP3 - V0 (VBR))-31511159.torrent
    # and it's corresponding file:
    # in added: Alex G - EASY - 2011 - V0

    def isAlmostSubset(self, folderSet):
        folderSet = self.stringToSet(folderSet)
        origLen = len(folderSet)
        intersecLen = len(folderSet.intersection(self.m_file_as_set))
        ratio = float(intersecLen) / float(origLen)
        if (ratio > self.subset_tolerance):
            return True

    def containsFilename(self, added):
        for elem in added:
            if (self.isAlmostSubset(elem)):
                return elem

    def xferFinished(self, dir_to_monitor):
        # send cmd for vlad to remem that self.m_file is pending xfer.
        rememcmd = "remem " + "\"" + dir_to_monitor + "\"" + " is pending_xfer"
        payload = {'value1' : rememcmd}
        r = requests.post(self.api_endpoint, data=payload)
        print("remem pending cmd: ", r.status_code,r.reason)

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

    def waitForXfer(self, dir_to_monitor):
        # send cmd for vlad to forget that self.m_file was downloading.
        forgetcmd = "forget " + "\"" + self.m_file + "\""
        payload = {'value1': forgetcmd}
        r = requests.post(self.api_endpoint, data=payload)
        print("forget downloading cmd: ", r.status_code, r.reason)
        filepath = self.path_to_watch + dir_to_monitor
        #TODO turn 60 and 10 into wait_period and non_changing_threshold
        count = 0
        same_count = 0
        before = self.get_size(filepath)

        #TODO need to verify all paths of this method are traversed
        while (count < 60):
            print("before: ", before)
            time.sleep(20)
            after = self.get_size(filepath)
            if before == after:
                same_count = same_count + 1
                if same_count == 10:
                    return True
            else:
                print("change")
                same_count = 0
            before = after
            count = count + 1


        if count == 60:
            payload = {'value1': "theBeast.py: infinite loop in waitForXfer breakout!"}
            r = requests.post(self.api_endpoint_talk, data=payload)
        return False

    def monitor(self):
        fileTransferring = True
        foundMatch = False
        count = 0

        before = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
        currLs = [f for f in before]

        foundMatch = self.containsFilename(currLs)
        if foundMatch:
            print("I got the match, it was already there ", foundMatch)
            fileTransferring = False
            if self.waitForXfer(foundMatch):
                self.xferFinished(foundMatch)

        # fileTransferring is false when the file is found, and
        # 2160 is the number of 10 second increments that equals
        # 6 hours, which is as long as I want this script to
        # wait. After 12 hours that file is probably not coming.

        print ("monitoring")
        while (fileTransferring and (count < self.time_to_wait)):
            count = count + 1
            time.sleep (10)
            after = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]

            if added:
                foundMatch = self.containsFilename(added)
                if foundMatch:
                    print("I got the match ", foundMatch)
                    fileTransferring = False
                    if self.waitForXfer(foundMatch):
                        self.xferFinished(foundMatch)
            before = after

        if (count == self.time_to_wait):
            # tell vlad to remember the file was not found.
            rememcmd = "remem " + "\"" + self.m_file + "\"" " is failed_xfer"
            payload = {'value1': rememcmd}
            r = requests.post(self.api_endpoint, data=payload)


if __name__ == "__main__":
    beast = theBeast(m_file = sys.argv[1],
            ifttt_api_key = sys.argv[2],
            path_to_watch = sys.argv[3])
    beast.monitor()
    #beast.waitForXfer("francis blah")

# Original monitoring script: http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
#import os, time
#path_to_watch = "."
#before = dict ([(f, None) for f in os.listdir (path_to_watch)])
#while 1:
  #time.sleep (10)
  #after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  #added = [f for f in after if not f in before]
  #removed = [f for f in before if not f in after]
  #if added: print "Added: ", ", ".join (added)
  #if removed: print "Removed: ", ", ".join (removed)
  #before = after
