import tkinter as tk
from tkinter import messagebox
from setting_config import config_data as setting
import netconf_session as ncs
from tkinter import ttk

button_list = ['设置BD域', '设置vni', '设置环回口地址范围', '添加网络设备']
action_buttons = []

class netconfapp_gui:
    def __init__(self, root):
        self.root = root
        self.root.title('初代python控制器')
        self.root.geometry('800x600')
        # 确保在 __init__ 方法中正确初始化 setting 属性
        self.setting = setting()
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
        ]  # 设置输入框的变量


        for (start_var, end_var), (label_text, frame) in zip(input_vars, [
            ('输入BD域的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入VNI的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
            ('输入vlan的起始值,如不输入将采用默认值1_100', tk.Frame(config_window)),
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

            setting().BD(bd_start, bd_end)
            setting().vni(vni_start, vni_end)
            setting().vlan(vlan_start, vlan_end)
            # 关闭窗口
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
            # 调用 setting_config 中的 create_device 方法添加设备
            self.setting.create_device(host, device_type)

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
            self.setting.delete_device(host)
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

# if __name__ == '__main__':
#     netconfapp_gui(4).refresh_device_list()
#     netconfapp_gui(4).refresh_device_list()