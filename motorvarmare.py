import appdaemon.appapi as appapi

from dateutil import parser
import datetime
import time

# this uses the google calendar component
# assumption is that the calendar is called "calendar.motorvarmare" (could be set in a parameter, but that is for later...)



class Motorvarmare(appapi.AppDaemon):
    
    def updatetimers(self, state):
        #print(state)
        #print(state.keys())

        attrib = state["attributes"]
        deadline = parser.parse(attrib["start_time"])
        #print(deadline)
        self.starttime = deadline - datetime.timedelta(minutes=120)
        print("motorvärmare: setting timer to "+str(self.starttime))
        self.stoptime = deadline + datetime.timedelta(minutes=30)
        
        if self.handlestart:
            self.cancel_timer(self.handlestart)
            
        if self.handlestop:
            self.cancel_timer(self.handlestop)
            
        self.handlestart = self.run_at(self.turnon, self.starttime)
        self.handlestop = self.run_at(self.turnoff, self.stoptime)

    def turnon(self, kwargs):
        self.turn_on("switch.motorvarmare")
        self.handlestart = False

    def turnoff(self, kwargs):
        self.turn_off("switch.motorvarmare")
        self.handlestop = False
    
            
    def initialize(self):
        self.handlestart = False
        self.handlestop = False        

        
        self.sensor = "calendar.motorvarmare"
        self.listen_state(self.checkstate, self.sensor)
        state = self.get_state(self.sensor, attribute = "all")
        self.updatetimers(state)
        
    def checkstate(self, entity, attribute, old, new, kwargs):
        state = self.get_state(self.sensor, attribute = "all")
        self.updatetimers(state)


            
    
