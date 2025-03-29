import threading
import tkinter as tk
from tkinter import messagebox  # 添加这一行
from tkinter import ttk

from netconf_session import NetconfSession


class NetworkManagerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('华为设备管理平台')

        # 设备列表
        self.device_frame = ttk.LabelFrame(self.root, text='设备列表')
        self.device_tree = ttk.Treeview(self.device_frame, columns=('IP', '端口', '状态', '角色', '用户名', '密码'), show='headings')
        self.device_tree.heading('IP', text='IP地址')
        self.device_tree.heading('端口', text='端口')
        self.device_tree.heading('状态', text='连接状态')
        self.device_tree.heading('角色', text='角色')
        self.device_tree.heading('用户名', text='用户名')
        self.device_tree.heading('密码', text='密码')

        # 操作按钮
        self.add_btn = ttk.Button(self.device_frame, text='添加设备', command=self.add_device)
        self.deploy_btn = ttk.Button(self.device_frame, text='部署OSPF', command=self.deploy_ospf)

        # 初始化设备树组件
        self.device_tree.pack(pady=5, fill='both', expand=True)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        self.device_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # 在操作按钮区增加VXLAN部署按钮
        self.vxlan_btn = ttk.Button(self.device_frame, text='部署VXLAN', command=self.deploy_vxlan)
        self.deploy_btn.pack(side=tk.RIGHT, padx=5)
        self.vxlan_btn.pack(side=tk.RIGHT, padx=5)

    def add_device(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('添加网络设备')

        # 设备参数输入项
        ttk.Label(dialog, text='IP地址:').grid(row=0, column=0)
        ip_entry = ttk.Entry(dialog)
        ip_entry.grid(row=0, column=1)

        ttk.Label(dialog, text='端口:').grid(row=1, column=0)
        port_entry = ttk.Entry(dialog)
        port_entry.insert(0, '830')
        port_entry.grid(row=1, column=1)

        ttk.Label(dialog, text='角色:').grid(row=2, column=0)
        role_combo = ttk.Combobox(dialog, values=['核心设备', '边界网关', '接入设备'])
        role_combo.current(0)
        role_combo.grid(row=2, column=1)

        ttk.Label(dialog, text='用户名:').grid(row=3, column=0)
        user_entry = ttk.Entry(dialog)
        user_entry.grid(row=3, column=1)

        ttk.Label(dialog, text='密码:').grid(row=4, column=0)
        pass_entry = ttk.Entry(dialog, show='*')
        pass_entry.grid(row=4, column=1)

        def validate_and_add():
            if not all([ip_entry.get(), port_entry.get(), user_entry.get()]):
                messagebox.showerror('错误', '必填字段不能为空')
                return

            self.device_tree.insert('', 'end', values=(
                ip_entry.get(),
                port_entry.get(),
                '未连接',
                role_combo.get(),
                user_entry.get(),
                pass_entry.get()
            ))
            dialog.destroy()

        ttk.Button(dialog, text='添加', command=validate_and_add).grid(row=5, columnspan=2, pady=10)

    def deploy_ospf(self):
        param_dialog = tk.Toplevel(self.root)
        param_dialog.title('OSPF参数配置')

        params = {
            '进程号': tk.IntVar(value=1),
            'Router ID': tk.StringVar(value='1.1.1.1'),
            '区域号': tk.StringVar(value='0.0.0.0'),
            '网络地址': tk.StringVar(value='10.0.0.0'),
            '反掩码': tk.StringVar(value='0.0.0.255'),
            '认证方式': tk.StringVar(value='none')
        }

        def validate_params():
            try:
                if not 1 <= params['进程号'].get() <= 65535:
                    raise ValueError('进程号必须为1-65535之间的整数')
                
                # 验证IP地址格式
                for field in ['Router ID', '网络地址', '反掩码']:
                    if not re.match(r'^\d+\.\d+\.\d+\.\d+$', params[field].get()):
                        raise ValueError(f'{field} 格式不正确')
                return True
            except Exception as e:
                messagebox.showerror('参数错误', str(e))
                return False

        def start_deployment():
            if validate_params():
                selected_devices = []
                for item in self.device_tree.selection():
                    device = self.device_tree.item(item)['values']
                    selected_devices.append({
                        'ip': device[0],
                        'port': device[1],
                        'username': device[4],
                        'password': device[5]
                    })

                ospf_params = {
                    'instance_id': params['进程号'].get(),
                    'router_id': params['Router ID'].get(),
                    'area_id': params['区域号'].get(),
                    'network': params['网络地址'].get(),
                    'mask': params['反掩码'].get(),
                    'authentication': {
                        'mode': params['认证方式'].get(),
                        'key': 'Huawei@123' if params['认证方式'].get() != 'none' else ''
                    }
                }

                for device in selected_devices:
                    threading.Thread(
                        target=NetconfSession.deploy_ospf_config,
                        args=(device['ip'], device['port'], device['username'], device['password']),
                        kwargs={'ospf_params': ospf_params, 'callback': self.update_status}
                    ).start()
                param_dialog.destroy()

        row = 0
        for label, var in params.items():
            ttk.Label(param_dialog, text=label).grid(row=row, column=0, padx=5, pady=5)
            if isinstance(var, tk.IntVar):
                ttk.Spinbox(param_dialog, from_=1, to=65535, textvariable=var).grid(row=row, column=1, padx=5, pady=5)
            else:
                ttk.Entry(param_dialog, textvariable=var).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        ttk.Button(param_dialog, text='开始部署', command=start_deployment).grid(row=row, columnspan=2, pady=10)

    def deploy_vxlan(self):
        param_dialog = tk.Toplevel(self.root)
        param_dialog.title('VXLAN参数配置')

        # 根据设备角色动态生成参数项
        params = {
            'VNI': tk.IntVar(value=10000),
            '网关地址': tk.StringVar(value='10.10.10.1'),
            'RD值': tk.StringVar(value='65001:1'),
            'Export RT': tk.StringVar(value='65001:100'),
            '隧道源地址': tk.StringVar(value='1.1.1.1'),
            'VLAN ID': tk.IntVar(value=10)
        }

        # 参数验证逻辑
        def validate_params():
            try:
                if not 1 <= params['VNI'].get() <= 16777215:
                    raise ValueError('VNI必须为1-16777215之间的整数')

                # 根据所选设备角色验证必要参数
                for item in self.device_tree.selection():
                    device_role = self.device_tree.item(item)['values'][3]
                    if device_role == '边界网关' and not params['RD值'].get():
                        raise ValueError('边界网关必须配置RD值')
                    if device_role == '核心设备' and not params['隧道源地址'].get():
                        raise ValueError('核心设备必须配置隧道源地址')
                return True
            except Exception as e:
                messagebox.showerror('参数错误', str(e))
                return False

        # 多线程部署执行逻辑
        def start_deployment():
            if validate_params():
                selected_devices = []
                for item in self.device_tree.selection():
                    device = self.device_tree.item(item)['values']
                    selected_devices.append({
                        'ip': device[0],
                        'port': device[1],
                        'role': device[3],
                        'username': device[4],
                        'password': device[5]
                    })

                'vxlan_params': {
                    'vni': params['VNI编号'].get(),
                    'gateway': params['网关地址'].get(),
                    'rd': params['RD值'].get(),
                    'export_rt': params['Export RT'].get(),
                    'source_ip': params['隧道源地址'].get(),
                    'vlan': params['VLAN ID'].get()
                }

                for device in selected_devices:
                    threading.Thread(
                        target=NetconfSession.deploy_vxlan_config,
                        args=(device['ip'], device['port'], device['username'], device['password'], device['role']),
                        kwargs={'vxlan_params': vxlan_params, 'callback': self.update_status}
                    ).start()
                param_dialog.destroy()

        # 布局参数输入框
        row = 0
        for label, var in params.items():
            ttk.Label(param_dialog, text=label).grid(row=row, column=0, padx=5, pady=5)
            if isinstance(var, tk.IntVar):
                ttk.Spinbox(param_dialog, from_=1, to=16777215, textvariable=var).grid(row=row, column=1, padx=5, pady=5)
            else:
                ttk.Entry(param_dialog, textvariable=var).grid(row=row, column=1, padx=5, pady=5)
            row += 1

        ttk.Button(param_dialog, text='开始部署', command=start_deployment).grid(row=row, columnspan=2, pady=10)

    def update_status(self, host, port, success, error=None):
        # 查找对应设备条目更新状态
        for child in self.device_tree.get_children():
            if self.device_tree.item(child)['values'][0] == host and str(self.device_tree.item(child)['values'][1]) == str(port):
                status = '配置成功' if success else f'失败: {error}'
                self.device_tree.item(child, values=(
                    host,
                    port,
                    status,
                    self.device_tree.item(child)['values'][3],
                    self.device_tree.item(child)['values'][4],
                    self.device_tree.item(child)['values'][5]
                ))
                # 添加消息提示框
                if success:
                    tk.messagebox.showinfo('操作完成', f'{host}:{port} 配置成功')
                else:
                    tk.messagebox.showerror('配置失败', f'{host}:{port} 错误: {error}')

if __name__ == '__main__':
    app = NetworkManagerGUI()
    app.root.mainloop()