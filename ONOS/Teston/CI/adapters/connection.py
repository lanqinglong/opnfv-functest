"""
Description:
    This file is used to make connections
    Include ssh & exchange public-key to each other so that 
    it can run without password
    
    lanqinglong@huawei.com
"""
import os
import os.path
import time
import pexpect
import re
import sys
from foundation import foundation 

class connection:

    def __init__( self ):
        self.loginfo = foundation()

    def SSHlogin ( self, ipaddr, username, password ) :
        login = pexpect.spawn ( 'ssh %s@%s' % ( username, ipaddr ) )
        index = 0
        while index != 2 :
            index = login.expect ( ['assword:', 'yes/no', '#|$', \
                                    pexpect.EOF, pexpect.TIMEOUT ] )
            if index == 0 :
                login.sendline( password )
                login.interact( )
            if index == 1 :
                login.sendline( 'yes' )
            if index == 3 :
                self.loginfo.log( 'Ssh return EOF,see screen information:' )
                self.loginfo.log( 'Info before:' + login.before )
                self.loginfo.log( 'Info after' + login.after )
            if index == 4 :
                self.loginfo.log( 'SSH timeout, please check the connection' )
        print ("SSH login " + ipaddr + " success!")

    def AddKnownHost( self, ipaddr, username, password ):
        print( "Now Adding an user to known hosts " + ipaddr )
        login = pexpect.spawn( "ssh -l %s -p 8101 %s"%( username, ipaddr ) )
        index = 0
        while index != 2:
            index = login.expect( ['assword:', 'yes/no', pexpect.EOF, \
                                   pexpect.TIMEOUT] )
            if index == 0:
                login.sendline( password )
                login.sendline( "logout" )
                index = login.expect( ["closed", pexpect.EOF] )
                if index == 0:
                    self.loginfo.log( "Add SSH Known Host Success!" )
                else:
                    self.loginfo.log( "Add SSH Known Host Failed! Please Check!" )
                login.interact()
            if index == 1:
                login.sendline('yes')

    def Gensshkey(self):
        print "Now Generating SSH keys..."
        os.system("rm -rf ~/.ssh/*")
        keysub = pexpect.spawn("ssh-keygen -t rsa")
        Result = 0
        while Result != 2:
            Result = keysub.expect( ["Overwrite", "Enter", pexpect.EOF, \
                                     pexpect.TIMEOUT])
            if Result == 0:
                keysub.sendline("y")
            if Result == 1:
                keysub.sendline("\n")
            if Result == 3:
                self.loginfo.log("Generate SSH key failed.")
        self.loginfo.log( "Generate SSH key success." )

    def GetRootAuth( self, password ):
        print( "Now changing to user root" )
        login = pexpect.spawn( "su - root" )
        index = 0
        while index != 2:
            index = login.expect( ['assword:', "failure", \
                                   pexpect.EOF, pexpect.TIMEOUT] )
            if index == 0:
                login.sendline( password )
            if index == 1:
                self.loginfo.log("Change user to root failed.")
        login.interact()

    def ReleaseRootAuth( self ):
        print( "Now Release user root" )
        login = pexpect.spawn( "exit" )
        index = login.expect( ['logout', \
                                pexpect.EOF, pexpect.TIMEOUT] )
        if index == 0:
            self.loginfo.log("Release root user success.")
        if index == 1:
            self.loginfo.log("Release root user failed.")
        login.interact()

    def AddEnvIntoBashrc( self, envalue ):
        print "Now Adding bash environment"
        os.system( "chmod a+r /etc/profile" )
        fileopen = open( "/etc/profile", 'r' )
        findContext = 1
        while findContext:
            findContext = fileopen.readline( )
            result = findContext.find( envalue )
            if result != -1:
                break
        fileopen.close
        if result == -1:
            envAdd = open( "/etc/profile", 'a+' )
            envAdd.writelines( "\n" + envalue )
            envAdd.close( )
        self.loginfo.log( "Add env to bashrc success!" )

    def OnosConnectionSet (self):
        self.GetRootAuth("root")
        self.Gensshkey()
        self.AddKarafUser("189.42.8.101","karaf","karaf")
        self.AddEnvIntoBashrc("source onos/tools/dev/bash_profile")
        self.ReleaseRootAuth()