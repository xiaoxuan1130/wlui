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

    def getCurrentDate(self):
        return time.strftime("%Y-%m-%d", time.localtime())

    def getDateDiff(day):
        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=day)
        return yes_time.strftime('%Y-%m-%d')

    def getName(key):
        key=ReadYaml.realVarYaml(key)
        return key+"_"+getDate()+"_"+getRandom()

    def getDriver(driver, path):
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, path)))
        return driver.find_element_by_xpath(path)

    def getDrivers(driver, path):
        #return WebDriverWait(driver, 10).until(lambda x: x.find_elements_by_xpath(path))
        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, path)))
        return driver.find_elements_by_xpath(path)

    #根据xpath定位数据
    def findByXpath(driver,module,title):
        WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH, ReadYaml.readYaml(module, title))))
        return driver.find_element_by_xpath(ReadYaml.readYaml(module,title))

    def getInputByClass(driver,className,name,value):
        xpath="//div[@class='"+className+"']//label[text()='"+name+"']/../div/div/input"
        Common.getDriver(driver, xpath).clear()
        return Common.getDriver(driver, xpath).send_keys(value)

    def getSelectByClass(driver,className,name,value):
        if value=='':
            return
        xpath="//div[@class='"+className+"']//label[text()='"+name+"']/../div/div/div/input"
        d=Common.getDriver(driver,xpath)
        d.click()
        d.send_keys(value)##用于模糊搜索
        time.sleep(1)
        xpath = "//div[@class='el-select-dropdown el-popper' and @x-placement='bottom-start']//span[contains(text(), '"+value+"')]"
        #xpath="//div[@class='el-select-dropdown el-popper' and @x-placement='bottom-start']//span[(text()='"+value+"')]"
        Common.getDriver(driver,xpath).click()

    def getDateSelectByClass(driver,className,name,value):
        xpath="//div[@class='"+className+"']//label[text()='"+name+"']/../div/div/input"
        d = Common.getDriver(driver, xpath)
        d.click()
        d.send_keys(value)

    def getButtonByClass(driver,className,value):
        xpath="//div[@class='"+className+"']//span[contains(text(),'"+value+"')]"
        Common.getDriver(driver,xpath).click()


    def dialogInput(driver,module,className,value):
        xpath="//*[@aria-label='"+module+"']//*[text()='"+className+"']/../div/div/input"
        Common.getDriver(driver, xpath).send_keys(value)

    def dialogSelect(driver,module,className,value):
        xpath="//*[@aria-label='"+module+"']//label[text()='"+className+"']/../div/div/div/input"
        d=Common.getDriver(driver,xpath)
        d.click()
        d.send_keys(value)##用户模糊搜索
        xpath="//div[@class='el-select-dropdown el-popper sex' and @x-placement='bottom-start']//span[(text()='"+value+"')]"
        Common.getDriver(driver,xpath).click()

    def dialogTextarea(driver,module,className,value):
        xpath = "//*[@aria-label='" + module + "']//*[text()='" + className + "']/../div/div/textarea"
        Common.getDriver(driver, xpath).send_keys(value)

    def getDialogButton(driver,module,name):
        xpath="//div[@role='dialog' and @aria-label='"+module+"']//button//span[contains(text(),'"+name+"')]"
        Common.getDriver(driver,xpath).click()

    def dialogNumInput(driver,module,name,value):
        xpath="//*[@aria-label='"+module+"']//*[text()='${name}"+name+"']/../div/div/div/input"
        Common.getDriver(driver, xpath).send_keys(value)

    def dialogCloseByModule(driver,module):
        xpath="//*[@aria-label='"+module+"']//*[@aria-label='Close']"
        Common.getDriver(driver, xpath).click()


    def getLink(driver,title):
        xpath="//span[(text()='"+title+"')]"
        Common.getDriver(driver,xpath).click()

    def queryByConditions(driver,list_key,list_value,xpath):
        rows=driver.find_elements_by_xpath(xpath)
        numbers=len(rows)+1
        for rowIndex in range(1,numbers):
            Common.queryAssert(driver,list_key,list_value,rowIndex)


    def queryAssert(driver,list_key,list_value,rowIndex):
        keyNumbers = len(list_key)
        for num in range(keyNumbers):
            value = list_value[num]
            key = list_key[num]
            xpath1 = "//*[@class='el-table__body']//tbody/tr[" + str(rowIndex) + "]/td[" + str(key) + "]"
            curText=driver.find_element_by_xpath(xpath1).text
            print(curText+"====="+value)
            assert curText==value