from flask import Blueprint,request,jsonify

from ospf_auto import ospf_auto as ospf
from VXlan_auto import vxlan_auto as vxlan 
#用于配置设备的类,包括设备管理,路由协议等,不需要引入其它的参数

class route_protocol:
    def __init__(self):
        self.ospf = ospf()
        self.vxlan = vxlan()
        self.device_route_protocol = Blueprint('device_route_protocol',__name__)
        #创建蓝图,用于加载路由
        self.ospf_config()
        self.bgp_config()
        self.vxlan_gateway()
        #加载路由协议配置的路由


    def ospf_config(self):
        @self.device_route_protocol.route('/api/ospf_config', methods=['POST'])
        def ospf_config():
            data = request.get_json()
            #处理前端传递的OSPF数据
            ospf_process_id = data['ospf_process']
            ospf_area_id = data['ospf_area']
            print(ospf_process_id,ospf_area_id)
            if not ospf_process_id or not ospf_area_id:
                return jsonify({'message':'请输入OSPF进程ID和区域ID'}),400
            else:
                self.ospf.ospf_web(ospf_process_id,ospf_area_id)
                return jsonify({'message':'OSPF配置成功'}),200

    def bgp_config(self):
        @self.device_route_protocol.route('/api/bgp_config', methods=['POST'])
        def bgp_config():
            data = request.get_json()
            as_number = data['as_number']
            #处理前端传递的BGP数据
            if not as_number:
                return jsonify({'message':'请输入AS号'}),400
            else:
                self.vxlan.bgp_peer_web(as_number)
                return jsonify({'message':'BGP配置成功'}),200

    def vxlan_gateway(self):
        @self.device_route_protocol.route('/api/vxlan_gateway', methods=['POST'])
        def vxlan_config():
            data = request.get_json()
            address = data['address'];mask = data['mask']
            bd_id = data['bd_id'];vni= data['vni'];RD = data['RD']
            import_rt = data['import_rt'];export_rt = data['export_rt']
            #处理前端传递的VXLAN网关数据
            self.vxlan.vxlan_gateway_web(bd_id,vni,RD,import_rt,export_rt,address,mask)
            #调用VXLAN网关配置的方法`
            return jsonify({'message':'VXLAN网关配置成功'}),200


