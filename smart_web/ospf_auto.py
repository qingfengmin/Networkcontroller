import ipaddress
from random import choice
from Configuring_the_database import config, generic, RT_before
from setting_config import config_data as setting
from netconf_session import netconf_auto
from sharing_data import database as db


class ospf_auto:
    def __init__(self,database):
        self.xml_list = []
        self.up_GE_list = []
        self.up_LoopBack_list = []
        self.ns = {'ifm':'http://www.huawei.com/netconf/vrp'}
        self.ip_list = {}
        self.vlan = list(setting().vlan())
        self.loopback_network = list(setting().loopback().keys())
        self.loopback_mask = list(setting().loopback().values())
        self.db = database
        print(self.db.Devices)

    def ospf_interface(self,process,area_id):
        netconf_auto('').get_interfaces()



    
