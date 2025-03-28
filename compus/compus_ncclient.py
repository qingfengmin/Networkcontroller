
import logging

from ncclient import manager

# 配置日志记录
logging.basicConfig(level=logging.INFO)

# 设备连接信息
device = {
    'host': '192.168.1.1',  # 设备IP地址
    'port': 830,  # NETCONF端口
    'username': 'admin',  # 用户名
    'password': 'password',  # 密码
    'hostkey_verify': False  # 不验证主机密钥
}

# 连接到设备
with manager.connect(**device) as m:
    # 获取设备配置
    config = m.get_config(source='running').data_xml
    logging.info('设备当前配置:\n%s', config)

    # 修改配置示例（这里只是示例，具体修改根据实际需求）
    new_config = '''
    <config>
        <!-- 这里添加要修改的配置内容 -->
    </config>
    '''
    try:
        # 应用新配置
        m.edit_config(target='running', config=new_config)
        logging.info('配置修改成功')
    except Exception as e:
        logging.error('配置修改失败: %s', e)
