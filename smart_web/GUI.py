import tkinter as tk
from tkinter import messagebox
from setting_config import config_data as setting
import netconf_session as ncs
from tkinter import ttk
from sharing_data import database as db

button_list = ['设置BD域', '设置vni', '设置环回口地址范围', '添加网络设备']
action_buttons = []

class netconfapp_gui:
    def __init__(self, root):
        self.db = db()  # 创建持久化实例
        self.root = root
        self.root.title('初代python控制器')
        self.root.geometry('800x600')
        # 确保在 __init__ 方法中正确初始化 setting 属性
        self.setting = setting()
        self.db = db()
        self.design()
        self.Centralized_gateway()
        self.show_buttons()
        self.device_list()
        self.create_console()  # 新增控制台初始化
        self.root.mainloop()
        self.contralized = None
        self.tree = None

    def open_config_window(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("配置资源")
        config_window.geometry("300x400")
        tk.Label(config_window, text="这里是配置资源的窗口").pack()
        # 定义用于存储输入值的变量
        bd_start_var = tk.StringVar()
        bd_end_var = tk.StringVar()
        vni_start_var = tk.StringVar()
        vni_end_var = tk.StringVar()
        vlan_start_var = tk.StringVar()
        vlan_end_var = tk.StringVar()
        ipaddress = tk.StringVar()
        mask = tk.StringVar()

        ipaddress.set("10.1.100.0/24")
        mask.set("30")

        input_vars = [
            (bd_start_var, bd_end_var),
            (vni_start_var, vni_end_var),
            (vlan_start_var, vlan_end_var),
            (ipaddress, mask)
        ]  # 设置输入框的变量


        for (start_var, end_var), (label_text, frame) in zip(input_vars, [
            ('输入BD域的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入VNI的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入vlan的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入互联地址网段,如不输入将采用默认10.1.100.0/24 30', tk.Frame(config_window)),
        ]):  # 设置输入框的标签
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
            ipaddress_net = ipaddress.get()
            mask_net = mask.get()
        
            # 更新共享配置
            setting().update_config(
                vlan_range=(int(vlan_start), int(vlan_end)),
                BD_range=(int(bd_start), int(bd_end)),
                vni_range=(int(vni_start), int(vni_end)),
                internet_segment=f"{ipaddress_net}/{mask_net}"
            )
            
            config_window.destroy()

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

        infor2 = tk.Label(self.root, text='点击初始化按钮,将会自动获取网络设备的信息', bg='green', fg='white')
        infor2.pack()

        init_button = tk.Button(self.root, text="初始化", command=lambda :self.db.init())
        init_button.pack()

        infor3 = tk.Label(self.root, text='点击查看配置,可以看见设备配置的基础信息', bg='green', fg='white')
        infor3.pack()

        # 修改查看配置按钮的绑定
        get_config_button = tk.Button(
            self.root, 
            text="查看配置",
            command=lambda: self.log_message(self.db.get_device())  # 输出到GUI控制台
        )
        get_config_button.pack()

        for i in button_list:
            button2 = tk.Button(self.root, text=i, bg='green', fg='white')
            action_buttons.append(button2)

    def device_list(self):
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
        device_windows = tk.Toplevel(self.root)
        device_windows.title("添加网络设备")
        device_windows.geometry("300x300")

        # 设备参数输入项
        ttk.Label(device_windows, text='IP地址:').grid(row=0, column=0)
        ip_entry = ttk.Entry(device_windows)
        ip_entry.grid(row=0, column=1)

        ttk.Label(device_windows, text='设备类型:').grid(row=1, column=0)
        device_type_combo = ttk.Combobox(device_windows, values=['核心设备', '边界网关', '接入设备'])
        device_type_combo.current(0)
        device_type_combo.grid(row=1, column=1)

        def validate_and_add():
            if not all([ip_entry.get(), device_type_combo.get()]):
                messagebox.showerror('错误', '必填字段不能为空')
                return

            host = ip_entry.get()
            device_type = device_type_combo.get()
            print(host, device_type)
            # 调用 setting_config 中的 create_device 方法添加设备
            self.db.create_device(host, device_type)

            self.tree.insert('', 'end', values=(
                host,
                device_type
            ))
            device_windows.destroy()

        ttk.Button(device_windows, text='添加', command=validate_and_add).grid(row=2, columnspan=2, pady=10)

    def delete_device(self):
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

    def log_message(self, message):
        """向控制台添加日志"""
        self.console_text.configure(state='normal')
        self.console_text.insert(tk.END, message + "\n")
        self.console_text.see(tk.END)  # 自动滚动到底部
        self.console_text.configure(state='disabled')
