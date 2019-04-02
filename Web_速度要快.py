import requests
import base64
 
url = 'http://123.206.87.240:8002/web6/'
req = requests.session()
res = req.get(url)
flag = res.headers['flag']
 
txt = base64.b64decode(flag)
txt = txt[encode(txt.index(":"))+2:]
txt = base64.b64decode(txt)
 
data = {'margin': txt}
ans = req.post(url, data)
print (ans.content)
