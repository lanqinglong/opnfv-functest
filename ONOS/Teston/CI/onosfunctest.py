"""
Description: This test is to run onos Teston VTN scripts

List of test cases:
CASE1 - Northbound NBI test network/subnet/ports
CASE2 - Ovsdb test&Default configuration&Vm go online

lanqinglong@huawei.com
"""
from adapters.client import client 

if __name__=="__main__":
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
    
    main = client()
    main.onosbasic()
    main.RunScript("FUNCvirNetNB",self.masterusername,self.masterpassword)
    main.RunScript("FUNCovsdbtest",self.masterusername,self.masterpassword)
