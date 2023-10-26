import requests

response = requests.get("https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key=8353d1f11aa2efca9cf2e2b555cda111507b17af&host=awdarma.uz")
response = response.json()
print(response)