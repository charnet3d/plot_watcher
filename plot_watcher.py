"""Working example of the ReadDirectoryChanges API which will
 track changes made to a directory. Can either be run from a
 command-line, with a comma-separated list of paths to watch,
 or used as a module, either via the watch_path generator or
 via the Watcher threads, one thread per path.

Examples:
  watch_directory.py c:/temp,r:/images

or:
  import watch_directory
  for file_type, filename, action in watch_directory.watch_path ("c:/temp"):
    print filename, action

or:
  import watch_directory
  import Queue
  file_changes = Queue.Queue ()
  for pathname in ["c:/temp", "r:/goldent/temp"]:
    watch_directory.Watcher (pathname, file_changes)

  while 1:
    file_type, filename, action = file_changes.get ()
    print file_type, filename, action
    
(c) Tim Golden - mail at timgolden.me.uk 5th June 2009
Licensed under the (GPL-compatible) MIT License:
http://www.opensource.org/licenses/mit-license.php
"""
from __future__ import generators
import os
import sys
import queue
import threading
import time
import glob

import win32file
import win32con

ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed to something",
  5 : "Renamed from something"
}

def watch_path (path_to_watch, include_subdirectories=False):
  FILE_LIST_DIRECTORY = 0x0001
  hDir = win32file.CreateFile (
    path_to_watch,
    FILE_LIST_DIRECTORY,
    win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
    None,
    win32con.OPEN_EXISTING,
    win32con.FILE_FLAG_BACKUP_SEMANTICS,
    None
  )
  while 1:
    results = win32file.ReadDirectoryChangesW (
      hDir,
      1024,
      include_subdirectories,
      win32con.FILE_NOTIFY_CHANGE_FILE_NAME | 
       win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
       win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
       win32con.FILE_NOTIFY_CHANGE_SIZE |
       win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
       win32con.FILE_NOTIFY_CHANGE_SECURITY,
      None,
      None
    )
    for action, file in results:
      full_filename = os.path.join (path_to_watch, file)
      if not os.path.exists (full_filename):
        file_type = "<deleted>"
      elif os.path.isdir (full_filename):
        file_type = 'folder'
      else:
        file_type = 'file'
      yield (file_type, full_filename, ACTIONS.get (action, "Unknown"))

class Watcher (threading.Thread):

  def __init__ (self, path_to_watch, results_queue, **kwds):
    threading.Thread.__init__ (self, **kwds)
    self.setDaemon (1)
    self.path_to_watch = path_to_watch
    self.results_queue = results_queue
    self.start ()

  def run (self):
    for result in watch_path (self.path_to_watch):
      self.results_queue.put (result)

if __name__ == '__main__':
  """If run from the command line, use the thread-based
   routine to watch the current directory (default) or
   a list of directories specified on the command-line
   separated by commas, eg

   watch_directory.py c:/temp,c:/
  """
  PATH_TO_WATCH = ["."]
  #PATH_TO_WATCH = "D:/chia/Portable_Plots", "H:/Portable_Plots", "I:/Portable_Plots", "J:/Portable_Plots", "K:/Portable_Plots", "L:/Portable_Plots"
  try: path_to_watch = sys.argv[1].split (",") or PATH_TO_WATCH
  except: path_to_watch = PATH_TO_WATCH
  path_to_watch = [os.path.abspath (p) for p in path_to_watch]

  print("Watching %s at %s" % (", ".join (path_to_watch), time.asctime ()))
  files_changed = queue.Queue ()
  
  for p in path_to_watch:
    Watcher (p, files_changed)

  while 1:
    try:
      file_type, filename, action = files_changed.get_nowait ()
      ext = os.path.splitext(filename)[1]
      if (action == "Created" or "Renamed from" in action) and ext == ".plot":
        print("%s %s %s" % (file_type, filename, action))
        oldPlotDir = os.path.abspath(os.path.join(os.path.dirname(filename), "..", "Plots"))
        oldPlots = glob.glob(os.path.join(oldPlotDir, "*.plot"))
        if len(oldPlots) > 0:
          print("Removing {}".format(oldPlots[0]))
          #os.remove(oldPlots[0])
        time.sleep (1)
    except queue.Empty:
      time.sleep (1)
      pass
