from Configuring_the_database import config, generic, RT_before
from setting_config import config_data as setting
from random import choice as cho

class vxlan_auto:
    def __init__(self,sharing_data):
        self.xml_list = []
        self.bd_list = list(setting().BD())
        self.vni_list = list(setting().vni())

    def bgp(self,as_number):
        neighbors = config().bgp_neighbor(as_number,)

    def vxlan(self,bd,vni):
        vxlan_tunnel = config().vxlan_BD(bd,vni)
