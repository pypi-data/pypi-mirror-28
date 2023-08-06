#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import requests
import sys
import logging
import xmltodict

import dateutil.parser


def isNotEmpty(s):
    #small script to check if not empty and not None
    return bool(s and s.strip())  

class storingen():
    """
        class for fetching and parsing NS train failures data
    """
    def __init__(self, usr=None, pwd=None):
        try:
            #set the right NS API URL
            self.url = "http://webservices.ns.nl/ns-api-storingen?station={}&actual={}&unplanned={}"
            
            #Check if username and password are into place and set them
            if isNotEmpty(usr) and isNotEmpty(pwd):
                self.usr = usr
                self.pwd = pwd
            else:
                raise Exception("You must provide a username and password for the API")
    
        except Exception as e:
            msg = "storingen def __init__ : " + str(e)
            logging.error(msg)
        
    
    def goFetch(self, station="", actual=True, unplanned=""):
        """
        Let op: bij unplanned=true worden de geplande werkzaamheden geretourneerd. 
        Dit is dus net andersom dan wat de parameternaam doet vermoeden.
        """
        try:
            #get the data with authentication from NS API
            
            url = self.url.format(station,str(actual).lower(),str(unplanned).lower())
            r = requests.get(url, auth=(self.usr, self.pwd))
            
            if r.status_code != 200:
                    raise Exception("NS Connection failure" + str(r.status_code))
            
            return r.text
    
        except Exception as e:
            msg = "def goFetch : " + str(e)
            logging.warning(msg)

    
    def getData(self, station="", actual=True, unplanned=""):
        try:
            
            #fetch the elements from the NS API
            root = self.goFetch(station, actual, unplanned)
            
            #parse elements into dict
            elements = xmltodict.parse(root, dict_constructor=dict)
            
            if elements['Storingen'] is not None:
                return elements['Storingen'] 
            else:
                return False    
    
    
        except Exception as e:
            msg = "def getData : " + str(e)
            logging.warning(msg)