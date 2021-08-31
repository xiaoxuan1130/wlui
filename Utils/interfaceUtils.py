import requests

from Utils.readyaml import ReadYaml


class InterfaceUtils():
    def __init__(self,cookies,address):
        url=ReadYaml.readYaml("url","host")
        self.url=url+address
        headers={"Authorization":cookies.get("value")}
        self.headers=headers

    def addItem(self,type,json):
        re=""
        if type==1:
            re=requests.post(self.url,headers=self.headers,json=json)
        else:
            re=requests.put(self.url, headers=self.headers, json=json)
        return re