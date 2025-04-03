from Configuring_the_database import config as con
from setting_config import config_data as setting
from random import choice as cho
from netconf_session import netconf_auto as ncs
import tkinter as tk
from tkinter import ttk

class vxlan_auto:
    def __init__(self,sharing_data):
        #传入sharing_data，用于共享数据
        self.db = sharing_data
        self.device = self.db.Devices
        self.host = self.db.hostlist
        self.bd_list = list(setting().BD())
        self.vni_list = list(setting().vni())
        self.con = con()

    def bgp_evpn_gui(self, parent_window):
        """BGP EVPN配置窗口"""
        bgp_window = tk.Toplevel(parent_window)
        bgp_window.title("BGP EVPN配置")
        bgp_window.geometry("300x200")
        
        ttk.Label(bgp_window, text="BGP AS号:").pack(pady=5)
        as_entry = ttk.Entry(bgp_window)
        as_entry.pack(pady=5)
        as_entry.insert(0, "100")  # 默认值
        
        def on_configure():
            as_number = as_entry.get()
            self.__bgp_peer(as_number)
            bgp_window.destroy()
            
        ttk.Button(bgp_window, text="配置", command=on_configure).pack(pady=10)

    def vxlan_gateway_gui(self, parent_window):
        """VXLAN网关配置窗口"""
        vxlan_window = tk.Toplevel(parent_window)
        vxlan_window.title("VXLAN网关配置")
        vxlan_window.geometry("300x600")
        
        ttk.Label(vxlan_window, text="BD ID:").pack(pady=5)
        bd_entry = ttk.Entry(vxlan_window)
        bd_entry.pack(pady=5)
        
        ttk.Label(vxlan_window, text="VNI:").pack(pady=5)
        vni_entry = ttk.Entry(vxlan_window)
        vni_entry.pack(pady=5)

        ttk.Label(vxlan_window, text="RD:").pack(pady=5)
        rd_entry = ttk.Entry(vxlan_window)
        rd_entry.pack(pady=5)

        ttk.Label(vxlan_window, text="Export_RT:").pack(pady=5)
        import_rt_entry = ttk.Entry(vxlan_window)
        import_rt_entry.pack(pady=5)

        ttk.Label(vxlan_window, text="Import_RT:").pack(pady=5)
        import_rt_entry = ttk.Entry(vxlan_window)
        import_rt_entry.pack(pady=5)

        ttk.Label(vxlan_window, text="网关地址:").pack(pady=5)
        ip_entry = ttk.Entry(vxlan_window)
        ip_entry.pack(pady=5)

        ttk.Label(vxlan_window, text="掩码:").pack(pady=5)
        mask_entry = ttk.Entry(vxlan_window)
        mask_entry.pack(pady=5)
        mask_entry.insert(0, "255.255.255.0")  # 默认值
        
        def on_configure():
            bd = bd_entry.get() or None
            vni = vni_entry.get() or None
            rd = rd_entry.get()
            export_rt = import_rt_entry.get()
            import_rt = import_rt_entry.get()
            address = ip_entry.get()
            mask = mask_entry.get()
            self.__vxlan_tunnel(bd, vni)
            self.__tunnel(address,mask,bd,rd,import_rt,export_rt)
            vxlan_window.destroy()
            
        ttk.Button(vxlan_window, text="配置", command=on_configure).pack(pady=10)

    def __bgp_peer(self, as_number):
        #配置BGP对等体,无需被调用,所以隐藏了
        for device_ip in self.device:
            config = [
                self.con.bgp(as_number, self.device[device_ip]['loopback_ip'])
            ]
            for peer_ip in self.device[device_ip]['bgppeer'].values():
                config.extend(self.con.bgp_neighbor(peer_ip, as_number, 'LoopBack0'))
            
            for xml_config in config:
                print(ncs(device_ip).dly_key(xml_config))

    def __vxlan_tunnel(self, bd=None, vni=None):
        #配置VXLAN隧道,无需被调用,所以隐藏了
        bd = bd or cho(self.bd_list)
        vni = vni or cho(self.vni_list)
        
        for device_ip in self.device:
            configs = [
                self.con.nve_source(self.device[device_ip]['loopback_ip'])
            ]
            configs.extend(self.con.vxlan_BD(bd, vni))

            for xml_config in configs:
                print(ncs(device_ip).dly_key(xml_config))

    def __tunnel(self,address,mask,bd_id,RD,import_rt,export_rt):
        #配置VXLAN网关,无需被调用,所以隐藏了
        configs = []
        for z in self.host.keys():
            if self.host[z] == '核心设备':
                configs.extend(self.con.l3evpn(bd_id, RD, export_rt, import_rt))
                configs.append(self.con.interface_addrsss(f'vbdif{bd_id}',address,mask))
            if self.host[z] == '边界设备':
                configs.extend(self.con.l3evpn(bd_id, RD, import_rt, export_rt))
            for xml in configs:
                print(ncs(z).dly_key(xml))
            configs.clear()




