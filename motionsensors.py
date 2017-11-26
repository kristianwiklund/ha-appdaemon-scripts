
import appdaemon.appapi as appapi

class MotionLights(appapi.AppDaemon):
    on = False
    handle = False
    lamp = ""
    sensor = ""
    
    def initialize(self):
        self.lamp = self.args["lamp"]
        self.sensor = self.args["sensor"]
        print(self.lamp+": controlled by sensor "+self.sensor)
        self.listen_state(self.motion, self.sensor, new = "on")
            
    def motion(self, entity, attribute, old, new, kwargs):
        if not self.on:
            self.turn_on(self.lamp)
            self.on = True
#            self.log(self.lamp+": On")
        else:
            self.cancel_timer(self.handle)
            
        self.handle = self.run_in(self.light_off, 600)

            
    def light_off(self,kwargs):
        self.turn_off(self.lamp)
        self.on = False
#        self.log(self.lamp+": Off")


