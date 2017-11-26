#short script to turn on a specified lamp. Made it as a quick and dirty hack
#to be able to remotely turn something on without exposing a web page
import appdaemon.appapi as appapi

from dateutil import parser
import datetime
import time
 
class Turnon(appapi.AppDaemon):

    def initialize(self):
        self.lamp = self.args["lamp"]
        self.turn_on(self.lamp)

