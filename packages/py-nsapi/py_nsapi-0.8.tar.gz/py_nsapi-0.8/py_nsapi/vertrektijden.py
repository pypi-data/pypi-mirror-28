#!/usr/bin/python
# -*- encoding: utf-8 -*-
import requests
import sys
import logging
import xmltodict


def isNotEmpty(s):
    #small script to check if not empty and not None
    return bool(s and s.strip())    
        
class vertrektijden():
    """
        class for fetching and parsing NS train failures data
    """
    def __init__(self, usr=None, pwd=None):
        try:
            #set the right NS API URL
            self.url = "https://webservices.ns.nl/ns-api-avt?station={}"
            
            #Check if username and password are into place and set them
            if isNotEmpty(usr) and isNotEmpty(pwd):
                self.usr = usr
                self.pwd = pwd
            else:
                raise Exception("You must provide a username and password for the API")
    
        except Exception as e:
            msg = "vertrektijden def __init__ : " + str(e)
            logging.error(msg)
        
    
    def goFetch(self, station=None):
        """
        Let op: bij unplanned=true worden de geplande werkzaamheden geretourneerd. 
        Dit is dus net andersom dan wat de parameternaam doet vermoeden.
        """
        try:
            #get the data with authentication from NS API
            
            url = self.url.format(station)

            r = requests.get(url, auth=(self.usr, self.pwd))
        
            if r.status_code != 200:
                    raise Exception("NS Connection failure" + str(r.status_code))
            
            return r.text
 
        
        except Exception as e:
            msg = "def goFetch : " + str(e)
            logging.warning(msg)

    
    def getData(self, station=None):
        try:
            if isNotEmpty(station):
                #fetch the elements from the NS API
                root = self.goFetch(station)
            
                #parse elements into dict
                elements =  xmltodict.parse(root, dict_constructor=dict)
                
                if elements['ActueleVertrekTijden'] is not None:
                    return elements['ActueleVertrekTijden'] 
                else:
                    return False
                
            else:
                raise Exception("You should use a station")
      
        except Exception as e:
            msg = "def getData : " + str(e)
            logging.warning(msg)