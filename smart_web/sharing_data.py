class database:
    def __init__(self):
        self.Devices= dict({})
    def Device(self,host,loopback,interfaces,process,vlans):
        device = {host:{'ip':loopback,
                        'ospf_process':process,
                        'connect_data':{vlans:interfaces}
                        }}
        self.Devices.update(device)

    def get_interfaces_vlans(self,host):
        interfaces = self.Devices[host]['connect_data']
        return interfaces

if __name__ == '__main__':
    db = database()
    db.Device('172.16.1.1','172.16.1.2','G0/0/1','1',12)
    print(db.Devices)