import requests
from json import dumps, loads
import xmltodict
import dicttoxml
from requests.auth import HTTPBasicAuth
import tldextract
import os
from urllib.parse import urlparse

class Client:

    def __init__(self, url, service=None, request=None):

        self.request = request
        self.url = url

        self.run_service = None
        ext = tldextract.extract(url)
        path = str(urlparse(url).path).replace("/","").replace(".wsdl","")

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
            content = res.content
            with open(fp, "wb") as f:
                f.write(res.content)

        self.response = xmltodict.parse(content)
        self.prefix = "xs"
        try:
            definitions = loads(dumps(self.response))['wsdl:definitions']
            self.wsdl = "wsdl:"
            for k, v in loads(dumps(self.response))['wsdl:definitions'].items():
                if v == 'http://www.w3.org/2001/XMLSchema':
                    self.prefix = str(k).split(":")[1]
        except:
            self.wsdl = ""
            for k, v in loads(dumps(self.response))['definitions'].items():
                if v == 'http://www.w3.org/2001/XMLSchema':
                    self.prefix = str(k).split(":")[1]

        self.tns = 'xmlns:tns="' + self.soap_definitions()["@xmlns:tns"] + '"'
        self.targetNamespace = self.soap_definitions()["@targetNamespace"]

        if request == None:

            if service:
                for portType in self.soap_portType():
                    if portType["@name"] == service:
                        print("Method: \n" + str(portType[str("wsdl:input").replace("wsdl:", self.wsdl)]))
                        print("\n")
                        try:
                            self.input = portType[str("wsdl:input").replace("wsdl:", self.wsdl)]["@name"]
                            self.run_service = portType[str("wsdl:input").replace("wsdl:", self.wsdl)]["@name"]
                        except:
                            self.input = \
                            str(portType[str("wsdl:input").replace("wsdl:", self.wsdl)]["@message"]).split(":")[1]
                            self.run_service = \
                            str(portType[str("wsdl:input").replace("wsdl:", self.wsdl)]["@message"]).split(":")[1]

                if self.run_service:
                    try:
                        input_name = self.input.split(":")[1]
                    except:
                        input_name = self.input

                    try:
                        for i in self.soap_message():
                            if self.input == str(i["@name"]):
                                print("\tAttributes:\n")
                                print(i['part'])
                    except:
                        pass

                    try:
                        for k, complexType in self.soap_schema().items():
                            if 'xsd:complexType' == k:
                                for cType in complexType:
                                    if input_name == cType["@name"]:
                                        print("\tAttributes: \n" + "\t" + str(input_name))
                                        print("\t\tSub Attributes: \n" + "\t\t" + str(cType["part"]))
                                        print("\n")
                            elif 'xs:complexType' == k:
                                for cType in complexType:
                                    if input_name == cType["@name"]:
                                        print("\tAttributes: \n" + "\t" + str(input_name))
                                        print("\t\tSub Attributes: \n" + "\t\t" + str(cType["part"]))
                                        print("\n")
                            elif 's:complexType' == k:
                                for cType in complexType:
                                    if input_name == cType["@name"]:
                                        print("\tAttributes: \n" + "\t" + str(input_name))
                                        print("\t\tSub Attributes: \n" + "\t\t" + str(cType["part"]))
                                        print("\n")
                            elif 'xs:element' == k:
                                for eType in complexType:
                                    if input_name == eType["@name"]:
                                        print("\tAttributes: \n" + "\t" + str(input_name))
                                        print("\t\tSub Attributes: \n" + "\t\t" + str(
                                            eType["xs:complexType"]["xs:sequence"]["xs:element"]))
                                        print("\n")
                            elif 'xsd:element' == k:
                                for eType in complexType:
                                    if input_name == eType["@name"]:
                                        print("\tAttributes: \n" + "\t" + str(input_name))
                                        print("\t\tSub Attributes: \n" + "\t\t" + str(
                                            eType["xsd:complexType"]["xsd:sequence"]["xsd:element"]))
                                        print("\n")
                            elif 's:element' == k:
                                for eType in complexType:
                                    if input_name == eType["@name"]:
                                        print("\tAttributes: \n" + "\t" + str(input_name))
                                        print("\t\tSub Attributes: \n" + "\t\t" + str(
                                            eType["s:complexType"]["s:sequence"]["s:element"]))
                                        print("\n")
                    except:
                        pass

                    try:
                        for soap_schema in self.soap_schema():
                            for k, complexType in soap_schema.items():
                                if 'xsd:complexType' == k:
                                    for cType in complexType:
                                        if input_name == cType["@name"]:
                                            print("\tAttributes: \n" + "\t" + str(input_name))
                                            print("\t\tSub Attributes: \n" + "\t\t" + str(cType["part"]))
                                            print("\n")
                                elif 'xs:complexType' == k:
                                    for cType in complexType:
                                        if input_name == cType["@name"]:
                                            print("\tAttributes: \n" + "\t" + str(input_name))
                                            print("\t\tSub Attributes: \n" + "\t\t" + str(cType["part"]))
                                            print("\n")
                                elif 's:complexType' == k:
                                    for cType in complexType:
                                        if input_name == cType["@name"]:
                                            print("\tAttributes: \n" + "\t" + str(input_name))
                                            print("\t\tSub Attributes: \n" + "\t\t" + str(cType["part"]))
                                            print("\n")
                                elif 'xs:element' == k:
                                    for eType in complexType:
                                        if input_name == eType["@name"]:
                                            print("\tAttributes: \n" + "\t" + str(input_name))
                                            print("\t\tSub Attributes: \n" + "\t\t" + str(
                                                eType["xs:complexType"]["xs:sequence"]["xs:element"]))
                                            print("\n")
                                elif 'xsd:element' == k:
                                    for eType in complexType:
                                        if input_name == eType["@name"]:
                                            print("\tAttributes: \n" + "\t" + str(input_name))
                                            print("\t\tSub Attributes: \n" + "\t\t" + str(
                                                eType["xsd:complexType"]["xsd:sequence"]["xsd:element"]))
                                            print("\n")
                                elif 's:element' == k:
                                    for eType in complexType:
                                        if input_name == eType["@name"]:
                                            print("\tAttributes: \n" + "\t" + str(input_name))
                                            print("\t\tSub Attributes: \n" + "\t\t" + str(
                                                eType["s:complexType"]["s:sequence"]["s:element"]))
                                            print("\n")

                    except:
                        pass
                else:
                    print("Service Not Found")

            else:
                for portType in self.soap_portType():
                    print(portType["@name"])

    def soap_definitions(self):
        return loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)]

    def soap_message(self):
        return loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
            str('wsdl:message').replace("wsdl:", self.wsdl)]

    def soap_schema(self):
        if "xsd:schema" in loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
            str('wsdl:types').replace("wsdl:", self.wsdl)]:
            return loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
                str('wsdl:types').replace("wsdl:", self.wsdl)][str('xsd:schema')]
        elif "xs:schema" in loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
            str('wsdl:types').replace("wsdl:", self.wsdl)]:
            return loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
                str('wsdl:types').replace("wsdl:", self.wsdl)][str('xs:schema')]
        elif "s:schema" in loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
            str('wsdl:types').replace("wsdl:", self.wsdl)]:
            return loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
                str('wsdl:types').replace("wsdl:", self.wsdl)][str('s:schema')]

    def soap_portType(self):
        try:
            return loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
                str('wsdl:portType').replace("wsdl:", self.wsdl)][str('wsdl:operation').replace("wsdl:", self.wsdl)]
        except:
            return loads(dumps(self.response))[str('wsdl:definitions').replace("wsdl:", self.wsdl)][
                str('wsdl:portType').replace("wsdl:", self.wsdl)][0][str('wsdl:operation').replace("wsdl:", self.wsdl)]

    def send(self, username=None, password=None, **kwargs):

        if self.request:
            xml = dicttoxml.dicttoxml(kwargs)
            r = str(xml).replace('<?xml version="1.0" encoding="UTF-8" ?><root>', '').replace('</root>', '').replace(
                'type="dict"', '').replace('type="str"', '').replace('type="int"', '').replace(" ", "")

            headers = {'content-type': 'text/xml'}

            body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" """ + self.tns + """>
						 <soapenv:Header/>
						   <soapenv:Body>
						   <tns:""" + self.request + """>
									""" + r + """
									</tns:""" + self.request + """>
								   </soapenv:Body>
					  </soapenv:Envelope>"""

            if username and password:
                res = requests.post(self.url, data=body, headers=headers, auth=HTTPBasicAuth(username, password))
            else:
                res = requests.post(self.url, data=body, headers=headers)

            if res.status_code == 200:
                response = xmltodict.parse(res.content)
                return loads(dumps(response))['env:Envelope']['env:Body']
            else:
                return res.status_code