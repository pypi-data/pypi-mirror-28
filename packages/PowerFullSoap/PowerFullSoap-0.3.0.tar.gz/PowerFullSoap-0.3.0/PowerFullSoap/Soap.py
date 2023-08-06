import requests
from json import dumps, loads
import xmltodict
import dicttoxml
from requests.auth import HTTPBasicAuth
import tldextract
import os
from urllib.parse import urlparse
from lxml import etree

class Client:

	def __init__(self, url, service=None, request=None):

		types = ["xs:long","s:long","xsd:long","xs:string",
				"s:string","xsd:string","xs:integer","s:integer",
				"xsd:integer","xs:decimal","s:decimal","xsd:decimal",
				"xs:boolean","s:boolean","xsd:boolean",
				"xs:int","s:int","xsd:int","xs:str","s:str","xsd:str",
				"xs:bool","s:bool","xsd:bool",
				"xs:stringArray","s:stringArray","xsd:stringArray",
				"xs:intArray","s:intArray","xsd:intArray",
				"xs:integerArray","s:integerArray","xsd:integerArray",
				"xs:strArray","s:strArray","xsd:strArray"]

		self.request = request
		self.url = url

		self.run_service = None
		ext = tldextract.extract(url)
		path = str(urlparse(url).path).replace("/","").replace(".wsdl","").replace("?wsdl","")

		fp_ = str(ext.domain) + str(path) + str(".xml")
		cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

		try:
			os.stat(cache)
		except:
			os.mkdir(cache)

		fp = str(os.path.join(cache, fp_))

		try:
			fopen = open(fp, "rb")
			content = fopen.read()
		except:
			res = requests.get(self.url)
			with open(fp, "wb") as f:	
				content = res.content
				f.write(res.content)
			
		
		tree = etree.fromstring(content)
		namespaces = tree.nsmap

		namespaces.setdefault("xs","http://www.w3.org/2001/XMLSchema")
		namespaces.setdefault("xsd","http://www.w3.org/2001/XMLSchema")
		namespaces.setdefault("s","http://www.w3.org/2001/XMLSchema")
		try:
			definitions = tree.xpath("//wsdl:definitions", namespaces=namespaces)
		except:
			definitions = tree.xpath("//definitions")
		for d in definitions:
			self.tns = d.attrib['targetNamespace']

		RequestDict = {}

		#Methodlar çekiliyor
		try:
			portType = tree.xpath("//wsdl:portType/wsdl:operation", namespaces=namespaces)
		except:
			portType = tree.xpath("//portType/operation")

		methods = []

		for p in portType:
			MethodName = p.attrib['name']
			methods.append(MethodName)
			try:
				input_name = tree.xpath("//wsdl:portType/wsdl:operation[@name=\""+p.attrib['name']+"\"]/wsdl:input", namespaces=namespaces)
			except:
				input_name = tree.xpath("//portType/operation[@name=\""+p.attrib['name']+"\"]/input")
			
			if MethodName == service:
				for i in input_name:
					try:
						RequestName = i.attrib['name']
					except:
						RequestName = str(i.attrib['message']).split(":")[1]

					#RequestDict.setdefault(RequestName,{})
					#print(RequestName)
					try:
						message = tree.xpath("//wsdl:message[@name=\""+RequestName+"\"]/wsdl:part", namespaces=namespaces)
					except:
						message = tree.xpath("//message[@name=\""+RequestName+"\"]/part")

					for m in message:
						t = m.attrib["name"]
						
						try:
							elem = m.attrib["element"]
						except:
							elem = m.attrib["name"]
						
						if 'type' in m.attrib:
							RequestDict.setdefault(m.attrib["name"],m.attrib["type"])

						if not t in types:
							RequestDict.setdefault(elem,{})
							element = tree.xpath("//xs:element[@name=\""+str(t)+"\"]/xs:complexType/xs:sequence/xs:element", namespaces=namespaces)
							for e in element:
								if not e.attrib["type"] in types:
									RequestDict[elem].setdefault(e.attrib["name"],{})
									complexType = tree.xpath("//xs:complexType[@name=\""+str(e.attrib["type"]).split(":")[1]+"\"]/xs:sequence/xs:element", namespaces=namespaces)
									for c2 in complexType:
										if not c2.attrib["type"] in types:
											RequestDict[elem][e.attrib["name"]].setdefault(c2.attrib["name"],{})
											complexType = tree.xpath("//xs:complexType[@name=\""+str(c2.attrib["type"]).split(":")[1]+"\"]/xs:sequence/xs:element", namespaces=namespaces)
											for c3 in complexType:
												if not c3.attrib["type"] in types:
													RequestDict[elem][e.attrib["name"]][c2.attrib["name"]].setdefault(c3.attrib["name"],{})
													complexType = tree.xpath("//xs:complexType[@name=\""+str(c3.attrib["type"]).split(":")[1]+"\"]/xs:sequence/xs:element", namespaces=namespaces)
													for c4 in complexType:
														if not c4.attrib["type"] in types:
															RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]].setdefault(c4.attrib["name"],{})
															complexType = tree.xpath("//xs:complexType[@name=\""+str(c4.attrib["type"]).split(":")[1]+"\"]/xs:sequence/xs:element", namespaces=namespaces)
															for c5 in complexType:
																if not c5.attrib["type"] in types:
																	RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]][c4.attrib["name"]].setdefault(c5.attrib["name"],{})
																	complexType = tree.xpath("//xs:complexType[@name=\""+str(c5.attrib["type"]).split(":")[1]+"\"]/xs:sequence/xs:element", namespaces=namespaces)	
																	for c6 in complexType:
																		if not c6.attrib["type"] in types:
																			RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]][c4.attrib["name"]][c5.attrib["name"]].setdefault(c6.attrib["name"],{})
																			complexType = tree.xpath("//xs:complexType[@name=\""+str(c6.attrib["type"]).split(":")[1]+"\"]/xs:sequence/xs:element", namespaces=namespaces)	
																			for c7 in complexType:
																				if not c7.attrib["type"] in types:
																					RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]][c4.attrib["name"]][c5.attrib["name"]][c6.attrib["name"]].setdefault(c7.attrib["name"],{})
																					complexType = tree.xpath("//xs:complexType[@name=\""+str(c7.attrib["type"]).split(":")[1]+"\"]/xs:sequence/xs:element", namespaces=namespaces)	
																				else:
																					RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]][c4.attrib["name"]][c5.attrib["name"]][c6.attrib["name"]].setdefault(c7.attrib["name"],c7.attrib["type"])
																		else:
																			RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]][c4.attrib["name"]][c5.attrib["name"]].setdefault(c6.attrib["name"],c6.attrib["type"])
																else:
																	RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]][c4.attrib["name"]].setdefault(c5.attrib["name"],c5.attrib["type"])

														else:
															RequestDict[elem][e.attrib["name"]][c2.attrib["name"]][c3.attrib["name"]].setdefault(c4.attrib["name"],c4.attrib["type"])
												else:
													RequestDict[elem][e.attrib["name"]][c2.attrib["name"]].setdefault(c3.attrib["name"],c3.attrib["type"])
										else:
											RequestDict[elem][e.attrib["name"]].setdefault(c2.attrib["name"],c2.attrib["type"])
								else:
									RequestDict[elem].setdefault(e.attrib["name"],e.attrib["type"])

		self.service = service
		self.RequestDict = dumps(RequestDict,indent=4)
		self.methods = dumps(methods,indent=4)

	def __str__(self):
		if self.service:
			return '%s' % self.RequestDict
		else:
			return '%s' % self.methods

	def post(self, data, username=None, password=None):
		for k,v in data.items():
			key= k
			values = v
		xml = dicttoxml.dicttoxml(values)
		r = str(xml).replace('<?xml version="1.0" encoding="UTF-8" ?><root>', '').replace('</root>', '').replace(
			'type="dict"', '').replace('type="str"', '').replace('type="int"', '').replace(" ", "")

		headers = {'content-type': 'text/xml'}

		body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns=\"""" + self.tns + """\">
					 <soapenv:Header/>
					   <soapenv:Body>
					   	<"""+key+""">
							""" + r + """
						</"""+key+""">
						</soapenv:Body>
				  </soapenv:Envelope>"""
		print(body)
		if username and password:
			res = requests.post(self.url, data=body, headers=headers, auth=HTTPBasicAuth(username, password))
		else:
			res = requests.post(self.url, data=body, headers=headers)

		if res.status_code == 200:
			response = xmltodict.parse(res.content)
			return loads(dumps(response))['env:Envelope']['env:Body']
		else:
			return res.status_code