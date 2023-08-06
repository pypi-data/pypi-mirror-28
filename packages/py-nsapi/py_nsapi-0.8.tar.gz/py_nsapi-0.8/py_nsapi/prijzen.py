#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Voor gebruik van de webservice is aparte autorisatie vereist. 
Deze autorisatie wordt verleend na ontvangst van een getekend contract. 
Dit contract is op te vragen via nsr.api@ns.nl.
"""

import requests
import sys
import logging
import xmltodict

def isNotEmpty(s):
    #small script to check if not empty and not None
    return bool(s and s.strip())    


class prijzen():
    """
        class for fetching and parsing NS train failures data
    """
    def __init__(self, usr=None, pwd=None):
        try:
            #set the right NS API URL
            self.url = "http://webservices.ns.nl/ns-api-prijzen-v3?from={}&to={}&via={}&dateTime={}"
            
            #Check if username and password are into place and set them
            if isNotEmpty(usr) and isNotEmpty(pwd):
                self.usr = usr
                self.pwd = pwd
            else:
                raise Exception("You must provide a username and password for the API")
    
        except Exception as e:
            msg = "prijzen def __init__ : " + str(e)
            logging.error(msg)
    
    
    def goFetch(self, fromST=None, toST=None, viaST="", dateTime=""):
        """
        Let op: bij unplanned=true worden de geplande werkzaamheden geretourneerd. 
        Dit is dus net andersom dan wat de parameternaam doet vermoeden.
        """
        try:
            #get the data with authentication from NS API
            url = self.url.format(fromST,toST,viaST,dateTime)
            
            r = requests.get(url, auth=(self.usr, self.pwd))
            
            if r.status_code != 200:
                    raise Exception("NS Connection failure" + str(r.status_code))
            
            return r.text
    
        except Exception as e:
            msg = "def goFetch : " + str(e)
            logging.warning(msg)

    
    def getData(self, fromST=None, toST=None, viaST="", dateTime=""):
        try:
            if fromST is None or toST is None:
                raise Exception("You must provide a From and To station")    
            
            #fetch the elements from the NS API
            root = self.goFetch(fromST,toST,viaST,dateTime)
            
            return xmltodict.parse(root, dict_constructor=dict)
    
        except Exception as e:
            msg = "def getData : " + str(e)
            logging.warning(msg)   