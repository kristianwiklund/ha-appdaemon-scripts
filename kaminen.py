# a script to run my fireplace fan if the temperature is more than 40 degrees on the shelf

import appdaemon.appapi as appapi

class Kaminflakt(appapi.AppDaemon):

    def initialize(self):
        self.handle = self.run_in(self.check_temperature, 1)


    def check_temperature(self,kwargs):
        self.handle = self.run_in(self.check_temperature,60)
        # sensor.kaminen_temperature

        t = float(self.get_state("sensor.kaminen_temperature"))
        if t>40.0:
            self.turn_on("switch.kaminflakten")
        else:
            self.turn_off("switch.kaminflakten")            


        
