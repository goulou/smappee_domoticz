'''
Created on Nov 6, 2016

@author: goulou
'''
import datetime

class EnergyCounter(object):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.initial_values_set = False
        self.last_update_time = None
        self.last_power_value = None
        self.last_energy_value = None
    
    def set_initial_values(self, last_update_time, last_power_value, last_energy_value):
        self.last_update_time = last_update_time
        self.last_power_value = last_power_value
        self.last_energy_value = last_energy_value
        self.initial_values_set = True
        
    def set_current_value(self, power):
        update_time = datetime.datetime.now()

        if self.initial_values_set is False:
            self.last_update_time= update_time
            self.last_power_value = power
            return
        
        if self.last_update_time is not None:
            delta_time = (update_time - self.last_update_time).total_seconds()
            delta_energy = (((power + self.last_power_value)/2) * delta_time) / 3600
            self.last_energy_value += delta_energy
            print("[%s] in %f seconds, got %f Wh out of %f W : total energy is %f Wh" % (self.name, delta_time, delta_energy, power, self.last_energy_value))
        
        self.last_update_time= update_time
        self.last_power_value = power
    
    def get_power(self):
        return self.last_power_value

    def get_energy(self):
        return self.last_energy_value