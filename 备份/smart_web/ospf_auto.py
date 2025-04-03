from Configuring_the_database import config as con
from netconf_session import netconf_auto as ncs
import tkinter as tk
from tkinter import ttk

class ospf_auto:
    def __init__(self, sharing_data):
        #调入sharing_data，用于共享数据
        self.db = sharing_data
        self.device = self.db.Devices
        self.con = con()

    def ospf_gui(self, parent_window):
        #OSPF协议配置的窗口
        ospf_window = tk.Toplevel(parent_window)
        ospf_window.title("OSPF配置")
        ospf_window.geometry("300x200")
        
        # 进程ID输入
        ttk.Label(ospf_window, text="OSPF进程ID:").pack(pady=5)
        process_entry = ttk.Entry(ospf_window)
        process_entry.pack(pady=5)
        process_entry.insert(0, "1")  # 默认值
        
        # 区域ID输入
        ttk.Label(ospf_window, text="区域ID:").pack(pady=5)
        area_entry = ttk.Entry(ospf_window)
        area_entry.pack(pady=5)
        area_entry.insert(0, "0.0.0.0")  # 默认值
        
        # 配置按钮
        def on_configure():
            process_id = process_entry.get()
            area_id = area_entry.get()
            self.__ospf_process(process_id, area_id)
            ospf_window.destroy()
            
        ttk.Button(
            ospf_window, 
            text="配置", 
            command=on_configure
        ).pack(pady=10)

    def __ospf_process(self, process_id, area_id):
        #用于配置OSPF进程和区域的方法,不需要被调用,所以隐藏了
        for device in self.db.Devices.keys():
            interfaces = ['loopback0'] + [f'vlanif{vlan}' for vlan in self.db.Devices[device]['vlanif'].keys()]
            router_id = self.db.Devices[device]['loopback_ip']
            conlist = [self.con.ospf_Process(process_id, router_id, area_id)]
            conlist.extend([self.con.ospf_network(process_id, area_id, interface) for interface in interfaces])
            for config in conlist:
                result = ncs(device).dly_key(config)
                print(result)
            print('OSPF进程及其区域配置成功')




    
