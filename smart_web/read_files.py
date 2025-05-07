import json,os

class readfile:
    def __init__(self):
        self.hostlist = self.__read('host.json')
        self.reslist = self.__read('res.json')
        self.templist = self.__read('temp.json')

    def write(self, data:dict):
        # 以写入模式打开文件，指定编码为 utf-8
        if not os.path.exists('temp'):
            os.mkdir('temp')
        with open(r'temp/temp.json', 'w', encoding='utf-8') as f:
            # 将 Python 字典数据写入 JSON 文件
            json.dump(data, f, ensure_ascii=False, indent=4)

    def wirte_res(self,data):
        if not os.path.exists('temp'):
            os.mkdir('temp')
        with open(r'temp/res.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def write_host(self,data):
        files_name = r'temp/host.json'
        existing_data = {}
        # 以写入模式打开文件，指定编码为 utf-8,需要保证这个空字典存在
        if not os.path.exists(files_name):
            with open(files_name, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                #判断路径下是否有host.json文件,如果没有就创建一个,
                # 如果有就读取文件,并将新的数据写入文件中
        existing_data.update(data)
        with open(files_name, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
        

    def __read(self,files_name:str):
        # 以读取模式打开文件，指定编码为 utf-8
                # 以读取模式打开文件，指定编码为 utf-8
        path = os.path.join(r'temp', files_name)
        if not os.path.exists(path):
            # 确保 temp 目录存在
            temp_dir = os.path.dirname(path)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            # 创建文件并写入空的 JSON 对象
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({}, f)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {}
            try:
                # 读取 JSON 文件内容并解析为 Python 字典
                data = json.loads(content)
            except json.JSONDecodeError:
                return {}
        return data
    
    def detlete(self,keys:str):
        # 删除指定JSON文件中的键值对
        hostlist = self.hostlist
        if keys in self.hostlist:
            del hostlist[keys]
        # 将更新后的数据写回文件
        with open(r'temp/host.json','w',encoding='utf-8') as f:
            json.dump(hostlist,f,ensure_ascii=False,indent=4)


# 创建 readfile 类的实例