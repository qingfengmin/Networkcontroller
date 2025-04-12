from urllib.request import urlopen

url = 'http://www.baidu.com'
res = urlopen(url)
# html = res.read()
#
# print(html.decode('gbk'))

with open(r'C:\Users\Administrator\Downloads\Programs\niu.html', 'w') as f:
    f.write(res.read().decode('utf-8'))
# print(f)
