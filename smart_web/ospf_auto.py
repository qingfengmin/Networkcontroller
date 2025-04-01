from Configuring_the_database import config as con
from netconf_session import netconf_auto as ncs

class ospf_auto:
    def __init__(self,sharing_data):
        self.db = sharing_data
        self.device = self.db.Devices
        self.con = con()

    def ospf_process(self, process_id, area_id):
        for device in self.db.Devices.keys():
            interfaces = ['loopback0'] + [f'vlanif{vlan}' for vlan in self.db.Devices[device]['vlanif'].keys()]
            router_id = self.db.Devices[device]['loopback_ip']
            conlist = [self.con.ospf_Process(process_id, router_id, area_id)]
            conlist.extend([self.con.ospf_network(process_id, area_id, interface) for interface in interfaces])
            for config in conlist:
                result = ncs(device).dly_key(config)
                print(result)
            print('OSPF进程及其区域配置成功')




    
