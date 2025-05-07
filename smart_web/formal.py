import tkinter as tk
from GUI import netconfapp_gui
from app import controller,tips
import threading

def start_gui():
    root = tk.Tk()
    app = netconfapp_gui(root)
    # 启动 GUI 主循环
    root.mainloop()


def start_web_controller():
    kun = controller()
    # 因为需要同时运行 GUI 和 Flask，所以这里使用了多线程, 其中 debug=False 表示不开启调试模式
    kun.app.run(debug=False)


if __name__ == "__main__":
    # 创建并启动 GUI 线程
    tips()
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()

    # 创建并启动网页版控制器线程
    web_thread = threading.Thread(target=start_web_controller)
    web_thread.start()
    