import time

from Utils import Global
from Utils.common import Common
from Utils.dbUtils import Dbutils
from Utils.interfaceUtils import InterfaceUtils
from Utils.readyaml import ReadYaml


class TestProductPlan():

    def test_01_query(self,login):
        Common.getLink(login,"生产计划管理")
        Common.getLink(login, "生产单管理")
        result=Dbutils().sqlGetPlanByRandom()
        number=result[0][0]
        productNumber = result[0][1]
        productName = result[0][2]
        className="ikas-form-box flex-start"
        Common.getInputByClass(login,className,"产品名称",productName)
        Common.getSelectByClass(login,className,"生产单号",number)
        Common.getSelectByClass(login,className, "产品物料编码", productNumber)
        Common.getButtonByClass(login,"ikas-btns","查询")
        time.sleep(1)
        list_key=[]
        list_key.append(1)
        list_key.append(5)
        list_key.append(6)
        list_value=[]
        list_value.append(number)
        list_value.append(productNumber)
        list_value.append(productName)
        xpath='//table[@class="el-table__body"]//tr'
        Common.queryByConditions(login,list_key,list_value,xpath)

    def test_02_add(self,login):
        Common.getLink(login, "生产计划管理")
        Common.getLink(login, "生产单管理")
        value=login.__getattribute__("value")
        date=Common.getCurrentDate("")
        leadTime=Common.getDateDiff(7)
        json={
            "number":str(Global.planNo+value),
            "date":str(date),
            "biz_type":"汇报入库-普通生产",
            "workshop":"生产部-绑定",
            "material_number":str(Global.productNumber+value),
            "total":"1000",
            "start_time":str(date),
            "end_time":str(leadTime),
            "lead_time":str(leadTime),
            "remark":"tongnm test",
            "components":[
                {
                    "row_number":"1",
                    "material_number":str(Global.materialNumber)+value,
                    "use_qty":"1000",
                    "molecule_qty":"1",
                    "denominator_qty":"1"
                }
            ],
            "secret_key":str(Global.secretKey)
        }
        cookies=login.get_cookie("huawei-Token")
        address=ReadYaml.readYaml("interface_url","mes-api-erp_manufacture_orders")
        InterfaceUtils(cookies,address).addItem(1,json)