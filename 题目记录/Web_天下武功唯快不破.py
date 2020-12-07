import requests
import base64

r = requests.post('http://ctf5.shiyanbar.com/web/10/10.php')

key = r.headers['FLAG']

flag = base64.b64decode(key).decode().split(':')[1]

para = {'key':flag}

r = requests.post('http://ctf5.shiyanbar.com/web/10/10.php',data = para)

print(r.text)
input('以上为题目答案')
