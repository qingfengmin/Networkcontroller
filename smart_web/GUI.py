import tkinter as tk
from setting_config import config_data as setting
import netconf_session as ncs
from tkinter import ttk

button_list = ['设置BD域', '设置vni', '设置环回口地址范围', '添加网络设备']
action_buttons = []

class netconfapp_gui:
    def __init__(self,root): #将初始化的参数放在这里
        self.root = root
        self.root.title('初代python控制器')
        self.root.geometry('800x600')
        self.design()
        self.Centralized_gateway()
        self.show_buttons()
        self.device_list()
        self.root.mainloop()
        self.contralized = None
        self.tree = None

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("配置资源")
        config_window.geometry("300x300")
        tk.Label(config_window, text="这里是配置资源的窗口").pack()
        #定义配置资源的窗口

        # 定义用于存储输入值的变量
        bd_start_var = tk.StringVar()
        bd_end_var = tk.StringVar()
        vni_start_var = tk.StringVar()
        vni_end_var = tk.StringVar()
        vlan_start_var = tk.StringVar()
        vlan_end_var = tk.StringVar()

        input_vars = [
            (bd_start_var, bd_end_var),
            (vni_start_var, vni_end_var),
            (vlan_start_var, vlan_end_var)
        ]#设置输入框的变量

        for (start_var, end_var), (label_text, frame) in zip(input_vars, [
            ('输入BD域的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入VNI的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入vlan的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
        ]):#设置输入框的标签
            frame.pack(side=tk.TOP, pady=20)
            tk.Label(frame, text=label_text).pack()
            # 将输入框与对应的变量关联
            start_entry = tk.Entry(frame, textvariable=start_var)
            start_entry.pack(side=tk.LEFT, padx=10)
            end_entry = tk.Entry(frame, textvariable=end_var)
            end_entry.pack(side=tk.LEFT, padx=10)

        # 添加一个提交按钮来捕获输入的值
        def get_input_values():
            # 获取输入值
            bd_start = bd_start_var.get()
            bd_end = bd_end_var.get()
            vni_start = vni_start_var.get()
            vni_end = vni_end_var.get()
            vlan_start = vlan_start_var.get()
            vlan_end = vlan_end_var.get()

            setting().BD(bd_start,bd_end)
            setting().vni(vni_start,vni_end)
            setting().vlan(vlan_start,vlan_end)

        submit_button = tk.Button(config_window, text="提交", command=get_input_values)
        submit_button.pack()

    def design(self):
        self.root.config(background='#38D3ED')

        infor1 = tk.Label(self.root, text=
                          '初代控制器,目前只能使用VXlan集中式网关\n如需要配置请先配置相应的资源如BD域或者VNI之类的', bg='green', fg='white')
        infor1.pack()

        config_button = tk.Button(self.root, text="配置资源", command=self.open_config_window)
        config_button.pack()

        add_device_button = tk.Button(self.root, text="添加网络设备", command=self.add_device)
        add_device_button.pack()

        for i in button_list:
            button2 = tk.Button(self.root, text=i, bg='green', fg='white')
            action_buttons.append(button2)

    def device_list(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)
        columns = ('IP地址', '设备类型')
        self.tree  = ttk.Treeview(frame, columns=columns,show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def add_device(self):
        device_windows = tk.Toplevel(self.root)
        device_windows.title("添加网络设备")
        device_windows.geometry("300x300")

        # 创建输入变量
        ip_address_var = tk.StringVar()
        device_type_var = tk.StringVar(value="核心网关")

        # IP地址输入框
        ip_frame = tk.Frame(device_windows)
        ip_frame.pack(pady=20)
        tk.Label(ip_frame, text="设备IP地址:").pack(side=tk.LEFT)
        tk.Entry(ip_frame, textvariable=ip_address_var).pack(side=tk.LEFT, padx=10)

        # 设备类型下拉菜单
        type_frame = tk.StringVar(device_windows)
        type_frame.set("核心网关")
        type_frame_menu = ttk.Combobox(device_windows, textvariable=type_frame, values=["核心网关", "边缘网关"])
        type_frame_menu.pack(pady=20)
        # 提交处理函数
        def submit_device():
            ip = ip_address_var.get()
            dev_type = device_type_var.get()
            setting().create_device(ip, dev_type)


            self.tree.insert('', 'end', values=(ip, dev_type))
            ip_address_var.delete(0, tk.END)
            device_windows.destroy()

        submit_btn = tk.Button(device_windows, text="提交", command=submit_device)
        submit_btn.pack(pady=20)

    def refresh_device_list(self):

        devices = setting().device()

        for ip, dev_type in devices:
            self.tree.insert('', tk.END, values=(ip, dev_type))
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 直接使用 setting 实例调用 devices 方法


    def Centralized_gateway(self):
        self.contralized = tk.IntVar()
        self.checkbutton = tk.Checkbutton(self.root, text='集中式网关', variable=self.contralized,
                                          command=self.show_buttons)
        self.checkbutton.pack()

    def show_buttons(self):
        if self.contralized.get():
            for button in action_buttons:
                button.pack()
        else:
            for button in action_buttons:
                button.pack_forget()

# if __name__ == '__main__':
#     netconfapp_gui(4).refresh_device_list()
#     netconfapp_gui(4).refresh_device_list()