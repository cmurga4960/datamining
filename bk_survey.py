# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 21:51:58 2017

@author: The4960
"""
from selenium import webdriver


def fill_satisfied_table(browser):
    #nextpage (satisfied lvl)
    table = browser.find_element_by_tag_name("tbody")
    ops = table.find_elements_by_tag_name('tr')[1:]
    for i in ops:
        i.find_element_by_class_name('Opt4').find_element_by_class_name('radioBranded').click()
    browser.find_element_by_id("NextButton").click()

def first_radio(browser):
    browser.find_element_by_class_name("radioBranded").click()
    browser.find_element_by_id("NextButton").click()

def last_radio(browser):
    browser.find_elements_by_class_name("radioBranded")[-1].click()
    browser.find_element_by_id("NextButton").click()





resturant_number = "11076"
survey_code = "07510-48122-21033-171604"
site = "https://www.mybkexperience.com/"
survey_code= survey_code.split("-")

browser = webdriver.Firefox()
browser.get(site)
browser.find_element_by_id("Initial_StoreID").send_keys(resturant_number)
browser.find_element_by_id("NextButton").click()

for i in range(len(survey_code)):
    print (i)
    CN = browser.find_element_by_id("CN"+str(i+1))
    CN.send_keys(survey_code[i])
browser.find_element_by_id("NextButton").click()


fill_satisfied_table(browser)
first_radio(browser)
fill_satisfied_table(browser)
fill_satisfied_table(browser)
first_radio(browser)
first_radio(browser)
last_radio(browser)
browser.find_element_by_id("NextButton").click()
browser.find_element_by_id("NextButton").click()
first_radio(browser)
first_radio(browser)
browser.find_element_by_id("NextButton").click()

#got it xD
