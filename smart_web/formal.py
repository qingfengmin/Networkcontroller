import tkinter as tk

action_buttons = []
button_list = ['设置BD域','设置vni','设置环回口地址范围','添加网络设备']

class netconfapp_gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('初代python控制器')
        self.root.geometry('800x600')
        self.design()
        self.Centralized_gateway()
        self.show_buttons()
        self.root.mainloop()

        self.contralized = None

    def design(self):
        self.root.config(background='#38D3ED')

        infor1 = tk.Label(self.root,text='初代控制器,目前只能使用VXlan集中式网关',bg='red',fg='white')
        infor1.pack()

        infor2 = tk.Label(self.root,text='请添加网络设备',bg='green',fg='white')
        infor2.pack()

        for i in button_list:
            button2 = tk.Button(self.root,text=i,bg='green',fg='white')
            action_buttons.append(button2)

    def Centralized_gateway(self):
        self.contralized = tk.IntVar()
        self.checkbutton = tk.Checkbutton(self.root,text='集中式网关',variable=self.contralized,command=self.show_buttons)
        self.checkbutton.pack()

    def show_buttons(self):
        if self.contralized.get():
            for button in action_buttons:
                button.pack()
        else:
            for button in action_buttons:
                button.pack_forget()

if __name__ == '__main__':
    app = netconfapp_gui()