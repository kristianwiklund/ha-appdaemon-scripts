#turn on a lamp when a motion on a sensor is detected. keep the lamp on for 10 minutes, then turn it off
# works with mysensors.org sensors, at least

# example appdaemon.yaml snippet:
#kitchenlight:
#  module: motionsensors
#  class: MotionLights
#  lamp: light.koket
#  timeout: 10
#  sensor: binary_sensor.motion_sensor_1_1


import appdaemon.appapi as appapi

class MotionLights(appapi.AppDaemon):
    on = False
    handle = False
    lamp = ""
    sensor = ""
    
    def initialize(self):
        self.lamp = self.args["lamp"]
        self.sensor = self.args["sensor"]
        self.timeout = int(self.args["timeout"])*60
        print(self.lamp+": controlled by sensor "+self.sensor + " timeout :"+str(self.timeout/60)+" minutes")
        self.listen_state(self.motion, self.sensor, new = "on")
            
    def motion(self, entity, attribute, old, new, kwargs):
        print ("tjillevipp " + self.sensor)
        if not self.on:
            # if time of day > 22.00 set brightness to reduced
            self.turn_on(self.lamp)
            self.on = True
            self.log(self.lamp+": On")
        else:
            self.cancel_timer(self.handle)
            
        self.handle = self.run_in(self.light_off, self.timeout)

            
    def light_off(self,kwargs):
        self.turn_off(self.lamp)
        self.on = False
        self.log(self.lamp+": Off")
 

