
import appdaemon.appapi as appapi

class Octoprint(appapi.AppDaemon):
    on = False
    handle = False
    lamp = ""
    sensor = ""
    
    def initialize(self):
        self.lamp = self.args["lamp"]
        self.sensor = self.args["sensor"]
        print(self.lamp+": controlled by printer "+self.sensor)
        self.listen_state(self.checkstate, self.sensor)
             
    def checkstate(self, entity, attribute, old, new, kwargs):	
        self.printerstate = self.get_state(self.sensor)
        print("/"+self.printerstate+"/")
        if self.printerstate == "Offline":
            self.turn_off(self.lamp)
            self.on = False
            print(self.lamp+": Lamp off")
        else:
            self.turn_on(self.lamp)
            self.on = True
            print(self.lamp+": Lamp on")
            
