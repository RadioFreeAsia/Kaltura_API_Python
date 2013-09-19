import os, sys, inspect
import unittest

from KalturaClient import KalturaClient
from KalturaClientBase import KalturaConfiguration
from KalturaCoreClient import KalturaSessionType
from KalturaClientBase import KalturaObjectFactory, KalturaEnumsFactory
from KalturaCoreClient import KalturaMediaType

from secret_config import PARTNER_ID, SERVICE_URL, SECRET, ADMIN_SECRET, USER_NAME

import logging
logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(levelname)s %(message)s',

                    stream = sys.stdout)


from KalturaClientBase import IKalturaLogger
class KalturaLogger(IKalturaLogger):
    def log(self, msg):
        logging.info(msg)

def GetConfig():
    config = KalturaConfiguration(PARTNER_ID)
    config.serviceUrl = SERVICE_URL
    config.setLogger(KalturaLogger())
    return config

def getTestFile(filename, mode='rb'):
    testFileDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    return file(testFileDir+'/'+filename, mode)
    
    

class KalturaBaseTest(unittest.TestCase):
    """Base class for all Kaltura Tests"""
    #TODO  create a client factory as to avoid thrashing kaltura with logins...
    
    def setUp(self):
        #(client session is enough when we do operations in a users scope)
        self.config = GetConfig()
        self.client = KalturaClient(self.config)
        self.ks = self.client.generateSession(ADMIN_SECRET, USER_NAME, 
                                             KalturaSessionType.ADMIN, PARTNER_ID, 
                                             86400, "")
        self.client.setKs(self.ks)            
            
            
    def tearDown(self):        
        self.config = None
        self.client = None
        self.ks = None    