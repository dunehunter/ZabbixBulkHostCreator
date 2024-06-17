import requests
import json

# Zabbix API的URL
zabbix_api_url = "http://10.15.102.166/zabbix/api_jsonrpc.php"

# 第一步：登录Zabbix API获取Token
login_data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {"user": "Admin", "password": "zabbix"},
    "id": 1
}

response = requests.post(zabbix_api_url, json=login_data).json()
auth_token = response.get('result')

# 第二步：获取所有模板的列表
get_templates_params = {
    "output": "extend",
    "selectHosts": "refer"
}
get_templates_data = {
    "jsonrpc": "2.0",
    "method": "template.get",
    "params": get_templates_params,
    "auth": auth_token,
    "id": 2
}

templates_response = requests.post(zabbix_api_url, json=get_templates_data).json()
templates = templates_response.get('result', [])

# 打印模板列表
for template in templates:
    print(f"Template Name: {template['name']}, Template ID: {template['templateid']}")

# 第三步：获取所有主机组的列表
get_groups_params = {
    "output": "extend"
}
get_groups_data = {
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": get_groups_params,
    "auth": auth_token,
    "id": 3
}

groups_response = requests.post(zabbix_api_url, json=get_groups_data).json()
groups = groups_response.get('result', [])

# 打印主机组列表
for group in groups:
    print(f"Group Name: {group['name']}, Group ID: {group['groupid']}")
