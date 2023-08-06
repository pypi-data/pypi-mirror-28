#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import requests
import sys
import logging
import xmltodict

def isNotEmpty(s):
    #small script to check if not empty and not None
    return bool(s and s.strip())    

class reisadviezen():
    """
        class for fetching and parsing NS train reis advies data
    """
    def __init__(self, usr=None, pwd=None):
        try:
            #set the right NS API URL
            self.url = "http://webservices.ns.nl/ns-api-treinplanner?fromStation={}&toStation={}&viaStation={}&previousAdvices={}&nextAdvices={}&dateTime={}&Departure={}&hslAllowed={}&yearCArd={}"
            
            #Check if username and password are into place and set them
            if isNotEmpty(usr) and isNotEmpty(pwd):
                self.usr = usr
                self.pwd = pwd
            else:
                raise Exception("You must provide a username and password for the API")
    
        except Exception as e:
            msg = "storingen def __init__ : " + str(e)
            logging.error(msg)
        
    
    def goFetch(self, fromStation=None, toStation=None, viaStation="", previousAdvices=2,nextAdvices=3,dateTime="",Departure="true",hslAllowed="true",yearCArd="false"):
        """
        Let op: bij unplanned=true worden de geplande werkzaamheden geretourneerd. 
        Dit is dus net andersom dan wat de parameternaam doet vermoeden.
        """
        try:
            #get the data with authentication from NS API
            url = self.url.format(fromStation,toStation,viaStation,previousAdvices,nextAdvices,dateTime,str(Departure).lower(),str(hslAllowed).lower(),str(yearCArd).lower())
            r = requests.get(url, auth=(self.usr, self.pwd))
            
            if r.status_code != 200:
                    raise Exception("NS Connection failure" + str(r.status_code))
            
            return r.text
    
        except Exception as e:
            msg = "def goFetch : " + str(e)
            logging.warning(msg)

    
    def getData(self, fromStation=None, toStation=None, viaStation="", previousAdvices=2,nextAdvices=3,dateTime="",Departure="true",hslAllowed="true",yearCArd="false"):
        try:
            
            if fromStation is None or toStation is None:
                raise Exception("You have to put in a From Station and To Station")
            
            #fetch the elements from the NS API
            root = self.goFetch(fromStation, toStation, viaStation, previousAdvices,nextAdvices,dateTime,Departure,hslAllowed,yearCArd)
            
            #parse elements into dict
            elements = xmltodict.parse(root, dict_constructor=dict)
            
            if elements['ReisMogelijkheden'] is not None:
                return elements['ReisMogelijkheden'] 
            else:
                return False
            
        except Exception as e:
            msg = "def getData : " + str(e)
            logging.warning(msg)