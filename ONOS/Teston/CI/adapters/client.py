"""
Description:
    This file is used to run testcase 
    lanqinglong@huawei.com
"""
from environment import environment

class client( environment ):

    def __init__( self ):
        environment.__init__( self )
        self.loginfo = environment()

    def RunScript( self, testname, masterusername, masterpassword ):
        """
        Run ONOS Test Script
        Parameters:
        testname: ONOS Testcase Name
        masterusername: The server username of running ONOS
        masterpassword: The server password of running ONOS
        """
        self.ChangeTestCasePara( testname, masterusername, masterpassword )
        runtest = "OnosSystemTest/TestON/bin/cli.py run " + testname
        os.system(runtest)
        print "Done!"

    def onosbasic(self):
        #This is the compass run machine user&pass,you need to modify
        self.masterusername = "root"
        self.masterpassword = "root"
        self.agentusername = "root"
        self.agentpassword = "root"
        self.OCT = '189.42.8.99'
        self.OC1 = '189.42.8.101'
        self.OC2 = '189.42.8.102'
        self.OC3 = '189.42.8.103'
        self.OCN = '189.42.8.104'
        self.OCN2 = '189.42.8.105'
        self.localhost = self.OCT

        print "Test Begin....."
        self.OnosConnectionSet()
        masterhandle = self.SSHlogin(self.localhost,self.masterusername,self.masterpassword)
        self.OnosEnvSetup( masterhandle )
        self.SSHRelease( masterhandle )