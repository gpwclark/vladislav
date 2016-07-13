#!/usr/bin/python3
import sys
import re
import os
import time
import requests

#https://maker.ifttt.com/trigger/ + {event} + /with/key/ + self.ifttt_api_key
#event = torrent_ready

class theBeast:        
    def __init__(self, m_file, ifttt_api_key):
        self.m_file = m_file
        self.ifttt_api_key = ifttt_api_key
        self.api_endpoint = "https://maker.ifttt.com/trigger/torrent_ready/with/key/" + self.ifttt_api_key

    def monitor(self):
        print(self.m_file)
        print(self.ifttt_api_key)
        path_to_watch = "."
        print("monitoring")
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        while 1:
            time.sleep (10)
            after = dict ([(f, None) for f in os.listdir (path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]
            if added: 
                addedStr = "Added: ", ", ".join (added)
                payload = {'value1': addedStr}
                r = requests.post(self.api_endpoint, data=payload)
                print(r.status_code, r.reason)
            if removed: 
                removedStr = "Removed: ", ", ".join (removed)
                payload = {'value1': removedStr}
                r = requests.post(self.api_endpoint, data=payload)
                print(r.status_code, r.reason)
            before = after

if __name__ == "__main__":
    beast = theBeast(m_file=sys.argv[1],ifttt_api_key=sys.argv[2])
    beast.monitor()
