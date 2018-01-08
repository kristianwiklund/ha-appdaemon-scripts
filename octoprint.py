

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
        self.psu = self.args["psu"]        
        self.rgblamp = self.args["rgblamp"]
        self.lamp = self.args["lamp"]
        self.powerbutton = self.args["powerbutton"]
        self.psusensor = self.args["psusensor"]
        print ("octoprint: listening to "+self.powerbutton+" and "+self.psusensor)
        print(self.psu+": controlled by switch "+self.sensor)
        print(self.psu+": controlled by "+self.psusensor)
#        self.listen_state(self.handlelamp, self.sensor)
        self.listen_state(self.handlepsu, self.psusensor)
        self.listen_state(self.poweron, self.powerbutton, new="on")

        
#    def handlelamp(self, entity, attribute, old, new, kwargs):	
#        self.printerstate = self.get_state(self.sensor)
#
#        if self.printerstate == "Offline":
#            if self.on:
#                self.turn_off(self.lamp)
#                self.on = False
#                print(self.lamp+": Lamp off")
#        else:
            #if not self.on:
            #    self.turn_on(self.lamp)
            #    self.on = True
            #    print(self.lamp+": Lamp on")

    def poweron(self, entity, attribute, old, new, kwargs):	
        print("I got the powah!")
        self.turn_off(self.powerbutton)
        if not self.psuon:
            self.turn_on(self.psu)
            self.turn_on(self.lamp)
            self.turn_on(self.rgblamp)
            self.psuon = True
            
    def handlepsu(self, entity, attribute, old, new, kwargs):	
        self.psucommand = self.get_state(self.psusensor)
        print (">"+self.psucommand+"<")
        if self.psucommand == "off":
            self.turn_off(self.psu)
            self.turn_off(self.lamp)
            self.psuon = False
            print(self.psu+": Power off")
        else:
            self.turn_on(self.psu)
            self.turn_on(self.lamp)
            self.psuon = True
            print(self.psu+": Power on")

