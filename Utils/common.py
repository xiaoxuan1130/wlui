import datetime
import time

#公共类
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Utils.readyaml import ReadYaml


def getDate():
    return time.strftime('%Y%m%d', time.localtime(time.time()))

def getRandom():
    return '1'

class Common():

    def __init__(self,driver):
        self.driver=driver

    def getCurrentDate(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    def getDateDiff(day):
        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=day)
        return yes_time.strftime('%Y-%m-%d')

    def getName(key):
        key=ReadYaml.realVarYaml(key)
        return key+"_"+getDate()+"_"+getRandom()

    def getDriver(self,path):
        WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, path)))
        return self.driver.find_element_by_xpath(path)

    def getDrivers(self,path):
        #return WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath(path))
        WebDriverWait(self.driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, path)))
        return self.driver.find_elements_by_xpath(path)

    #根据xpath定位数据
    def findByXpath(self,module,title):
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH, ReadYaml.readYaml(module, title))))
        return self.driver.find_element_by_xpath(ReadYaml.readYaml(module,title))

    def getInputByClass(self,className,name,value):
        xpath="//div[@class='"+className+"']//label[text()='"+name+"']/../div/div/input"
        Common(self.driver).getDriver(xpath).clear()
        return Common(self.driver).getDriver(xpath).send_keys(value)

    def getSelectByClass(self,className,name,value):
        if value=='':
            return
        xpath="//div[@class='"+className+"']//label[text()='"+name+"']/../div/div/div/input"
        d=Common(self.driver).getDriver(xpath)
        d.click()
        d.send_keys(value)##用于模糊搜索
        time.sleep(1)
        xpath = "//div[@class='el-select-dropdown el-popper' and @x-placement='bottom-start']//span[contains(text(), '"+value+"')]"
        #xpath="//div[@class='el-select-dropdown el-popper' and @x-placement='bottom-start']//span[(text()='"+value+"')]"
        Common(self.driver).getDriver(xpath).click()

    def getDateSelectByClass(self,className,name,value):
        xpath="//div[@class='"+className+"']//label[text()='"+name+"']/../div/div/input"
        d = Common(self.driver).getDriver(xpath)
        d.click()
        d.send_keys(value)

    def getButtonByClass(self,className,value):
        xpath="//div[@class='"+className+"']//span[contains(text(),'"+value+"')]"
        Common(self.driver).getDriver(xpath).click()


    def dialogInput(self,module,className,value):
        xpath="//*[@aria-label='"+module+"']//*[text()='"+className+"']/../div/div/input"
        Common(self.driver).getDriver(xpath).send_keys(value)

    def dialogSelect(self,module,className,value):
        xpath="//*[@aria-label='"+module+"']//label[text()='"+className+"']/../div/div/div/input"
        d=Common(self.driver).getDriver(xpath)
        d.click()
        d.send_keys(value)##用户模糊搜索
        xpath="//div[@class='el-select-dropdown el-popper sex' and @x-placement='bottom-start']//span[(text()='"+value+"')]"
        Common(self.driver).getDriver(xpath).click()

    def dialogTextarea(self,module,className,value):
        xpath = "//*[@aria-label='" + module + "']//*[text()='" + className + "']/../div/div/textarea"
        Common(self.driver).getDriver(xpath).send_keys(value)

    def getDialogButton(self,module,name):
        xpath="//div[@role='dialog' and @aria-label='"+module+"']//button//span[contains(text(),'"+name+"')]"
        Common(self.driver).getDriver(xpath).click()

    def dialogNumInput(self,module,name,value):
        xpath="//*[@aria-label='"+module+"']//*[text()='${name}"+name+"']/../div/div/div/input"
        Common(self.driver).getDriver( xpath).send_keys(value)

    def dialogCloseByModule(self,module):
        xpath="//*[@aria-label='"+module+"']//*[@aria-label='Close']"
        Common(self.driver).getDriver( xpath).click()


    def getLink(self,title):
        xpath="//span[(text()='"+title+"')]"
        Common(self.driver).getDriver(xpath).click()

    def queryByConditions(self,list_key,list_value,xpath):
        rows=Common(self.driver).getDrivers(xpath)
        numbers=len(rows)+1
        for rowIndex in range(1,numbers):
            Common(self.driver).queryAssert(list_key,list_value,rowIndex)

    def queryAssert(self,list_key,list_value,rowIndex):
        keyNumbers = len(list_key)
        for num in range(keyNumbers):
            value = list_value[num]
            key = list_key[num]
            xpath1 = "//*[@class='el-table__body']//tbody/tr[" + str(rowIndex) + "]/td[" + str(key) + "]"
            curText=Common(self.driver).getDriver(xpath1).text
            print(curText+"====="+value)
            assert curText==value


    def getTableButton(self,name):
        xpath="//table[@class='el-table__body']//span[contains(text(),'"+name+"')]"
        Common(self.driver).getDriver(xpath).click()

    def getSelectValue(self,className,name):
        xpath="//div[@class='"+className+"']//label[text()='"+name+"']/../div/div/div/input"
        d = Common(self.driver).getDriver(xpath).get_attribute('value')
        return d