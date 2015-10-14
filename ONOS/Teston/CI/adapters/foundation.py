"""
Description:
    This file include basis functions
    lanqinglong@huawei.com
"""

import logging
import os
import time
import yaml

class foundation:

    def __init__(self):

        currentpath = os.getcwd()
        self.logdir = os.path.join( currentpath, 'log' )
        self.workhome = currentpath[0:currentpath.rfind('testcases')]
        self.Result_DB = ''

    def log (self, loginfo):
        """
        Record log in log directory for deploying test environment
        parameters:
        loginfo(input): record info
        """
        filename = time.strftime( '%Y-%m-%d-%H-%M-%S' ) + '.log'
        filepath = os.path.join( self.logdir, filename )
        logging.basicConfig( level=logging.INFO,
                format = '%(asctime)s %(filename)s:%(message)s',
                datefmt = '%d %b %Y %H:%M:%S',
                filename = filepath,
                filemode = 'w')
        filelog = logging.FileHandler( filepath )
        logging.getLogger( 'Functest' ).addHandler( filelog )
        print loginfo
        logging.info(loginfo)

    def getdefaultpara( self ):
        """
        Get Default Parameters value
        """
        with open(self.workhome + "testcases/config_functest.yaml") as f:
            functest_yaml = yaml.safe_load(f)
        f.close()

        self.Result_DB = functest_yaml.get("results").get("test_db_url")
        self.masterusername = functest_yaml.get("ONOS").get("general").\
                            get('onosbench_username')
        self.masterpassword = functest_yaml.get("ONOS").get("general").get("onosbench_password ")
        self.agentusername = functest_yaml.get("ONOS").get("general").get("onoscli_username")
        self.agentpassword = functest_yaml.get("ONOS").get("general").get("onoscli_password")
        self.runtimeout = functest_yaml.get("ONOS").get("general").get("runtimeout")
        self.OCT = functest_yaml.get("ONOS").get("environment").get("OCT")
        self.OC1 = functest_yaml.get("ONOS").get("environment").get("OC1")
        self.OC2 = functest_yaml.get("ONOS").get("environment").get("OC2")
        self.OC3 = functest_yaml.get("ONOS").get("environment").get("OC3")
        self.OCN = functest_yaml.get("ONOS").get("environment").get("OC4")
        self.OCN2 = functest_yaml.get("ONOS").get("environment").get("OC5")
        self.localhost = self.OCT
        return True