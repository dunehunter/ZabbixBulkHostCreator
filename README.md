# Zabbix Bulk Host Creater

这是一个Python脚本，用于为Zabbix监控系统中的主机批量添加模板。该脚本使用Zabbix API进行操作。

## 先决条件
- Python 3.x
- `requests` 库（可通过 `pip install requests` 安装）
- 有效的Zabbix API访问权限

## 使用方法
1. **安装依赖**：
   确保Python环境已安装`requests`库。
   ```bash
   pip install requests
配置脚本：
编辑脚本文件，替换以下占位符为实际值：
```
zabbix_api_url：您的Zabbix服务器地址。
user：您的Zabbix用户名。
password：您的Zabbix密码。
```
编辑hosts.xml，格式参照已有的模板，在命令行中运行Python脚本：
```bash
python hosts_create.py
```
XML输入格式说明:
```
<hosts>：根元素，包含所有主机的列表。
<host>：每个主机的容器。
<host_name>：主机的名称。
<interfaces>：定义主机接口。
<type>：定义接口类型，1=Zabbix Agent, 2=SNMP, 3=IPMI。
<templateid>：Zabbix模板的ID。
<groupid>：Zabbix组ID。
```
