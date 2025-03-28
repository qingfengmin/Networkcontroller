import ipaddress
import logging

from ncclient import manager


class NetconfSession:
    @staticmethod
    def deploy_ospf_config(host, port, username, password, callback=None, **ospf_params):
        """
        :param ospf_params: 可接收router_id/area_id/network等参数
        :param callback: 配置完成后的回调函数
        """
        required_params = ['instance_id', 'router_id', 'area_id', 'network', 'mask']
        for param in required_params:
            if param not in ospf_params:
                error_msg = f"缺少必要参数 {param}"
                logging.error(f"{host} 配置失败: {error_msg}")
                if callback:
                    callback(host, port, False, error_msg)
                return False
        try:
            # 将前缀长度转换为通配符掩码
            try:
                prefix_length = int(ospf_params['mask'])
                net = ipaddress.ip_network(f"0.0.0.0/{prefix_length}", strict=False)
                wildcard_mask = str(ipaddress.IPv4Address(int(net.hostmask)))
            except ValueError:
                # 如果输入的不是有效的前缀长度，使用原始值
                wildcard_mask = ospf_params['mask']

            with manager.connect(host=host, port=port, username=username,
                              password=password, hostkey_verify=False,
                              device_params={'name': 'huawei'}) as conn:

                # 动态生成OSPF配置
                ospf_config = f'''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <ospfv2 xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <ospfv2comm>
            <ospfSites>
                <ospfSite>
                    <processId>{ospf_params['instance_id']}</processId>
                    <areas>
                        <area>
                            <areaId>{ospf_params['area_id']}</areaId>
                            <networks>
                                <network operation="merge">
                                    <ipAddress>{ospf_params['network']}</ipAddress>
                                    <wildcardMask>{wildcard_mask}</wildcardMask>
                                </network>
                            </networks>
                        </area>
                    </areas>
                </ospfSite>
            </ospfSites>
        </ospfv2comm>
    </ospfv2>
</config>
                '''

                conn.edit_config(target='running', config=ospf_config)
                logging.info(f"成功部署OSPF到{host}:{port}")
                if callback:
                    callback(host, port, True)
                return True

        except Exception as e:
            logging.error(f"{host} 配置失败: {str(e)}")
            if callback:
                callback(host, port, False, str(e))
            return False

    @staticmethod
    def deploy_vxlan_config(host, port, username, password, role, vxlan_params, callback=None):
        try:
            with manager.connect(host=host, port=port, username=username,
                              password=password, hostkey_verify=False,
                              device_params={'name': 'huawei'}) as conn:

                base_config = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <vxlan xmlns="http://www.huawei.com/netconf/vrp">
        <vxlans>
            <vxlan operation="merge">
                <vni>{vni}</vni>
                <gateway>{gateway}</gateway>'''.format(**vxlan_params)

                if role == '边界网关':
                    base_config += '''
                <bgpEvpn>
                    <routeDistinguisher>{rd}</routeDistinguisher>
                    <exportRt>{export_rt}</exportRt>
                </bgpEvpn>'''.format(**vxlan_params)
                elif role == '核心设备':
                    base_config += '''
                <tunnel>
                    <source>{source_ip}</source>
                    <binding>
                        <vlan>{vlan}</vlan>
                    </binding>
                </tunnel>'''.format(**vxlan_params)

                base_config += '''
            </vxlan>
        </vxlans>
    </vxlan>
</config>'''

                conn.edit_config(target='running', config=base_config)
                logging.info(f"{host} VXLAN配置成功")
                if callback:
                    callback(host, port, True)
                return True

        except Exception as e:
            logging.error(f"{host} VXLAN配置失败: {str(e)}")
            if callback:
                callback(host, port, False, str(e))
            return False