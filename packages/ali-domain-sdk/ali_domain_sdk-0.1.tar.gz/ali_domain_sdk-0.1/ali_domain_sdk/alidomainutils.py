from urllib.parse import quote
from hashlib import sha1
import datetime
import hmac
import base64
import requests
import random

SEPARATOR = "&"


class AliAuthInfo:
    def __init__(self, accessKeyId, accessKeySecret, domainName):
        self.accessKeyId = accessKeyId
        self.accessKeySecret = accessKeySecret
        self.domainName = domainName


class DomainRecordType:
    A = "A"
    NS = "NS"
    MX = "MX"
    TXT = "TXT"
    CNAME = "CNAME"
    SRV = "SRV"
    AAAA = "AAAA"
    CAA = "CAA"
    REDIRECT_URL = "REDIRECT_URL"
    FORWARD_URL = "FORWARD_URL"


class AliDomainRecord:
    def __init__(self,
                 RecordId,
                 RR=None,
                 Type=None,
                 Value=None,
                 DomainName=None,
                 TTL=None,
                 Priority=None,
                 Line=None,
                 Status=None,
                 Locked=None,
                 Weight=None):
        self.RecordId = RecordId
        self.RR = RR
        self.Type = Type
        self.Value = Value
        self.DomainName = DomainName
        self.TTL = TTL
        self.Priority = Priority
        self.Line = Line
        self.Status = Status
        self.Locked = Locked
        self.Weight = Weight

    def update(self, aliAuthInfo):
        parameters = geneateDefaultParmeters(aliAuthInfo)
        parameters["Action"] = "UpdateDomainRecord"
        parameters["RecordId"] = self.RecordId
        parameters["RR"] = self.RR
        parameters["Type"] = self.Type
        parameters["Value"] = self.Value
        if self.TTL != None: 
            parameters["TTL"] = self.TTL
        if self.Priority != None: 
            parameters["Priority"] = self.Priority
        if self.Line != None: 
            parameters["Line"] = "Line"
        
        return sendRequest(parameters,aliAuthInfo).text

def percentEncode(url):
    url = quote(
        url, encoding="UTF-8", safe='-_.~').replace("+", "%20").replace(
            "*", "%2A").replace("%7E", "~")
    return url


def getTimestamp():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def getSignature(aliAuthInfo, parameters, httpMethod):
    keys = list(parameters.keys())
    keys.sort()

    stringToSign = httpMethod + SEPARATOR + percentEncode("/") + SEPARATOR

    canonicalizedQueryString = ""
    for key in keys:
        canonicalizedQueryString += "&"
        canonicalizedQueryString += (percentEncode(key) + "=")
        canonicalizedQueryString += (percentEncode(parameters[key]))
    stringToSign += percentEncode(canonicalizedQueryString[1:])

    digest = hmac.new((aliAuthInfo.accessKeySecret + "&").encode(),
                      stringToSign.encode(), sha1).digest()
    signature = base64.b64encode(digest).decode("utf-8")
    return signature


def sendRequest(parameters, aliAuthInfo, httpMethod="GET"):
    parameters["Signature"] = getSignature(aliAuthInfo, parameters, httpMethod)
    if (httpMethod == "GET"):
        return requests.get("https://alidns.aliyuncs.com/", params=parameters)
    else:
        return requests.post("https://alidns.aliyuncs.com/", data=parameters)


def geneateDefaultParmeters(aliAuthInfo, format="JSON"):
    parameters = {
        "Format": format,
        "Version": "2015-01-09",
        "AccessKeyId": aliAuthInfo.accessKeyId,
        "SignatureMethod": "HMAC-SHA1",
        "Timestamp": getTimestamp(),
        "SignatureVersion": "1.0",
        "SignatureNonce": str(random.randrange(1, 100000))
    }
    return parameters


def getDomainRecords(aliAuthInfo, format="JSON"):
    timestamp = getTimestamp()
    parameters = geneateDefaultParmeters(aliAuthInfo, format)
    parameters["Action"] = "DescribeDomainRecords"
    parameters["DomainName"] = aliAuthInfo.domainName
    return (sendRequest(parameters, aliAuthInfo).text)
