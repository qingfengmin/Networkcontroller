import mysql.connector

class reamysql:
    def __init__(self):
        self.user = {
            'host': 'localhost',
            'user': 'root',
            'password': '123456',
            'database': 'route'
        }
        self.table = 'devices_resource'

    def __connect(self):
        mydb = mysql.connector.connect(**self.user)
        return mydb

    def create(self,revice_id):
        client = self.__connect()
        cursor = client.cursor()
        sql = f'INSERT INTO {self.table} (control_id) VALUE ({revice_id})'
        cursor.execute(sql)
        client.commit();cursor.close();client.close()

    def update_resource(self,data_type,data_key,revice_id):
        client = self.__connect()
        cursor = client.cursor()
        sql = f'UPDATE {self.table} SET {data_type} = {data_key} WHERE control_id = {revice_id};'
        print(sql)
        cursor.execute(sql)
        client.commit();cursor.close();client.close()

    def update_resource_str(self,data_type,data_key,revice_id):
        client = self.__connect()
        cursor = client.cursor()
        sql = f'UPDATE {self.table} SET {data_type} = "{data_key}" WHERE control_id = {revice_id}'
        cursor.execute(sql)
        client.commit();cursor.close();client.close()

    def read(self,receive_id,type):
        client = self.__connect()
        cursor = client.cursor()
        sql = f"SELECT {type} FROM {self.table} WHERE control_id = {receive_id}"
        cursor.execute(sql)
        result = cursor.fetchall()
        client.commit();cursor.close();client.close()
        return result[0][0]

    def read_all(self):
        client = self.__connect()
        cursor = client.cursor()
        sql = f'SELECT * FROM {self.table}'
        cursor.execute(sql)
        result = cursor.fetchall()
        names = [i[0] for i in cursor.description]
        for row in result:
            print(dict(zip(names, row)))
        client.commit();cursor.close();client.close()

    def create_user(self,username,password):
        client = self.__connect()
        cursor = client.cursor()
        sql = f'INSERT INTO user_info (username,password) VALUE ("{username}","{password}")'
        cursor.execute(sql)
        client.commit();cursor.close();client.close()

    def update_user(self,username,password):
        client = self.__connect()
        cursor = client.cursor()
        sql = f'UPDATE user_info SET password = "{password}" WHERE username = "{username}"'
        cursor.execute(sql)
        client.commit();cursor.close();client.close()

    def read_user_password(self,username):
        client = self.__connect()
        cursor = client.cursor()
        sql = f'SELECT password FROM user_info WHERE username = "{username}"'
        cursor.execute(sql)
        result = cursor.fetchall()
        client.commit();cursor.close();client.close()
        return result[0][0]

if __name__ == '__main__':
    a = reamysql()
    # kunhua = a.read('1','vlan_after')
    # kunhua1 = a.update_resource_str('ip_address','10.1.200.0/24',1)
    # # print(kunhua)
    kunhua = a.create_user('kunhua','123456')

