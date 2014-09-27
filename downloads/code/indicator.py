#!/usr/bin/env python3

import sys
import urllib.request
import hashlib
import lxml.html
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib

class MyIndicator:
  def __init__(self):
    self.hash = ''
    self.ind = appindicator.Indicator.new(
                "Test",
                "indicator-messages",
                appindicator.IndicatorCategory.APPLICATION_STATUS)
    self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
    self.ind.set_attention_icon("new-messages-red")
    self.menu = Gtk.Menu()

    item = Gtk.MenuItem()
    item.set_label("Clear")
    item.connect("activate", self.clear)
    self.menu.append(item)

    item = Gtk.MenuItem()
    item.set_label("Exit")
    item.connect("activate", self.quit)
    self.menu.append(item)

    self.menu.show_all()
    self.ind.set_menu(self.menu)

  def main(self):
    self.check_site()
    GLib.timeout_add_seconds(60, self.check_site)
    Gtk.main()

  def clear(self, widget):
    self.hash = self.remote_hash
    self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

  def check_site(self):
    remote_data = urllib.request.urlopen('http://habrahabr.ru').read()
    self.remote_hash = hashlib.md5(remote_data).hexdigest()
    if self.hash == '':
      self.hash = self.remote_hash
      print("======INITIAL======")
      print(self.remote_hash)
    else:
      print("======TRIGGERED=======");
      print("Local hash: " + self.hash)
      print("Remote hash: " + self.remote_hash)
      if self.hash != self.remote_hash:
        print("======ATTENTION=======");
        self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)
    return True

  def quit(self, widget):
    Gtk.main_quit()

if __name__ == '__main__':
  indicator = MyIndicator();
  indicator.main();
