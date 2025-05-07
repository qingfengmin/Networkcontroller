from flask import Blueprint, request, jsonify
from sharing_data import database as db
from flask_cors import CORS

class DeviceManagement:
    def __init__(self):
        self.db = db()
        self.device_management = Blueprint('device_management',__name__)
        self.device_add()
        self.delete_device()

    def device_add(self):
        @self.device_management.route('/api/add_device', methods=['POST'])
        def add_device():
            data = request.get_json()
            device_name = data['device_ip']
            device_type = data['device_type']
            print(device_name,device_type)
            if not device_name or not device_type:
                return jsonify({'message':'请输入设备名称和类型'}),400
            else:
                self.db.create_device(device_name,device_type)
                return jsonify({'message':'设备添加成功'}),200
        # 处理前端传递的设备信息
    def delete_device(self):
        @self.device_management.route('/api/del_device', methods=['POST'])
        def del_device():
            data = request.get_json()
            device_name = data['device_ip']
            if not device_name:
                return jsonify({'message':'请输入设备名称'}),400
            else:
                self.db.delete_device(device_name)
                return jsonify({'message':'设备删除成功'}),200
            #删除设备信息