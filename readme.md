# 基于requests模块多进程下载图片的爬虫demo

(受一个不愿意透露姓名的朋友委托制作的)

## 依赖的模块

- sys
- os
- requests
- lxml.etree
- multiprocessing.Pool

## 用法

`re_catch.py [option]`

必须在接受参数才能启动，目前可接受的options:

- `card` : 获取公主链接卡面
- `title_bg`: 获取bangbang主题背景

## 示例

在终端中输入如下命令：

```shell
python re_catch.py card
```

运行后会在当前目录生成对应的文件夹，保存获取的图片

![pic_01](https://cdn.jsdelivr.net/gh/Dqz00116/pic//img/20210509173749.png)

P.S.每次运行后都可以覆盖更新，隔段时间运行一下就可以了
