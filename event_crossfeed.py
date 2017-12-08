import appdaemon.appapi as appapi

from dateutil import parser
import datetime
import time
import json


class Crossfeed(appapi.AppDaemon):
    # set up listeners to all "sensors" in the sensors dictionary

    def initialize(self):
    
        self.sensors = {'sensor.temperature_sensor_4_0':'home/temperature/pilsnerkranarna',
                        'sensor.utomhus_temperature':'home/temperature/utomhus',
                        'sensor.inomhusuppe_temperature':'home/temperature/inomhusuppe',
                        'sensor.kabelsensor_temperature':'home/temperature/kabelsensor',
                        'sensor.lime_temperature':'home/temperature/lime',
                        'sensor.chili_temperature':'home/temperature/chili',
                        'sensor.kaminen_temperature':'home/temperature/kaminen',
                        'binary_sensor.motion_sensor_1_1':'home/motion/koket',
                        'binary_sensor.motion_sensor_2_2':'home/motion/hall_uppe',
                        'binary_sensor.motion_sensor_3_3':'home/motion/hall_nere'
        }
    
        for key in self.sensors:
            self.listen_state(self.pubstate, key)


    def pubstate(self, entity, attribute, old, new, kwargs):	
#        print ("sending mqtt crossfeed for "+entity)
        t = {"value":self.get_state(entity), "timestamp":time.time(), "date":time.strftime("%Y-%m-%d"), "time":time.strftime("%H:%M")}
#        print(t)
        
        self.call_service("mqtt/publish",topic=self.sensors[entity], payload=json.dumps(t,separators=(',', ':')), retain=1)
