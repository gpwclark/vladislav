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
# 2. EVENT: 
#
#
#
#

class theBeast:        
    def __init__(self, m_file, ifttt_api_key):
        self.subsetTolerance = .5
        self.timeToWait = 2160 
        self.m_file = m_file
        self.m_file_as_set = self.stringToSet(m_file)
        self.ifttt_api_key = ifttt_api_key
        self.api_endpoint = "https://maker.ifttt.com/trigger/torrent_ready/with/key/" + self.ifttt_api_key
        self.api_endpoint_talk = "https://maker.ifttt.com/trigger/talk_to_vlad/with/key/" + self.ifttt_api_key
        payload = {'value1': "don't call me that arsehole"}
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
        if (ratio > self.subsetTolerance):
            return True
        
    def containsFilename(self, added):
        for elem in added:
            print ("the elem: ")
            if (self.isAlmostSubset(elem)):
                return elem

    def xferFinished(self, dirToMonitor):
        # send cmd for vlad to remem that self.m_file is pending xfer.
        rememcmd = "remem " + "\"" + dirToMonitor + "\"" + " is pending_xfer"
        payload = {'value1' : rememcmd}
        r = requests.post(self.api_endpoint, data=payload)
        print("remem pending cmd: ", r.status_code,r.reason)

    def waitForXfer(self):
        # send cmd for vlad to forget that self.m_file was downloading.
        forgetcmd = "forget " + "\"" + self.m_file + "\""
        payload = {'value1': forgetcmd}
        r = requests.post(self.api_endpoint, data=payload)
        print("forget downloading cmd: ", r.status_code, r.reason)
        #TODO WAIT FUNCTIONALITY GOES HERE


    def monitor(self):
        path_to_watch = "/home/emby/movies/torrents/"
        fileTransferring = True 
        foundMatch = False
        count = 0

        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        currLs = [f for f in before]

        foundMatch = self.containsFilename(currLs)
        if foundMatch:
            print("I got the match, it was already there ", foundMatch)
            fileTransferring = False
            self.xferFinished(foundMatch)
            self.waitForXfer()

        # fileTransferring is false when the file is found, and
        # 2160 is the number of 10 second increments that equals
        # 6 hours, which is as long as I want this script to 
        # wait. After 12 hours that file is probably not coming.

        print ("monitoring")
        while (fileTransferring and (count < self.timeToWait)):
            count = count + 1
            time.sleep (10)
            after = dict ([(f, None) for f in os.listdir (path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]

            if added:
                addedStr = "Added: ", ", ".join (added)
                print(addedStr)
                foundMatch = self.containsFilename(added)
                if foundMatch:
                    print("I got the match ", foundMatch)
                    fileTransferring = False
                    self.xferFinished(foundMatch)
                    self.waitForXfer()
            if removed: 
                removedStr = "Removed: ", ", ".join (removed)
                payload = {'value1': removedStr}
                r = requests.post(self.api_endpoint, data=payload)
                print(r.status_code, r.reason)
            before = after

        if (count == self.timeToWait):
            # tell vlad to remember the file was not found.
            rememcmd = "remem " + "\"" + self.m_file + "\"" " is failed_xfer"
            payload = {'value1': rememcmd}
            r = requests.post(self.api_endpoint, data=payload)


if __name__ == "__main__":
    beast = theBeast(m_file=sys.argv[1],ifttt_api_key=sys.argv[2])
    beast.monitor()

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
