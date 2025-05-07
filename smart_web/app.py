from flask import Flask,request,jsonify,render_template
from flask_cors import CORS
#用于WEB网页相关的库

from reabase import reamysql as rea
#使用统一定制的MYSQL方法

from routes import route_protocol
from user_login import user_login
from device_management import DeviceManagement
from template import html_routes as route
#第三方py文件的flask路由

from sharing_data import database as db
#底层用于实现配置的方法

from read_files import readfile as rf
#可以将配置写入配置文件的方法

class controller:
    def __init__(self):
        self.app = Flask(__name__,template_folder='temp_html')
        self.app.register_blueprint(user_login)
        self.app.register_blueprint(route_protocol().device_route_protocol)
        self.app.register_blueprint(DeviceManagement().device_management)

        #加载蓝图
        CORS(self.app)

        self._mysql = rea()
        self.config_resources()
        self.config_init()
        self.must_configs()
        self.config_connect_address()
        route(self.app)
 
        #加载本Py文件的路由

        self.db = None
        self.rf = rf()
        #加载数据库和配置文件


    def config_resources(self):
        #资源配置路由
        @self.app.route('/api/device_resources',methods=['POST'])
        def receive_resources():
            data = request.get_json()
            resource = data['resource']
            bd_start = data['bd_before'];bd_end = data['bd_after']
            vni_start = data['vni_before'];vni_end = data['vni_after']
            vlan_start = data['vlan_before'];vlan_end = data['vlan_after']
            ip_address = data['ip_address'];ip_mask = data['ip_mask']
            #获取前端资源数据

            self._mysql.create(resource)
            self._mysql.update_resource('bd_before',bd_start,resource)
            self._mysql.update_resource('bd_after',bd_end,resource)
            self._mysql.update_resource('vni_before',vni_start,resource)
            self._mysql.update_resource('vni_after',vni_end,resource)
            self._mysql.update_resource('vlan_before',vlan_start,resource)
            self._mysql.update_resource('vlan_after',vlan_end,resource)
            self._mysql.update_resource_str('ip_address',ip_address,resource)
            self._mysql.update_resource_str('ip_mask',ip_mask,resource)
            #更新数据库资源数据

            self.rf.wirte_res({'resource':f'{resource}'})

            self.__loopcall()

            return jsonify({'message':'资源配置成功'}),200

    def config_init(self):
        #初始化配置路由
        @self.app.route('/api/device_init',methods=['POST'])
        def receive_init():
            data = request.get_json()
            ack = data['True']
            if ack == True:
                self.db.init()
                return jsonify({'message':'设备初始化成功'}),200
            else:
                return jsonify({'message':'设备初始化失败'}),400

    def must_configs(self):
        #必须配置路由
        @self.app.route('/api/device_must',methods=['POST'])
        def receive_must():
            data = request.get_json()
            ack = data['True']
            if ack == True:
                self.db.must_config()
                return jsonify({'message':'设备配置成功'}),200
            else:
                return jsonify({'message':'设备配置失败'}),400


    def config_connect_address(self):
        @self.app.route('/api/device_connect_address',methods=['POST'])
        def receive_connect_address():
            data = request.get_json()
            ack = data['True']
            if ack == True:
                self.db.connect_ipaddress()
                return jsonify({'message':'设备配置成功'}),200
            else:
                return jsonify({'message':'设备配置失败'}),400
    
    def index(self):
        @self.app.route('/',methods=['GET'])
        def index_ht():
            return render_template('index.html')
    
    def __loopcall(self):
        #循环调用,用于配置设备
        self.db = db()

def tips():
    print('本程序为网络设备配置程序，用于配置部署网络设备\n'
          '可以通过GUI界面进行配置，也可以通过网页版进行配置\n'
          '网页版会映射到本机的5000端口，通过浏览器访问即可\n'
          '默认本地网页地址为\n'
          'http://127.0.0.1:5000/index.html\n')


# if __name__ == '__main__':
#     app = controller()
#     app.app.run(debug=True)