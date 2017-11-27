import appdaemon.appapi as appapi

from dateutil import parser
import datetime
import time



class Crossfeed(appapi.AppDaemon):
    # set up listeners to all "sensors" in the sensors dictionary

    def initialize(self):
    
        self.sensors = {'sensor.temperature_sensor_4_0':'home/temperature/pilsnerkranarna'}
    
        for key in self.sensors:
            self.listen_state(self.pubstate, key)


    def pubstate(self, entity, attribute, old, new, kwargs):	
        print ("sending mqtt crossfeed for "+entity)
        t = float(self.get_state(entity))

        self.call_service("mqtt/publish",topic=self.sensors[entity], payload=t)
