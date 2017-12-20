import appdaemon.appapi as appapi

from dateutil import parser
import datetime
import time

# this uses the google calendar component

# how to config
#motorvarmare:
#    module: motorvarmare
#    class: Motorvarmare
#    calendar: calendar.motorvarmare
#    offset: 120
#    switch: switch.motorvarmare
    
# bug: if the calendar is changed to make the start time be before the current wall clock time, it fails
# need to add code to start the heater in that case instead of setting a timer to start the heater

class Motorvarmare(appapi.AppDaemon):
    
    def updatetimers(self, state):
        #print(state)
        #print(state.keys())

        attrib = state["attributes"]
        deadline = parser.parse(attrib["start_time"])
        #print(deadline)
        self.starttime = deadline - datetime.timedelta(minutes=self.offset)
        print("motorvärmare: setting timer to "+str(self.starttime))
        self.stoptime = deadline + datetime.timedelta(minutes=30)

        
        if self.handlestart:
            self.cancel_timer(self.handlestart)
            
#        if self.handlestop:
#            self.cancel_timer(self.handlestop)
#            self.turn_off(self.switch)
            
        self.handlestart = self.run_at(self.turnon, self.starttime)


    def turnon(self, kwargs):
        self.turn_on(self.switch)
        self.handlestart = False
        self.handlestop = self.run_at(self.turnoff, self.stoptime)

    def turnoff(self, kwargs):
        self.turn_off(self.switch)
        self.handlestop = False
    
            
    def initialize(self):
        self.handlestart = False
        self.handlestop = False        

        self.offset = self.args["offset"]
        self.sensor = self.args["calendar"]
        self.switch = self.args["switch"]
        
        # self.sensor = "calendar.motorvarmare"
        self.listen_state(self.checkstate, self.sensor)
        state = self.get_state(self.sensor, attribute = "all")
        self.updatetimers(state)
        
    def checkstate(self, entity, attribute, old, new, kwargs):
        state = self.get_state(self.sensor, attribute = "all")
        self.updatetimers(state)


            
    
