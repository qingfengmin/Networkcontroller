from setting_config import config_data as settings
from netconf_session import netconf_auto as nc
import random

class database:
    def __init__(self):
        self.Devices= dict({})
        self.interface_infor = {}
    def Device(self,host,loopback,interfaces,process,vlans):
        device = {host:{'ip':loopback,
                        'ospf_process':process,
                        'connect_data':{vlans:interfaces}
                        }}
        self.Devices.update(device)

    def get_interfaces_vlans(self,host):
        interfaces = self.Devices[host]['connect_data']
        return interfaces

    # def auto_device_info(self):

    def neighbor(self,host):
        device = nc(host).get_interfaces()
        self.interface_infor.update(device)
        print(self.interface_infor)
        return device

    # def

    def __generate_vlan_config(self,lldp_info):
        # 初始化配置数据
        # 获取 VLAN 范围
        vlan_range = settings().vlan()

        # 存储每个设备接口的 VLAN 配置
        vlan_config = {}
        # 存储已经分配的 VLAN 信息
        assigned_vlans = {}

        # 遍历每个设备
        for device, interfaces in lldp_info.items():
            vlan_config[device] = {}
            # 遍历设备的每个接口
            for interface, neighbor in interfaces.items():
                # 构建唯一的连接标识
                link = tuple(sorted([(device, interface), (
                neighbor, [key for key, val in lldp_info[neighbor].items() if val == device][0])]))

                # 检查该连接是否已经分配了 VLAN
                if link in assigned_vlans:
                    # 如果已经分配，则使用相同的 VLAN
                    vlan = assigned_vlans[link]
                else:
                    # 如果未分配，则随机选择一个 VLAN
                    vlan = random.choice(vlan_range)
                    # 记录该连接的 VLAN 分配
                    assigned_vlans[link] = vlan

                # 记录当前设备接口的 VLAN 分配
                vlan_config[device][interface] = vlan

        return vlan_config




if __name__ == '__main__':
    db = database()
    # db.Device('172.16.1.1','172.16.1.2','G0/0/1','1',12)
    list = ['172.16.1.1','172.16.1.2','172.16.1.3']
    for i in list:
        db.neighbor(i)
    # print(db.Devices)