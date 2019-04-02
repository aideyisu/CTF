
import re
import requests
 
s = requests.Session()
r = s.get("http://123.206.87.240:8002/qiumingshan/")
searchObj = re.search(r'^<div>(.*)=\?;</div>$', r.text, re.M | re.S)
d = {
    "value": eval(searchObj.group(1))
}
r = s.post("http://123.206.87.240:8002/qiumingshan/", data=d)
print(r.text)
