import http.client

conn = http.client.HTTPSConnection("api.airvisual.com")
payload = ''
headers = {}
conn.request("GET", "/v2/city?city=Los%20Angeles&state=California&country=USA&key=4217e686-4099-4071-b670-5664769faaad", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))