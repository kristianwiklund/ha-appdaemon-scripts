
import appdaemon.appapi as appapi

class Octoprint(appapi.AppDaemon):
    on = False
    psuon = False
    handle = False
    lamp = ""
    psu = ""
    sensor = ""
    psusensor = ""
    
    def initialize(self):
        self.lamp = self.args["lamp"]
        self.psu = self.args["psu"]        
        self.sensor = self.args["sensor"]
        self.psusensor = self.args["psusensor"]
        print(self.lamp+": controlled by printer "+self.sensor)
        print(self.psu+": controlled by "+self.psusensor)
        self.listen_state(self.handlelamp, self.sensor)
        self.listen_state(self.handlepsu, self.psusensor)
        
    def handlelamp(self, entity, attribute, old, new, kwargs):	
        self.printerstate = self.get_state(self.sensor)

        if self.printerstate == "Offline":
            if self.on:
                self.turn_off(self.lamp)
                self.on = False
                print(self.lamp+": Lamp off")
        else:
            if not self.on:
                self.turn_on(self.lamp)
                self.on = True
                print(self.lamp+": Lamp on")


    def handlepsu(self, entity, attribute, old, new, kwargs):	
        self.psucommand = self.get_state(self.psusensor)
        print (">"+self.psucommand+"<")
        if self.psucommand == "off":
            self.turn_off(self.psu)
            self.psuon = False
            print(self.psu+": Power off")
        else:
            self.turn_on(self.psu)
            self.psuon = True
            print(self.psu+": Power on")

