import gconf
import pygtk, gtk, os
pygtk.require('2.0')

class FuzzyOpenConfigWindow:
  def __init__(self):
    self._builder = gtk.Builder()
    self._builder.add_from_file(os.path.join(os.path.dirname( __file__ ), "config.glade"))
    self._window = self._builder.get_object('configwindow')
    self._window.show_all()

