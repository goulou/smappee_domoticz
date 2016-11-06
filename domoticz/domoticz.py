'''
Created on Nov 5, 2016

@author: goulou
'''
import requests
import json
import pprint
import time

HTTP_HEADERS = { 'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest' }

USER_VARIABLE_TYPE_INTEGER = 0
USER_VARIABLE_TYPE_FLOAT = 1
USER_VARIABLE_TYPE_STRING = 2
USER_VARIABLE_TYPE_DATE = 3
USER_VARIABLE_TYPE_TIME = 4

class Domoticz(object):
    '''
    classdocs
    '''


    def __init__(self, idx, ip="127.0.0.1", port=8080):
        '''
        Constructor
        '''
        self.url = "http://%s:%d/json.htm" % (ip, port)
        self.idx = idx
        self.session = requests.Session()
    
    def send_request(self, request):
        url = self.url + "?" + request
        print("requesting %s" % url)
        start = time.time()
        response = self.session.get(url, headers=HTTP_HEADERS)
        print("request took %f seconds" % (time.time()-start))
        return response.json()
        
    def send_command(self, command):
        return self.send_request("type=command&%s" % (command))
    
    def send_device_request(self, command):
        return self.send_request("type=devices&%s" % (command))["result"][0]
    
    def send_device_command(self, command):
        return self.send_command("idx=%d&%s" % (self.idx, command))
    
    def list_variables(self):
        variables = self.send_command("param=getuservariables")
        pprint.pprint(variables)
        varlist = variables["result"]
        varmap = {}
        for variable in varlist:
            varmap[variable["Name"]] = variable
        return varmap
    
    def create_variable_if_absent(self, name, vartype, value=""):
        variables = self.list_variables()
        if variables.has_key(name) is False:
            self.send_command("param=saveuservariable&vname=%s&vtype=%d&vvalue=%s" % (name, vartype, value))
