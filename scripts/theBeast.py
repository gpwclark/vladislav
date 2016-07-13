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

class theBeast:        


    def __init__(self, m_file, ifttt_api_key):
        self.m_file = m_file
        self.m_file_as_set = self.stringToSet(m_file)
        self.ifttt_api_key = ifttt_api_key
        self.api_endpoint = "https://maker.ifttt.com/trigger/torrent_ready/with/key/" + self.ifttt_api_key

    def stringToSet(self, string):
        tokenSet = set()
        alphanumericWords = re.split(r'\W+', string, flags=re.IGNORECASE)
        for word in alphanumericWords:
            tokenSet.add(word)
        return tokenSet

    # The self.m_file is the torrent file. A potential match (as in a
    # downloaded file that appears in path_to_watch)in the added list
    # will not have the exact same name as the self.m_file but it will
    # be a proper subset, e.g. 
    # self.m_file: Alex G - EASY - 2011 (WEB - MP3 - V0 (VBR))-31511159.torrent
    # and it's corresponding file:
    # in added: Alex G - EASY - 2011 - V0

    def containsFilename(self, added):
        for elem in added:
            if (self.stringToSet(elem).issubset(self.m_file_as_set)):
                return elem

    def monitor(self):
        path_to_watch = "/home/emby/movies/torrents/"
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])

        #TODO print out files currently in folder to make sure I haven't forgotten.

        foundMatch = False
        fileTransferring = True 
        count = 0

        # fileTransferring is false when the file is found, and
        # 4320 is the number of 10 second increments that equals
        # 12 hours, which is as long as I want this script to 
        # wait. After 12 hours that file is probably not coming.
        while (fileTransferring and (count < 4320)):
            print("monitoring")
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
                    payload = {'value1': addedStr}
                    r = requests.post(self.api_endpoint, data=payload)
                    print(r.status_code, r.reason)
                    fileTransferring = False
            if removed: 
                removedStr = "Removed: ", ", ".join (removed)
                payload = {'value1': removedStr}
                r = requests.post(self.api_endpoint, data=payload)
                print(r.status_code, r.reason)
            before = after

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
