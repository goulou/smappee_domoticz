'''
Created on Nov 5, 2016

@author: goulou
'''
import requests
import json
import pprint
import sched

from domoticz import Domoticz
import datetime
import time
import threading
import traceback

UPDATE_DELAY_SECONDS = 3

class EnergyCounter(Domoticz):
    '''
    classdocs
    '''


    def __init__(self, counter, idx, ip="127.0.0.1", port=8080):
        super(EnergyCounter, self).__init__(idx, ip, port)
        
        self.counter = counter
        self.list_variables()
        self.get_values()
#         self.create_variable_if_absent("EnergyCounter_", vartype, value)
    
    def start_update_thread(self):
        threading.Timer(UPDATE_DELAY_SECONDS, self.send_counter_value).start()
    
    def send_counter_value(self):
        threading.Timer(UPDATE_DELAY_SECONDS, self.send_counter_value).start()
        self.send_electricity_command(self.counter.get_power(), self.counter.get_energy())
        
    def send_electricity_command(self, power, energy):
        self.send_device_command("param=udevice&idx=%d&nvalue=0&svalue=%d;%d" % (self.idx, power, energy))
    
    def get_values(self):
        try:
            last_values = self.send_device_request("rid=%d" % self.idx)
            pprint.pprint(last_values)
            last_update_time = datetime.datetime.strptime(last_values["LastUpdate"], "%Y-%m-%d %H:%M:%S")
            last_power_value = float(last_values["Usage"].split()[0])
            last_energy_value = float(last_values["Data"].split()[0]) * 1000
            print("Setting initial values from domoticz to %r, %d, %f" % (last_update_time, last_power_value, last_energy_value))
            self.counter.set_initial_values(last_update_time, last_power_value, last_energy_value)
        except:
            traceback.print_exc()
            print("Encountered an error, setting counter to empty values")
            self.counter.set_initial_values(None, None, 0)