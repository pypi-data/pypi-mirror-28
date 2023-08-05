# cnfaker


## 介绍
这个工具主要用来模拟真实数据，不同于其他数据生成工具，它直接采集并存储了外网真实数据。这样的方式对中文的支持更好，用着更舒服。


## 使用方法：

### 安装:
```
pip3 install cnfaker
```

### 示例:
```
import cnfaker

print(cnfaker.name(5))

>>>> {'郑荣', '胡媛洁', '王万金', '张余晖', '李文锋'}
```


当前支持的faker：
* 姓名：cnfaker.name()
* 地址：cnfaker.address()
* 邮箱：cnfaker.email()
* 身份证号：cnfaker.ID()
* 电话：cnfaker.phone()
* 用户名：cnfaker.username()
* 句子：cnfaker.sentence()
* 段落：cnfaker.pargraph()


欢迎提issue和PR。


