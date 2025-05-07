from flask import Blueprint,request,jsonify
import reabase as rea,hashlib as hash

user_login = Blueprint('user_login',__name__)

_mysql = rea.reamysql()

@user_login.route('/api/create_user',methods=['POST'])
def create_user():
    data = request.get_json()

    username = data['username']
    password = data['password']
    #获取前端传递的用户名和密码
    # print(username,password)
    if not username or not password :
        #如果用户名和密码都不为空,则创建用户
        return jsonify({'message': '请输入用户名和密码'}), 400
    else:
        hspassword = __md5_hash(password)
        #将密码进行哈希处理,然后存入数据库
        _mysql.create_user(username,hspassword)

        return jsonify({'message':'用户创建成功,请重新登陆'}),200

@user_login.route('/api/user_login',methods=['POST'])
def user_logins():
    data = request.get_json()
    username = data['username']
    password = data['password']
    # print(username,password)
    if not username or not password:
        #如果用户名和密码都不为空,则进行登录
        return jsonify({'message':'请输入用户名和密码'}),400
    else:
        hspassword = __md5_hash(password)
        #将密码进行哈希处理,然后与数据库中的哈希值进行比较
        datapassword  = _mysql.read_user_password(username)
        if hspassword == datapassword:
            return jsonify({'message':'登录成功'}),200
        else:
            return jsonify({'message':'用户名或密码错误'}),400

@user_login.route('/api/update',methods=['POST'])
def forgot_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    #获取前端传递的用户名和密码
    if not username:
        #如果用户名不为空,则进行密码重置
        return jsonify({'message':'请输入用户名'}),400
    else:
        hspassword = __md5_hash(password)
        _mysql.update_user(username,hspassword)
        return jsonify({'message':'密码重置成功,请重新登陆'}),200

@user_login.route('/api/user_logout',methods=['POST'])
def user_logout():
    return jsonify({'message':'登出成功'}),200


def __md5_hash(data):
    #这是一个简单的MD5哈希函数,我们将密码参数转化为哈希值存存入数据库,
    # 如果用户使用密码登录,我们将密码再次进行哈希,然后与数据库中的哈希值进行比较
    hash_object = hash.md5(data.encode('utf-8'))
    # 获取十六进制表示的哈希值
    return hash_object.hexdigest()

# data = __md5_hash('kunhua@123')
# print(data)
# #


