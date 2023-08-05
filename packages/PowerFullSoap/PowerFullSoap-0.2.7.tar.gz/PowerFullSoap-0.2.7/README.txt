Getting Started

Install:

pip install PowerFullSoap

Methods:

from PowerFullSoap.Soap import Client

print(Client(url))

Attributes:

attr = Client(url, 'Method name')
print(attr)

Request:

response = Client(url, 'Method name', 'Request name').send(**attributes)

Authentication Request:

response = Client(url, 'Method name', 'Request name').send(username, password, **attributes)