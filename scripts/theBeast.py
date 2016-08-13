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
#1.Torrent file uploaded to dropbox, IFTTT bot tells vlad:
#       "vlad awaken the beast {{Filename}} has been uploaded to dropbox."
#  theBeast.py tells vlad to remember that {{Filename}} is currently downloading
#  and then it runs on the server waiting for {{Filename}} to appear in the
#  self.path_to_watch_ directory.
#2.
#
#TODO we need logs badly. And maybe a post on the channel if something goes 
#     wrong?
#TODO WORRY ABOUT PEOPLE REQUESTING STUFF THAT ALREADY EXISTS.

class theBeast:
    def __init__(self, m_file, ifttt_api_key, path_to_watch):
        self.subset_tolerance = .5
        self.num_obs_no_delta = 10
        self.time_to_wait = 2160
        self.path_to_watch = path_to_watch
        self.m_file = m_file
        self.max_xfer_wait_count = 180
        self.sleep_time = 20
        self.m_file_as_set = self.stringToSet(m_file)
        self.ifttt_api_key = ifttt_api_key
        self.api_endpoint = "https://maker.ifttt.com/trigger/torrent_ready/with/key/" + self.ifttt_api_key
        self.api_endpoint_talk = "https://maker.ifttt.com/trigger/talk_to_vlad/with/key/" + self.ifttt_api_key
        payload = {'value1': "vlad remem " + "\"" + self.m_file + "\"" + " is downloading"}
        r = requests.post(self.api_endpoint_talk, data=payload)


    # if transferring a show should be tv_shows.....<name_of_show>
    #   -> since all shows just go in same directory and always have
    #      the proper naming convention that problem solves itself.
    #      the issue here is its possible the directory already exists,
    #      and it is also possible the file already exists.

    def moveMusic(self):
        print()
    
    def moveMovie(self):
        print()

    def moveBook(self):
        print()

    def moveTvshow(self):
        print()

    def xferFinished(self, fileName):
        # TODO
        # Decide what type of media this is and then dispatch it to the
        # proper method.
        return fileName

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
        #print("forget downloading cmd: ", r.status_code, r.reason)
        filepath = self.path_to_watch + dir_to_monitor
        #TODO turn 60 and 10 into wait_period and non_changing_threshold
        count = 0
        same_count = 0
        before = self.get_size(filepath)


        #TODO need to verify all paths of this method are traversed
        # this loop is monitoring a file/folder that is either xferring
        # or has xferred. It waits for max_xfer_wait_count * sleep_time
        while (count < self.max_xfer_wait_count):
            #print("before: ", before)
            time.sleep(self.sleep_time)
            after = self.get_size(filepath)
            if before == after:
                same_count = same_count + 1
                if same_count == self.num_obs_no_delta:
                    return True
            else:
                #print("change")
                same_count = 0
            before = after
            count = count + 1


        if count == 60:
            payload = {'value1': "theBeast.py: infinite loop in waitForXfer breakout!"}
            r = requests.post(self.api_endpoint_talk, data=payload)
        return False

# There are a couple steps to monitor() because of the way the servers are
# configured. Torrents are downloaded on a different computer than where
# this script is run. On that computer, I'm using autotools to copy the
# downloaded file to a folder on it's hard drive (~/emby_mount) that is
# connected to the self.path_to_watch folder on ~this~ computer with sshfs.
# so when "foundMatch" becomes True in this script it is because the file
# appeared in the self.path_to_watch folder. However, since it is
# connected with sshfs, it is actually being transferred, that is why
# we have the waitForXfer method that monitors the file size until it
# hasn't changed in a given amount of time. The last step is just to 
# transfer the file where it needs to go which is what the xferFinished
# method is responsible for doing. It looks at the type of torrent and
# dispatches it to the appropriate move method, which just call a bash
# script.
    def monitor(self):
        fileTransferring = True
        foundMatch = False
        count = 0

        before = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
        currLs = [f for f in before]

        foundMatch = self.containsFilename(currLs)
        if foundMatch:
            #print("I got the match, it was already there ", foundMatch)
            fileTransferring = False
            if self.waitForXfer(foundMatch):
                self.xferFinished(foundMatch)

        # fileTransferring is false when the file is found, and
        # 2160 is the number of 10 second increments that equals
        # 6 hours, which is as long as I want this script to
        # wait. After 12 hours that file is probably not coming.

        #print ("monitoring")
        while (fileTransferring and (count < self.time_to_wait)):
            count = count + 1
            time.sleep (10)
            after = dict ([(f, None) for f in os.listdir (self.path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]

            if added:
                foundMatch = self.containsFilename(added)
                if foundMatch:
                    #print("I got the match ", foundMatch)
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
