import requests

a = requests.get("https://localhost/", 
                 cert=('/etc/nginx/client.crt', '/etc/nginx/client.key'), 
                 verify=False)
print(a)
