import os, inspect, sys

class allezup:

  def add_path_rec(self, path):
    abspath = os.path.abspath(path)
    if os.path.isfile(os.path.join(abspath, '__init__.py')):
      if abspath not in sys.path:
        sys.path.append(abspath)
      if os.path.ismount(abspath):
        return
      self.add_path_rec(os.path.join(abspath, '..'))

  def __call__(self):
    start_path = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    self.add_path_rec(start_path)

sys.modules[__name__] = allezup()
