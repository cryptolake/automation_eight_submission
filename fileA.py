#!/usr/bin/python3
"""Monitors for changes to to the file."""

import os
import sys
import time
from sys import argv
import json
from multiprocessing.connection import Client


class Watcher():
    """
    Class to Watch a file.

    Functionality to watch changes in a file
    and perform actions when needed.
    """

    running = True
    refresh_delay_secs = 1

    def __init__(self, watch_file, call_func_on_change=None, *args, **kwargs):
        """Initialize Watcher class."""
        self._cached_stamp = 0
        self.filename = watch_file
        self.call_func_on_change = call_func_on_change
        self.args = args
        self.kwargs = kwargs

    # Look for changes
    def look(self):
        """Look for changes in file."""
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            # File has changed, so do something...
            print('File changed')
            if self.call_func_on_change is not None:
                self.call_func_on_change(*self.args, **self.kwargs)

    # Keep watching in a loop
    def watch(self):
        """Perform action when file changed."""
        while self.running:
            try:
                # Look for changes
                time.sleep(self.refresh_delay_secs)
                self.look()
            except KeyboardInterrupt:
                print('\nDone')
                break
            except FileNotFoundError:
                # Action on file not found
                pass
            except Exception:
                print('Unhandled error: %s' % sys.exc_info()[0])


# Call this function each time a change happens
def json_send(file, client):
    """Send file changes to fileb."""
    with open(file) as f:
        aps = json.load(f)
        client.send(aps["access_points"])


watch_file = argv[1]

address = ('localhost', 6000)
client = Client(address, authkey=b'password')

# watcher = Watcher(watch_file)  # simple
watcher = Watcher(watch_file, json_send, file=watch_file, client=client)
watcher.watch()  # start the watch going
client.close()
