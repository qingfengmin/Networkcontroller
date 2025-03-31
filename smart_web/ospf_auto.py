import ipaddress
from random import choice
from Configuring_the_database import config as con
from setting_config import config_data as setting
from netconf_session import netconf_auto as ncs
from sharing_data import database as db


class ospf_auto:
    def __init__(self,database):
        self.xml_list = []
        self.ns = {'ifm':'http://www.huawei.com/netconf/vrp'}
        self.ip_list = {}
        self.vlan = list(setting().vlan())
        self.loopback_network = list(setting().loopback().keys())
        self.loopback_mask = list(setting().loopback().values())
        self.db = database
        self.device = self.db.Devices
        self.con = con()

        # print(self.db.Devices)

    def ospf_process(self,process_id,area_id):
        device_list = self.db.Devices.keys()
        for i in device_list:
            router_id = self.db.Devices[i]['loopback_ip']
            niuwenjun = self.con.ospf_Process(process_id,router_id,area_id)
            res = ncs(i).dly_key(niuwenjun)
            print(res)

    def ospf_interface(self,process,area_id):





    
