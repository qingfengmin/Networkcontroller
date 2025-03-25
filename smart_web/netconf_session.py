from ncclient import manager
from ncclient.xml_ import to_ele


class netconf_auto:
    def __init__(self, host):
        self.host = host
        self.session = {
            'port': 830,
            'username': 'python',
            'password': 'Huawei@123',
            'hostkey_verify': False,
            'look_for_keys': False,
            'allow_agent': False,
            'device_params': {"name": "huawei"}
        }

    def __get_netconf(self):
        client = manager
        session = client.connect(**self.session, host=self.host)
        return session

    def display_config(self):
        client = self.__get_netconf()
        Brush = client.get_config(source='running')
        return Brush

    def display_config_filter(self, filter):
        filt = self.__get_netconf()
        Brush = filt.get_config(source='running', filter=filter)
        return Brush

    def display_config_get(self):
        client = self.__get_netconf()
        Brush = client.get()
        return Brush

    def display_config_get_filter(self, filter):
        filt = self.__get_netconf()
        Brush = filt.get(filter=filter)
        output = Brush.data_xml
        return output

    def dly_config(self, config_xml):
        dly = self.__get_netconf()
        output = dly.rpc(to_ele(config_xml))
        return output

    def dly_key(self, keys):
        key = self.__get_netconf()
        output = key.edit_config(target='running', config=keys)
        return output
