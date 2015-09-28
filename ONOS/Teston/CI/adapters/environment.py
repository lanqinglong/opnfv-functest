"""
Description:
    This file is used to setup the running environment
     
    lanqinglong@huawei.com
"""

import os
import os.path
import time
import pexpect
import re
import sys
from foundation import foundation

class environment:

    def __init__( self ):
        self.loginfo = foundation( )

    def DownLoadCode( self, codeurl ):
        print "Now loading test codes!Please wait in patient..."
        gitclone = pexpect.spawn ( "git clone " + codeurl )
        index = login.expect ( ['already exists', 'Receiving objects:', \
                                pexpect.EOF] )
        originalfolder = os.getcwd()
        filefolder = originalfolder + '/' + codeurl.split('/')[-1]
        if index == 0 :
            os.chdir( filefolder )
            os.system( 'git pull' )
            os.chdir( originalfolder )
        elif index == 1 :
            self.loginfo.log( 'Download code success!' )
        else :
            self.loginfo.log( 'Download code failed!' )

    def CleanEnv(self):
        print "Now Cleaning test environment"
        os.system("sudo apt-get install -y mininet")
        os.system("OnosSystemTest/TestON/bin/cleanup.sh")
        time.sleep(5)
        self.loginfo.log( 'Clean environment success!' )

    def OnosPushKeys(self, cmd, password):
        print "Now Pushing Onos Keys:"+cmd
        Pushkeys = pexpect.spawn(cmd)
        Result = 0
        while Result != 2:
            Result = Pushkeys.expect( ["yes", "password", pexpect.EOF, \
                                       pexpect.TIMEOUT])
            if ( Result == 0 ):
                Pushkeys.sendline( "yes" )
            if ( Result == 1 ):
                Pushkeys.sendline( password )
            if ( Result == 3 ):
                self.loginfo.log( "ONOS Push keys Error!" )
        print "Done!"

    def SetOnosEnvVar( self, masterpass, agentpass):
        print "Now Setting test environment"
        os.environ["OCT"] = "10.1.0.1"
        os.environ["OC1"] = "10.1.0.50"
        os.environ["OC2"] = "10.1.0.51"
        os.environ["OC3"] = "10.1.0.52"
        os.environ["OCN"] = "10.1.0.53"
        os.environ["OCN2"] = "10.1.0.54"
        os.environ["localhost"] = "10.1.0.1"
        os.system("sudo pip install configobj")
        os.system("sudo apt-get install -y sshpass")
        OnosPushKeys("onos-push-keys 10.1.0.1",masterpass)
        OnosPushKeys("onos-push-keys 10.1.0.50",agentpass)
        OnosPushKeys("onos-push-keys 10.1.0.53",agentpass)
        OnosPushKeys("onos-push-keys 10.1.0.54",agentpass)
    
    def ChangeOnosName( self, user, password):
        print "Now Changing ONOS name&password"
        line = open("onos/tools/build/envDefaults",'r').readlines()
        lenall = len(line)-1
        for i in range(lenall):
           if "ONOS_USER=" in line[i]:
               line[i]=line[i].replace("sdn",user)
           if "ONOS_GROUP" in line[i]:
               line[i]=line[i].replace("sdn",user)
           if "ONOS_PWD" in line[i]:
               line[i]=line[i].replace("rocks",password)
        NewFile = open("onos/tools/build/envDefaults",'w')
        NewFile.writelines(line)
        NewFile.close
        print "Done!"
    
    def ChangeTestCasePara(testcase,user,password):
        print "Now Changing " + testcase +  " name&password"
        filepath = "OnosSystemTest/TestON/tests/" + testcase + "/" + testcase + ".topo"
        line = open(filepath,'r').readlines()
        lenall = len(line)-1
        for i in range(lenall-2):
           if ("localhost" in line[i]) or ("OCT" in line[i]):
               line[i+1]=re.sub(">\w+",">"+user,line[i+1])
               line[i+2]=re.sub(">\w+",">"+password,line[i+2])
           if "OC1" in line [i] \
              or "OC2" in line [i] \
              or "OC3" in line [i] \
              or "OCN" in line [i] \
              or "OCN2" in line[i]:
               line[i+1]=re.sub(">\w+",">root",line[i+1])
               line[i+2]=re.sub(">\w+",">root",line[i+2])
        NewFile = open(filepath,'w')
        NewFile.writelines(line)
        NewFile.close

    def OnosEnvSetup( self ):
        self.DownLoadCode( 'https://github.com/sunyulin/OnosSystemTest.git' )
        self.DownLoadCode( 'https://gerrit.onosproject.org/onos' )
        self.ChangeOnosName(agentusername,agentpassword)
        self.CleanEnv()
        self.SetEnvVar(masterpassword,agentpassword)
