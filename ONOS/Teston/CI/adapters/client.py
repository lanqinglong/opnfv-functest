"""
Description:
    This file is used to run testcase 
    lanqinglong@huawei.com
"""
from connection import connection 
from environment import environment

class client( foundation, environment ):

    def __init__( self ):
        self.loginfo = foundation()

    def RunScript( self, testname, masterusername, masterpassword ):
        ChangeTestCasePara( testname, masterusername, masterpassword )
        runtest = "OnosSystemTest/TestON/bin/cli.py run " + testname
        os.system(runtest)
        print "Done!"

    def onosbasic(self):
        #This is the compass run machine user&pass,you need to modify
        masterusername = "root"
        masterpassword = "root"
    
        #The config below you don't need to care
        agentusername = "root"
        agentpassword = "root"
    
        print "Test Begin....."
        self.OnosConnectionSet()
        self.SSHlogin("189.42.8.101 ",masterusername,masterpassword)
        self.OnosEnvSetup()
         