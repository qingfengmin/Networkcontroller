from Configuring_the_database import config as con
from setting_config import config_data as setting
from random import choice as cho
from netconf_session import netconf_auto as ncs
import time

class vxlan_auto:
    def __init__(self,sharing_data):
        self.db = sharing_data
        self.device = self.db.Devices
        self.host = self.db.hostlist
        self.bd_list = list(setting().BD())
        self.vni_list = list(setting().vni())
        self.con = con()

    def bgp_peer(self, as_number):
        for device_ip in self.device:
            config = [
                self.con.bgp(as_number, self.device[device_ip]['loopback_ip'])
            ]
            for peer_ip in self.device[device_ip]['bgppeer'].values():
                config.extend(self.con.bgp_neighbor(peer_ip, as_number, 'LoopBack0'))
            
            for xml_config in config:
                print(ncs(device_ip).dly_key(xml_config))

    def vxlan_tunnel(self, bd=None, vni=None):
        bd = bd or cho(self.bd_list)
        vni = vni or cho(self.vni_list)
        
        for device_ip in self.device:
            configs = [
                self.con.nve_source(self.device[device_ip]['loopback_ip'])
            ]
            configs.extend(self.con.vxlan_BD(bd, vni))

            for xml_config in configs:
                print(ncs(device_ip).dly_key(xml_config))

    def tunnel(self,address,mask,bd_id,RD,import_rt,export_rt):
        configs = []
        for z in self.host.keys():
            if self.host[z] == '核心设备':
                configs.extend(self.con.l3evpn(bd_id, RD, export_rt, import_rt))
                configs.append(self.con.interface_addrsss(f'vbdif{bd_id}',address,mask))
            if self.host[z] == '':
                configs.extend(self.con.l3evpn(bd_id, RD, import_rt, export_rt))
            for xml in configs:
                print(ncs(z).dly_key(xml))
            configs.clear()




