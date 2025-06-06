import tkinter as tk
from tkinter import messagebox,ttk
from setting_config import config_data as setting
from sharing_data import database as db
from ospf_auto import ospf_auto
from VXlan_auto import vxlan_auto as vx
from reabase import reamysql as rea
from read_files import readfile as rf


class netconfapp_gui:
    def __init__(self, root): # 创建database实例 # 设置日志回调
        #等待被主程序调用
        self.root = root
        self.root.title('初代python控制器')
        self.root.geometry('800x800')
        # 确保在 __init__ 方法中正确初始化 setting 属性
        self.sql = rea()
        #数据库接口函数

        self.rf = rf()

        self.setting = None
        self.db = None
        #用于存储配置信息的变量,实例化setting和database类,

        # 实现GUI的参数,和sharing_data的参数一致
        self.button_list = [
            ('配置OSPF', self.configure_ospf),
            ('配置BGP_EVPN', self.configure_bgp_evpn),
            ('配置VXLAN集中式网关', self.configure_vxlan_gateway)
        ]
        self.action_buttons = []  # 也移到init内部

        self.design()
        self.Centralized_gateway()
        self.show_buttons()
        self.device_list()
        self.create_console()
        #各种GUI的配置函数
        self.root.mainloop()
        self.resource_id = None
        self.contralized = None
        self.tree = None

    def open_config_window(self):
        # 资源配置窗口
        config_window = tk.Toplevel(self.root)
        config_window.title("配置资源")
        config_window.geometry("300x500")
        tk.Label(config_window, text="这里是配置资源的窗口").pack()
        # 定义用于存储输入值的变量//相比上个版本这里新增了资源ID的新字段
        resource_var = tk.StringVar()
        bd_start_var = tk.StringVar()
        bd_end_var = tk.StringVar()
        vni_start_var = tk.StringVar()
        vni_end_var = tk.StringVar()
        vlan_start_var = tk.StringVar()
        vlan_end_var = tk.StringVar()
        ipaddress = tk.StringVar()
        mask = tk.StringVar()

        resource_var.set('1')
        bd_start_var.set('11')
        bd_end_var.set('150')
        vni_start_var.set('11')
        vni_end_var.set('150')
        vlan_start_var.set('11')
        vlan_end_var.set('150')
        ipaddress.set("10.1.100.0/24")
        mask.set("30")

        # 设置输入框的变量，将 resource_var 单独添加到列表中
        input_vars = [
            (resource_var,),
            (bd_start_var, bd_end_var),
            (vni_start_var, vni_end_var),
            (vlan_start_var, vlan_end_var),
            (ipaddress, mask)
        ]

        # 设置输入框的标签
        label_texts = [
            ('输入资源ID,如不输入将采用默认值1', tk.Frame(config_window)),
            ('输入BD域的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入VNI的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入vlan的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入互联地址网段,如不输入将采用默认10.1.100.0/24 30', tk.Frame(config_window))
        ]

        for vars, (label_text, frame) in zip(input_vars, label_texts):
            frame.pack(side=tk.TOP, pady=20)
            tk.Label(frame, text=label_text).pack()
            for var in vars:
                entry = tk.Entry(frame, textvariable=var)
                entry.pack(side=tk.LEFT, padx=10)

        # 添加一个提交按钮来捕获输入的值
        def get_input_values():
            # 获取输入值并设置默认值
            resource_id = resource_var.get() or "1"  # 如果为空则使用默认值
            bd_start = bd_start_var.get() # 如果为空则使用默认值
            bd_end = bd_end_var.get()
            vni_start = vni_start_var.get()
            vni_end = vni_end_var.get()
            vlan_start = vlan_start_var.get()
            vlan_end = vlan_end_var.get()
            ipaddress_net = ipaddress.get()   # 默认网段
            mask_net = mask.get()   # 默认掩码
            #相比上个版本这里新增了资源ID的新字段,不同的是这里不需要进行判断是否使用默认值,因为在数据库中已经设置了默认值

            # 相比于上个版本这个版本不需要将数据更新给其它的PY文件,而是直接将数据更新至数据库中
            self.sql.create(resource_id)
            #创建ID后,将数据更新至数据库中
            self.sql.update_resource('bd_after',bd_end,resource_id)
            self.sql.update_resource('bd_before',bd_start,resource_id)
            self.sql.update_resource('vni_after',vni_end,resource_id)
            self.sql.update_resource('vni_before',vni_start,resource_id)
            self.sql.update_resource('vlan_after',vlan_end,resource_id)
            self.sql.update_resource('vlan_before',vlan_start,resource_id)
            self.sql.update_resource_str('ip_address',ipaddress_net,resource_id)
            self.sql.update_resource_str('ip_mask',mask_net,resource_id)

            # 添加调试信息
            self.log_message(f"已更新配置 - IP网段: {ipaddress_net}, 掩码: {mask_net}")

            self.rf.wirte_res({'resource':f'{resource_id}'})
            self.__lumped_call()
            #将用户输入的资源ID传递给user_id函数,以便其它的函数以及PY文件可以使用这个资源

            config_window.destroy()
            #这是窗口关闭的函数,如果不关闭,则会一直打开,导致程序无法继续运行


        submit_button = tk.Button(config_window, text="提交", command=get_input_values)
        submit_button.pack()


    def design(self):
        # 设计GUI按钮的函数
        self.root.config(background='#38D3ED')

        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 信息标签
        infor1 = tk.Label(main_frame,
                         text='初代控制器,目前只能使用VXlan集中式网关\n如需要配置请先配置相应的资源如BD域或者VNI之类的',
                         bg='green', fg='white')
        infor1.grid(row=0, column=0, columnspan=2, pady=5, sticky='ew')

        # 第一行按钮
        config_button = tk.Button(main_frame, text="配置资源", command=self.open_config_window)
        config_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        add_device_button = tk.Button(main_frame, text="添加网络设备", command=self.add_device)
        add_device_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # 第二行按钮
        init_button = tk.Button(main_frame, text="初始化", command=lambda: self.db.init())
        init_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        get_config_button = tk.Button(main_frame, text="查看配置",
                                    command=lambda: self.log_message(self.db.get_device()))
        get_config_button.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        # 第三行按钮
        init_config = tk.Button(main_frame, text="初始配置", command=lambda: self.db.must_config())
        init_config.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        connect_address = tk.Button(main_frame, text='互联地址', command=lambda: self.db.connect_ipaddress())
        connect_address.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        # 配置网格权重
        for i in range(4):
            main_frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            main_frame.grid_columnconfigure(j, weight=1)

        # 功能按钮(保持原样)
        for text, command in self.button_list:
            button = tk.Button(main_frame, text=text, bg='green', fg='white', command=command)
            self.action_buttons.append(button)

    def device_list(self):
        #用来操控设备的列表的主要函数
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)
        columns = ('IP地址', '设备类型')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 添加删除按钮
        delete_button = ttk.Button(frame, text="删除设备", command=self.delete_device)
        delete_button.pack(side=tk.BOTTOM, pady=5)

    def add_device(self):
        #添加设备的主要窗口
        device_windows = tk.Toplevel(self.root)
        device_windows.title("添加网络设备")
        device_windows.geometry("300x300")

        # 设备参数输入项
        ttk.Label(device_windows, text='IP地址:').grid(row=0, column=0)
        ip_entry = ttk.Entry(device_windows)
        ip_entry.grid(row=0, column=1)

        ttk.Label(device_windows, text='设备类型:').grid(row=1, column=0)
        device_type_combo = ttk.Combobox(device_windows, values=['核心设备', '边界设备', '接入设备'])
        device_type_combo.current(0)
        device_type_combo.grid(row=1, column=1)

        def validate_and_add():
            if not all([ip_entry.get(), device_type_combo.get()]):
                messagebox.showerror('错误', '必填字段不能为空')
                return

            host = ip_entry.get()
            device_type = device_type_combo.get()
            # 调用 setting_config 中的 create_device 方法添加设备
            self.db.create_device(host, device_type)

            self.tree.insert('', 'end', values=(
                host,
                device_type
            ))
            device_windows.destroy()

        ttk.Button(device_windows, text='添加', command=validate_and_add).grid(row=2, columnspan=2, pady=10)

    def delete_device(self):
        #删除设备的主要窗口
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, "values")
            host = item_values[0]
            # 调用 setting_config 中的 delete_device 方法删除设备
            self.db.delete_device(host)
            self.tree.delete(selected_item)
        else:
            messagebox.showwarning("警告", "请先选择要删除的设备。")

    def Centralized_gateway(self):
        #集中式网关的主要函数
        self.contralized = tk.IntVar()
        self.checkbutton = tk.Checkbutton(self.root, text='集中式网关', variable=self.contralized,
                                          command=self.show_buttons)
        self.checkbutton.pack()

    def show_buttons(self):
        #集中式网关配置按钮的循环函数
        if self.contralized.get():
            # 显示所有功能按钮
            for i, button in enumerate(self.action_buttons):
                button.grid(row=4+i, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        else:
            # 隐藏所有功能按钮
            for button in self.action_buttons:
                button.grid_forget()

    def create_console(self):

        """创建日志输出控制台"""

        console_frame = ttk.Frame(self.root)

        console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 控制台标签
        ttk.Label(console_frame, text="运行日志:").pack(anchor=tk.W)

        # 带滚动条的文本框
        self.console_text = tk.Text(console_frame, wrap=tk.WORD, state='disabled', height=10)
        scroller = ttk.Scrollbar(console_frame, command=self.console_text.yview)

        self.console_text.configure(yscrollcommand=scroller.set)
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroller.pack(side=tk.RIGHT, fill=tk.Y)

    def __lumped_call(self):
        self.setting = setting()
        self.db = db()

    def log_message(self, message):
        """向控制台添加日志"""
        self.console_text.configure(state='normal')
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END)  # 自动滚动到底部
        self.console_text.configure(state='disabled')

    def configure_ospf(self):
        #OSPF进程配置窗口的函数,了解详细信息,请查看ospf_auto.py
        ospf = ospf_auto()  # 传入数据库实例
        ospf.ospf_gui(self.root)  # 打开OSPF配置窗口
        self.log_message("正在配置OSPF...")

    def configure_bgp_evpn(self):
        #BGP EVPN配置窗口的函数,了解详细信息,请查看VXlan_auto.py
        vxlan = vx()
        vxlan.bgp_evpn_gui(self.root)
        self.log_message("正在配置BGP EVPN...")

    def configure_vxlan_gateway(self):
        #VXLAN网关配置窗口的函数,了解详细信息,请查看VXlan_auto.py
        vxlan = vx()
        vxlan.vxlan_gateway_gui(self.root)
        self.log_message("正在配置VXLAN集中式网关...")

# class user_id:
#     #用于设置资源ID的类,在主程序中调用,也可为其它的PY文件调用,
#     def __init__(self, resource):
#         self.resource = resource

