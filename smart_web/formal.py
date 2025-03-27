from setting_config import config_data as resource
import tkinter as tk
from GUI import netconfapp_gui

if __name__ == '__main__':
    root = tk.Tk()
    app = netconfapp_gui(root)
    # 假设这里有一个按钮绑定了 get_input_values 方法
    # 确保正确调用
    # button = tk.Button(root, text="Get Values", command=app.get_input_values)
    # button.pack()
    # root.mainloop()