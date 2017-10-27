# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from selenium import webdriver



survey_code = "22423-13301-02717-15283-00032-4"
site = "https://www.mcdvoice.com/"
survey_code= survey_code.split("-")

browser = webdriver.Firefox()
browser.get(site)
for i in range(len(survey_code)):
    print (i)
    CN = browser.find_element_by_id("CN"+str(i+1))
    CN.send_keys(survey_code[i])
browser.find_element_by_id("NextButton").click()

#nextpage
browser.find_element_by_class_name("radioBranded").click()
browser.find_element_by_id("NextButton").click()

#next page
browser.find_element_by_class_name("radioBranded").click()
browser.find_element_by_id("NextButton").click()

#nextpage (satisfied lvl)
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt4').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()

#nextpage
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt4').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()

#nextpage (yes/no)
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt1').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()

#nextpage
browser.find_element_by_id("NextButton").click()


#nextpage (satisfied lvl)
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt4').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()

#nextpage
browser.find_element_by_id("NextButton").click()

#nextpage (yes/no)
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt2').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()

#nextpage
browser.find_element_by_class_name('Opt2').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()


#nextpage coffee
browser.find_element_by_class_name('Opt3').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()

#nextpage (satisfied lvl)
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt4').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()

#nextpage
browser.find_element_by_class_name('Opt2').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()


#nextpage (yes/no)
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt2').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()


#nextpage
browser.find_element_by_class_name("radioBranded").click()
browser.find_element_by_id("NextButton").click()

#nextpage
browser.find_element_by_class_name("radioBranded").click()
browser.find_element_by_id("NextButton").click()

#nextpage (satisfied lvl)
table = browser.find_element_by_tag_name("tbody")
ops = browser.find_elements_by_tag_name('tr')[1:]
for i in ops:
    i.find_element_by_class_name('Opt3').find_element_by_class_name('radioBranded').click()
browser.find_element_by_id("NextButton").click()


#nextpage
browser.find_element_by_id("NextButton").click()

#done xD










