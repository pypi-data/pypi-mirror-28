import os, inspect, sys

def add_path_rec(path):
  abspath = os.path.abspath(path)
  if os.path.isfile(os.path.join(abspath, '__init__.py')):
    sys.path.insert(0, abspath)
    if os.path.ismount(abspath):
      return
    add_path_rec(os.path.join(abspath, '..'))

start_path = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
add_path_rec(start_path)
