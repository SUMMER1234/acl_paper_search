#coding=utf-8
#!/usr/bin/env python3


from selenium import webdriver
import pyperclip


class Selenium_export():
    def __init__(self,driver_path,element,element_type):
        if element_type == 'xpath':
            self.element_xpath = element
        elif element_type == 'css_selector':
            self.element_css_selector = element
        elif element_type == 'id':
            self.element_id = element
        elif element_type == 'name':
            self.element_name = element
        self.driver_path=driver_path


    def setup(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def get_url(self,url):
        if url:
            self.driver.get(url)
        else:
            raise ValueError('Please input the page url you want to cite.')


    def check_element_enable(self):
        self.driver.implicitly_wait(5)
        if self.element_xpath:
            self.button = self.driver.find_element_by_xpath(self.element_xpath)
        elif self.element_css_selector:
            self.button = self.driver.find_element_by_css_selector(self.element_css_selector)
        elif self.element_id:
            self.button = self.driver.find_element_by_id(self.element_id)
        elif self.element_name:
            self.button = self.driver.find_element_by_name(self.element_name)
        else:
            raise ValueError('You have to enter the xpath or css selector or id or name of the button.')
        self.is_clickable = self.button.is_enabled()
        return self.is_clickable

    def click_and_copy(self):
        self.button.click()
        self.result=pyperclip.paste()
        return self.result

    def tear_down(self):
        self.driver.quit()

if __name__ == '__main__':
    driver_path = "/Users/summer-sun/chromedriver"
    webpage_url = "https://aclanthology.org/2021.winlp-1.4/"
    xpath_fromat_dict={"BibText":"//*[@id='main']/div[2]/div[1]/dl/dd[17]/button[1]",
                       "Markdown":"//*[@id='main']/div[2]/div[1]/dl/dd[17]/button[2]",
                       "MODS XML":"//*[@id='main']/div[2]/div[1]/dl/dd[17]/button[3]",
                       "Endnote":"//*[@id='main']/div[2]/div[1]/dl/dd[17]/button[4]"}
    se=Selenium_export(driver_path=driver_path, element=xpath_fromat_dict["BibText"],element_type="xpath" )
    se.setup()
    se.get_url(webpage_url)
    if se.check_element_enable()==True:
        result = se.click_and_copy()
        se.tear_down()
    print(result)
