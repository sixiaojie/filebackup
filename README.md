# 多进程 多目录备份

## 使用方式


在config.py中可配置多个备份，并发执行。

name: 此次备份的名字

delete: 如果备份文件存在是否覆盖。 属于本次任务全局变量

执行： python filebackup.py backup
