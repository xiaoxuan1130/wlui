import time

from Utils import Global
from Utils.common import Common
from Utils.dbUtils import Dbutils
from Utils.interfaceUtils import InterfaceUtils
from Utils.readyaml import ReadYaml
from logger.Loggers import Loggers


class TestProductPlan():

    def test_01_query(self,login):
        common=Common(login)
        common.getLink("生产计划管理")
        common.getLink( "生产单管理")
        result=Dbutils().sqlGetPlanByRandom()
        number=result[0][0]
        productNumber = result[0][1]
        productName = result[0][2]
        className="ikas-form-box flex-start"
        common.getInputByClass(className,"产品名称",productName)
        common.getSelectByClass(className,"生产单号",number)
        common.getSelectByClass(className, "产品物料编码", productNumber)
        common.getButtonByClass("ikas-btns","查询")
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
        common.queryByConditions(list_key,list_value,xpath)

    def test_02_add(self,login):
        time.sleep(1)
        currentDate = login.__getattribute__("get-date")
        value = login.__getattribute__("value")
        cookies = login.get_cookie("huawei-Token")
        #生产单中的辅料列表构建
        components=[]
        #调用接口新建材料
        materialAddress = ReadYaml.readYaml("interface_url", "mes-api-erp_materials")
        for num in range(1,6):
            n=currentDate+"_"+str(num)
            param={
                "name":str(Global.materialName+n),
                "number":str(Global.materialNumber+n),
                "specification":str(Global.specification+n),
                "description":"描述",
                "supplier":str(Global.materialSupplier+n),
                "attribute":"属性",
                "shelf_life":"2",
                "shelf_life_unit":"月",
                "min_unit":"pcs",
                "secret_key":str(Global.secretKey)
            }
            component={
                "row_number":"1",
                "material_number":str(Global.materialNumber+n),
                "use_qty":"1000",
                "molecule_qty":"1",
                "denominator_qty":"1"
            }
            components.append(component)
            InterfaceUtils(cookies, materialAddress).addItem(1, param)
        #调用接口新建产品
        n=currentDate+value
        param = {
            "name": str(Global.productName + n),
            "number": str(Global.productNumber + n),
            "specification": str(Global.specification + n),
            "description": "描述",
            "supplier": str(Global.materialSupplier + n),
            "attribute": "属性",
            "shelf_life": "2",
            "shelf_life_unit": "月",
            "min_unit": "pcs",
            "secret_key": str(Global.secretKey)
        }
        InterfaceUtils(cookies, materialAddress).addItem(1, param)
        #调用接口新建生产单
        date=Common.getCurrentDate("")
        leadTime=Common.getDateDiff(7)
        json={
            "number":str(Global.planNo+currentDate+value),
            "date":str(date),
            "biz_type":"汇报入库-普通生产",
            "workshop":"生产部-绑定",
            "material_number":str(Global.productNumber+currentDate+value),
            "total":"1000",
            "start_time":str(date),
            "end_time":str(leadTime),
            "lead_time":str(leadTime),
            "remark":"备注"+value,
            "components":components,
            "secret_key":str(Global.secretKey)
        }
        address=ReadYaml.readYaml("interface_url","mes-api-erp_manufacture_orders")
        re=InterfaceUtils(cookies,address).addItem(1,json)

    def test_queryMaterialList(self,login):
        common = Common(login)
        currentDate = login.__getattribute__("get-date")
        value = login.__getattribute__("value")
        common.getLink("生产计划管理")
        common.getLink("生产单管理")
        className = "ikas-form-box flex-start"
        common.getSelectByClass( className, "生产单号", str(Global.planNo+currentDate+value))
        common.getButtonByClass("ikas-btns", "查询")
        time.sleep(1)
        xpath = '//table[@class="el-table__body"]//tr'
        common.queryByConditions([1],[str(Global.planNo+currentDate+value)],xpath)
        common.getTableButton("生产用料清单")
        text=common.getSelectValue("ikas-form-box flex-start","生产单号")
        assert str(Global.planNo+currentDate+value)==text

    def test_finish(self,login):
        currentDate = login.__getattribute__("get-date")
        value = login.__getattribute__("value")
        common=Common(login)
        common.getLink("生产计划管理")
        common.getLink("生产单管理")
        className = "ikas-form-box flex-start"
        common.getSelectByClass(className, "生产单号", str(Global.planNo + currentDate + value))
        common.getButtonByClass("ikas-btns", "查询")
        time.sleep(1)
        xpath = '//table[@class="el-table__body"]//tr'
        common.queryByConditions( [1], [str(Global.planNo + currentDate + value)], xpath)
        common.getTableButton( "标记已完成")
        common.getDialogButton("dialog","确定")

