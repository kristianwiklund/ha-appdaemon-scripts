# simple timer script
# example appdaemon.yaml snippet:
# plantlights:
#   module: timer
#   class: Timer
#   lamp: switch.plantlights
#   lon: "06:00"
#   loff: "22:00"


import appdaemon.appapi as appapi

from dateutil import parser
import datetime
import time
 
class Timer(appapi.AppDaemon):

    def initialize(self):
        self.lamp = self.args["lamp"]

        self.lon = parser.parse(self.args["lon"])
        print(self.args["lon"])
        self.lon = self.lon.time()
        
        self.loff = parser.parse(self.args["loff"])
        print(self.args["loff"])
        self.loff = self.loff.time()

        self.handle_on = self.run_once(self.turnon, self.lon)
        self.handle_off = self.run_once(self.turnoff, self.loff)        

        print("will turn on "+self.lamp+" at "+self.lon.strftime("%H:%M:%S"))
        print("will turn off "+self.lamp+" at "+self.loff.strftime("%H:%M:%S"))        

        timenow = datetime.datetime.now().time()

        if self.lon <= timenow <= self.loff:
            self.log("timer: "+self.lamp+": On")
            self.turn_on(self.lamp)
        else:
            self.log("timer: "+self.lamp+": Off")
            self.turn_off(self.lamp)
        
    def turnon(self, kwargs):
        self.log("timer: "+self.lamp+": On")
        self.turn_on(self.lamp)
        self.handle_on = self.run_once(self.turnon, self.lon)
        
    def turnoff(self, kwargs):
        self.log("timer: "+self.lamp+": Off")
        self.turn_off(self.lamp)
        self.handle_off = self.run_once(self.turnoff, self.loff)        
