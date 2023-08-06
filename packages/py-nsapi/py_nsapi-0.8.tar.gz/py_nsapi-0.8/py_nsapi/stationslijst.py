#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import requests
import logging
import xmltodict

def isNotEmpty(s):
    #small script to check if not empty and not None
    return bool(s and s.strip())    


class stations():
    """
        class for fetching and parsing trainstation data
    """
    def __init__(self, usr=None, pwd=None):
        try:
            #set the right NS API URL
            self.url = "http://webservices.ns.nl/ns-api-stations-v2"
            
            #Check if username and password are into place and set them
            if isNotEmpty(usr) and isNotEmpty(pwd):
                self.usr = usr
                self.pwd = pwd
            else:
                raise Exception("You must provide a username and password for the API")
    
        except Exception as e:
            msg = "stations - def __init__ : " + str(e)
            logging.error(msg)
    
    
    def goFetch(self):
        try:
            #get the data with authentication from NS API
            r = requests.get(self.url, auth=(self.usr, self.pwd))
            
            if r.status_code != 200:
                    raise Exception("NS Connection failure" + str(r.status_code))
            
            return r.text

            # find the right element for parsing xml
            return root.findall('Station')
    
        except Exception as e:
            msg = "def goFetch : " + str(e)
            logging.warning(msg)

    
    def getData(self):
        try:
            #fetch the elements from the NS API
            root = self.goFetch()
            
            #parse elements into dict
            elements = xmltodict.parse(root, dict_constructor=dict)
            
            if elements['Stations'] is not None:
                return elements['Stations'] 
            else:
                return False
            
                
        except Exception as e:
            msg = "def getData : " + str(e)
            logging.warning(msg)