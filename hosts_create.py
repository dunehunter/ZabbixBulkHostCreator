import requests
import xml.etree.ElementTree as ET

# Zabbix API URL
zabbix_api_url = "http://10.15.102.166/zabbix/api_jsonrpc.php"

# Login credentials
login_data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {"user": "Admin", "password": "zabbix"},
    "id": 1
}

# Post request to get auth token
response = requests.post(zabbix_api_url, json=login_data).json()
auth_token = response.get('result')

def find_text_or_empty(xml_element, tag_name):
    return xml_element.find(tag_name).text if xml_element.find(tag_name) is not None else ''

def parse_hosts_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    hosts = []
    for host_elem in root.findall('host'):
        host_info = {
            'host': host_elem.find('host_name').text,
            'interfaces': [],
            'templates': [],
            'groups': []
        }
        # Parse interfaces
        for interface_elem in host_elem.findall('interfaces/interface'):
            interface = {
                'type': int(interface_elem.find('type').text),
                'main': int(interface_elem.find('main').text),
                'useip': int(interface_elem.find('useip').text),
                'ip': interface_elem.find('ip').text,
                'port': interface_elem.find('port').text,
                'dns': ''
            }
            # Add SNMP details if present
            if interface['type'] == 2:
                details_elem = interface_elem.find('details')
                interface['details'] = {
                    'version': int(details_elem.find('version').text),
                    'bulk': int(details_elem.find('bulk').text),
                    'securityname': details_elem.find('securityname').text,
                    'securitylevel': int(details_elem.find('securitylevel').text),
                    'authprotocol': int(details_elem.find('authprotocol').text),
                    'authpassphrase': details_elem.find('authpassphrase').text,
                    'privprotocol': int(details_elem.find('privprotocol').text),
                    'privpassphrase': details_elem.find('privpassphrase').text,
                }
            host_info['interfaces'].append(interface)

        # Parse templates
        for template_elem in host_elem.findall('templates/template'):
            templateid = template_elem.find('templateid').text
            host_info['templates'].append({
                'templateid': templateid
            })

        # Parse groups
        for group_elem in host_elem.findall('groups/group'):
            groupid = int(group_elem.find('groupid').text)
            host_info['groups'].append({
                'groupid': groupid
            })

        hosts.append(host_info)
    return hosts

# XML file path
xml_file_path = 'hosts.xml'  # Replace with the path to your XML file

# Read host data from XML file
hosts_data = parse_hosts_from_xml(xml_file_path)

# Create each host with its interfaces
for host in hosts_data:
    create_host_request = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": host['host'],
            "interfaces": host['interfaces'],
            "templates": host['templates'],
            "groups": host['groups'],
            "ipmi_username":"sysadmin",
            "ipmi_password":"Dm-12345678"
        },
        "auth": auth_token,
        "id": 1
    }
    create_host_response = requests.post(zabbix_api_url, json=create_host_request).json()
    if 'error' in create_host_response:
        print(f"Error creating host {host['host']}: {create_host_response['error']}")
    else:
        print(f"Host {host['host']} created successfully")
