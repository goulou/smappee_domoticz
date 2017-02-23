'''
Created on Nov 5, 2016

@author: goulou
'''
import requests
import json
import pprint
import sched
import time
import threading


HTTP_HEADERS = { 'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest' }

UPDATE_DELAY_SECONDS = 0.5

class Smappee(object):
    '''
    classdocs
    '''


    def __init__(self, ip):
        '''
        Constructor
        '''
        self.ip = ip
        self.url = "http://%s/gateway/apipublic/" % ip
        self.counters = {}
        self.session_reuse_count = 0
        self.session = requests.Session()
        self.last_used_password = ""
        
    def set_counter(self, idx, counter):
        self.counters[idx] = counter
    
    def request(self, path, data):
#         response = requests.post(url, "admin", headers=head)
#         print response.text
        
        url = self.url + path
        print("requesting %s" % url)
        if self.session_reuse_count > 1000:
            self.session_reuse_count = 0
            self.session = requests.Session()
            
        response = self.session.post(url, data, headers=HTTP_HEADERS)
        
        return response.json()

    def login_test(self, password=None):
        if password is None:
            password = self.last_used_password
        else:
            self.last_used_password = password
        val= self.request("logon", password)
        return str(val) != "{u'error': u'Logon failed, wrong portal password!'}"
    
    def retreive_data(self):
        data = self.request("instantaneous", "loadInstantaneous")
#         pprint.pprint(data)
        data_m = {}
        for ar in data:
            data_m[ar["key"]] = ar["value"]
            
            
#         pprint.pprint(data_m)
        for (counter_name, counter) in self.counters.iteritems():
            counter.set_current_value(int(data_m[counter_name])/1000.0)
                
    def start_instantaneous_reader(self):
        threading.Timer(UPDATE_DELAY_SECONDS, self.read_instantaneous_value).start()
    
    def read_instantaneous_value(self):
        threading.Timer(UPDATE_DELAY_SECONDS, self.read_instantaneous_value).start()
        self.retreive_data()

