# a script to run my fireplace fan if the temperature is more than 40 degrees on the shelf

import appdaemon.appapi as appapi

class Kaminflakt(appapi.AppDaemon):

    def initialize(self):
        self.state = "baff"
        self.handle = self.run_in(self.check_temperature, 1)
        self.state = self.get_state("switch.kaminflakten")
        log ("Kaminfläkten is "+str(self.state))

    def check_temperature(self,kwargs):
        self.handle = self.run_in(self.check_temperature,60)
        # sensor.kaminen_temperature

        t = float(self.get_state("sensor.kaminen_temperature"))
        if t>40.0:
            if self.state != "on":
                self.turn_on("switch.kaminflakten")
                self.state = "on"
        else:
            if self.state != "off":
                self.turn_off("switch.kaminflakten")            
                self.state = "off"

        
