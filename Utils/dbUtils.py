import pymysql as pymysql

from Utils.readyaml import ReadYaml

class Dbutils():
    def __init__(self):
        self.connect = pymysql.Connect(
            host= ReadYaml.readYaml("sql","host"),
            port=3306,
            user=ReadYaml.readYaml("sql","user"),
            passwd=str(ReadYaml.readYaml("sql","passwd")),
            db=ReadYaml.readYaml("sql","db"),
            charset='utf8'
        )
        self.cursor = self.connect.cursor()


    def getResult(self,sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # 关闭连接
        self.cursor.close()
        self.connect.close()
        return result

    def sqlGetPlanByRandom(self):
        sql="select o.number,m.number,m.name from tb_manufacture_order o left join tb_warehouse_raw_material m on o.material_id=m.id ORDER BY RAND() limit 1"
        return Dbutils().getResult(sql)
