from setting_config import config_data as settings
from netconf_session import netconf_auto as nc
from Configuring_the_database import generic,config
import random

class database:
    def __init__(self):
        self.Devices = {}
        self.__interface_infor = {}
        self.hostlist = {}
        self.con = config()
        self.__loopback_network = list(settings().loopback().keys())
        self.gui_logger = None  # 新增GUI日志引用

    def set_gui_logger(self, logger_func):
        """设置GUI日志函数"""
        self.gui_logger = logger_func

    def must_config(self):
        devicelist = self.Devices.keys()
        list = []
        for i in devicelist:
            list.append(generic['lldp_enable'])
            list.append(generic['evpn_overlay'])
            list.append(generic['nve1'])
            loopback_ip = self.Devices[i]['loopback_ip']
            list.append(self.con.interface_addrsss(f'loopback0',loopback_ip, '255.255.255.255'))
            for j in list:
                out = nc(i).dly_key(j)
                if self.gui_logger:
                    self.gui_logger(str(out))  # 使用GUI日志
                else:
                    print(out)  # 保留终端输出
            list.clear()

    def create_device(self, host, device_type):
        try:
            self.hostlist[host] = device_type
            return self.hostlist
        except ValueError as e:
            print(f"输入的网络地址或子网掩码无效: {e}")
            return []

    def delete_device(self, host):
        if host in self.hostlist:
            del self.hostlist[host]

    def init(self):
        for host in self.hostlist.keys():
            info = self.__neighbor(host)
            loopback_ip = random.choice(self.__loopback_network)
            self.Devices[host] = {
                'devices_name': info[host]['devices_name'],
                'loopback_ip': loopback_ip
            }
        # 在最后添加返回生成结果
        self.Devices = self.__generate_vlan_config(self.__interface_infor)
        return self.Devices  # 确保返回生成的配置

    # 原方法使用print直接输出到终端
    def check_device(self):
        print("\n" + "="*40 + " 设备配置清单 " + "="*40)
        for host, config in self.Devices.items():
            print(f"\n设备IP: {host}")
            print(f"设备名称: {config['devices_name']}")
            print(f"环回地址: {config['loopback_ip']}")

            # 接口配置信息
            if config['interface']:
                print("\n接口配置:")
                for intf, vlan in config['interface'].items():
                    ip = config['vlanif'].get(vlan, '未分配IP')
                    print(f"  {intf.ljust(8)} => VLAN {str(vlan).ljust(4)} | IP: {ip}")
            else:
                print("\n该设备暂无接口配置")

            print("-"*90)
        print("="*100 + "\n")

    def get_device(self):
        output = []
        output.append("\n" + "="*40 + " 设备配置清单 " + "="*40)
        for host, config in self.Devices.items():
            output.append(f"\n设备IP: {host}")
            output.append(f"设备名称: {config['devices_name']}")
            output.append(f"环回地址: {config['loopback_ip']}")

            if config['interface']:
                output.append("\n接口配置:")
                for intf, vlan in config['interface'].items():
                    ip = config['vlanif'].get(vlan, '未分配IP')
                    output.append(f"  {intf.ljust(8)} => VLAN {str(vlan).ljust(4)} | IP: {ip}")
            else:
                output.append("\n该设备暂无接口配置")

            output.append("-"*90)
        output.append("="*100 + "\n")
        return '\n'.join(output)  # <mcsymbol name="get_device" filename="sharing_data.py" path="e:\项目\pythonproject\smart_web\sharing_data.py" startline="36" type="function"></mcsymbol>

    def must_config(self):
        devicelist = self.Devices.keys()
        list = []
        for i in devicelist:
            list.append(generic['lldp_enable'])
            list.append(generic['evpn_overlay'])
            list.append(generic['nve1'])
            loopback_ip = self.Devices[i]['loopback_ip']
            list.append(self.con.interface_addrsss(f'loopback0',loopback_ip, '255.255.255.255'))
            for j in list:
                out = nc(i).dly_key(j)
                print(out)
            list.clear()

    def connect_ipaddress(self):
        devicelist = self.Devices.keys()
        list1 =[]
        for i in devicelist:
            config = self.Devices[i]
            # print(config)
            for ints,vs in config['interface'].items():
                vlanlist = [vs]
                vlans = self.__vlan_format(vlanlist)
                list1.append(self.con.create_vlan(vs))
                list1.append(self.con.GE_interface(ints,vlans))
                list1.append(self.con.interface_addrsss(f'vlanif{vs}',config['vlanif'][vs],'255.255.255.252'))
            out = nc(i)
            for j in list1:
                # print(list1)
                res = out.dly_key(j)
                print(res)
                # print(j)
            list1.clear()

    def __neighbor(self, host):
        device = nc(host).get_interfaces()
        self.__interface_infor.update(device)
        return device

    def __vlan_format(self, vlan_list):
        # 初始化两个长度为 4096 的二进制数组，默认值为 '0'
        allow_binary_array = ['0'] * 4096
        change_binary_array = ['0'] * 4096

        # 默认放行 VLAN 1
        allow_binary_array[2] = '1'  # VLAN 1 对应第 2 个二进制位
        change_binary_array[2] = '1'

        # 将输入的 VLAN 编号对应的位置设置为 '1'
        for vlan in vlan_list:
            if 1 <= vlan <= 4094:  # 确保 VLAN 在有效范围内
                allow_binary_array[vlan + 1] = '1'  # VLAN 1 对应第 2 个二进制位
                change_binary_array[vlan + 1] = '1'

        # 拼接成完整的二进制字符串
        allow_binary_string = ''.join(allow_binary_array)
        change_binary_string = ''.join(change_binary_array)

        # 截取中间的 4094 位，去掉首尾两个 '0'
        allow_binary_string = allow_binary_string[1:-1]
        change_binary_string = change_binary_string[1:-1]

        # 填充到 4094 位，确保每部分正好 1024 位十六进制数
        allow_binary_string = allow_binary_string.ljust(4094, '0')
        change_binary_string = change_binary_string.ljust(4094, '0')

        # 将二进制字符串分割为每 4 位一组，然后转换为十六进制字符
        def binary_to_hex(binary_string):
            hex_result = ''
            for i in range(0, len(binary_string), 4):
                chunk = binary_string[i:i+4]
                # 确保每个 chunk 都是 4 位，不足 4 位时补零
                chunk = chunk.ljust(4, '0')
                hex_digit = hex(int(chunk, 2))[2:].upper()  # 转为十六进制并去掉 '0x' 前缀
                hex_result += hex_digit
            return hex_result

        # 获取前 1024 位和后 1024 位的十六进制字符串
        allow_hex_part = binary_to_hex(allow_binary_string[:4094])
        change_hex_part = binary_to_hex(change_binary_string[:4094])

        # 返回最终的结果
        return f"{allow_hex_part}:{change_hex_part}"

    def __generate_vlan_config(self, lldp_info):
        # 直接获取最新配置
        vlan_range = settings().vlan()
        subnets = settings().subnetwork_partition()
        assigned_vlans = {}
        vlan_ip_networks = {}
        assigned_ips = set()
        vlan_config = {}

        for host_ip, info in lldp_info.items():
            interfaces = info['interface']
            vlan_config[host_ip] = {
                'devices_name': info['devices_name'],
                'loopback_ip': self.Devices.get(host_ip, {}).get('loopback_ip', ''),
                'vlanif': {},
                'interface': {},
                'bgppeer': {}
            }

            for interface, neighbor_device in interfaces.items():
                neighbor_host = next((ip for ip, data in lldp_info.items() 
                                    if data['devices_name'] == neighbor_device), None)
                
                # 生成链路标识(确保双向链路使用相同VLAN)
                link = tuple(sorted([
                    (host_ip, interface), 
                    (neighbor_host, next(
                        iface for iface, dev in lldp_info[neighbor_host]['interface'].items() 
                        if dev == info['devices_name']
                    ))
                ]))

                # 分配VLAN
                vlan = assigned_vlans.get(link) or random.choice(vlan_range)
                assigned_vlans[link] = vlan
                vlan_config[host_ip]['interface'][interface] = vlan

                # 分配IP地址
                if vlan not in vlan_ip_networks:
                    if subnets:
                        vlan_ip_networks[vlan] = subnets.pop(0)
                    else:
                        continue

                ip_network = vlan_ip_networks.get(vlan)
                ip_generator = ip_network.hosts()
                ip = next((ip for ip in ip_generator if str(ip) not in assigned_ips), None)
                
                if ip:
                    assigned_ips.add(str(ip))
                    vlan_config[host_ip]['vlanif'][vlan] = str(ip)
                
                # 添加BGP邻居信息
                if neighbor_host:
                    neighbor_loopback = self.Devices.get(neighbor_host, {}).get('loopback_ip', '')
                    print(neighbor_loopback)
                    if neighbor_loopback:
                        vlan_config[host_ip]['bgppeer'][interface] = neighbor_loopback

        return vlan_config