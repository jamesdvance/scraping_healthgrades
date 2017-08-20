import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait	
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import json
import pandas as pd
import datetime

def get_started(specialty_name):

	browser = webdriver.Firefox()
	browser.get('https://www.healthgrades.com')

	browser.wait = WebDriverWait(browser, 45)
	element = browser.wait.until(EC.presence_of_element_located((By.ID, 'search-term-selector-child')))

	search_Elem = browser.find_element_by_id('search-term-selector-child')
	search_Elem.send_keys(specialty_name)

	submit_button = browser.find_element_by_xpath('//*[@id="pageHeroHeader"]/div/div/div[2]/div/form/div/button/span[1]')
	submit_button.click()

	browser.wait = WebDriverWait(browser, 45)
	element = browser.wait.until(EC.presence_of_element_located((By.ID, 'select-filter-Distance')))

	distance_Elem = Select(browser.find_element_by_id('select-filter-Distance'))
	distance_Elem.select_by_visible_text('National')
	browser.wait = WebDriverWait(browser, 10)
	element = browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'uCard__name')))
	return(browser)

# Pull a single phone number from a doctor's personal page
def get_single_number():
	browser.wait = WebDriverWait(browser, 10)
	browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'hg3-address')))
	PhoneElems = browser.find_elements_by_class_name('hg3-address')
	PhoneList = []
	for element in PhoneElems:
		PhoneList.append(element.text)
	phone_segment = PhoneList[len(PhoneList)-1]
	line_id = re.compile("\n")
	phone_container_lines = line_id.split(phone_segment)
	phone = phone_container_lines[len(phone_container_lines)-1]
	print(phone)
	return(phone)
# Pull a single name from a doctor's personal page
def get_single_item_by_class(class_name):
	browser.wait = WebDriverWait(browser, 5)
	browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
	Elem = browser.find_element_by_class_name(class_name)
	return Elem.text

def try_and_retry_append(base_xpath, alt_base, end_xpath):
	'''browser.wait = WebDriverWait(browser, 10)
	browser.wait.until(EC.presence_of_ele ment_located((By.XPATH, xpath)))'''
	attempts=0
	while(attempts < 5):
		attempts +=1
		try:
			result= browser.find_element_by_xpath(base_xpath+end_xpath).text
			break
		except StaleElementReferenceException:
			print("retrying")
		except NoSuchElementException:
			base_xpath = alt_base
			print("retrying path")
	print(result)
	return result
def try_and_retry_append_phone(base_xpath, alt_base, end_xpath):
	'''browser.wait = WebDriverWait(browser, 10)
	browser.wait.until(EC.presence_of_ele ment_located((By.XPATH, xpath)))'''
	attempts=0
	while(attempts < 5):
		attempts +=1
		try:
			result= browser.find_element_by_xpath(base_xpath+end_xpath).text
			break
		except StaleElementReferenceException:
			print("retrying")
	return result

def try_and_retry_append_single_path(xpath):
	'''browser.wait = WebDriverWait(browser, 10)
	browser.wait.until(EC.presence_of_ele ment_located((By.XPATH, xpath)))'''
	attempts=0
	while(attempts < 5):
		attempts +=1
		try:
			result= browser.find_element_by_xpath(xpath).text
			break
		except StaleElementReferenceException:
			print("retrying")
		except NoSuchElementException:
			browser.refresh()
			browser.wait = WebDriverWait(browser, 5)
			browser.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
	return result

def get_single_item_by_XPath(XPath1, XPath2="none"):
	if XPath2 == "none":
			browser.wait = WebDriverWait(browser, 10)
			browser.wait.until(EC.presence_of_element_located((By.XPATH, XPath1)))
			Elem = browser.find_element_by_xpath(XPath1)
			return Elem.text
	else:
		try: 
			browser.wait = WebDriverWait(browser, 10)
			browser.wait.until(EC.presence_of_element_located((By.XPATH, XPath1)))
			Elem = browser.find_element_by_xpath(XPath1)
			return Elem.text
		except TimeoutException:
			browser.wait.until(EC.presence_of_element_located((By.XPATH, XPath2)))
			Elem = browser.find_element_by_xpath(XPath2)
			return Elem.text


# Pull some element from the list of doctors page
def retrying_find_element(class_name, class_vec):
	attempts = 0
	while(attempts < 5):
		attempts += 1
		try:
			Elems = browser.find_elements_by_class_name(class_name)
			for elem in Elems:
				class_vec.append(elem.text)
			break
		except StaleElementReferenceException:
			print('retrying...')
	return(class_vec)
# Click through a list of doctors and pull the phone number from each one
def scrape_single_page():
	phone_vec = []
	name_vec =[]
	location_vec = []
	address_vec = []
	city_vec = []
	state_vec = []
	zip_vec = []
	spec_vec = []

	attempts = 0
	while(attempts < 2):
		attempts += 1
		try:
			Elems = browser.find_elements_by_class_name('proCard')
			break
		except StaleElementReferenceException:
			print('retrying...')
	
	for i in range(3, len(Elems)+3):
		base_xpath = '//*[@id="card-carousel-search"]/div[2]/ul/li['+str(i)+']/div/div[1]'
		alt_xpath = '//*[@id="card-carousel-search"]/div[2]/ul/li['+str(i)+']/div/div'
		'''browser.wait = WebDriverWait(browser, 10)
		browser.wait.until(EC.presence_of_element_located((By.XPATH, base_xpath)))'''
		name_vec.append(try_and_retry_append(base_xpath, alt_xpath,'/div[1]/div/div[2]/h3/a'))
		location_vec.append(try_and_retry_append(base_xpath, alt_xpath,'/div[2]/div/div[1]/a/span/strong'))
		address_vec.append(try_and_retry_append(base_xpath, alt_xpath,'/div[2]/div/div[1]/a/span/span[1]'))
		city_vec.append(try_and_retry_append(base_xpath, alt_xpath,'/div[2]/div/div[1]/a/span/span[2]/span[1]'))
		state_vec.append(try_and_retry_append(base_xpath, alt_xpath,'/div[2]/div/div[1]/a/span/span[2]/span[3]'))
		zip_vec.append(try_and_retry_append(base_xpath, alt_xpath,'/div[2]/div/div[1]/a/span/span[2]/span[5]'))
		
		try:
			phone_vec.append(try_and_retry_append_phone(base_xpath, alt_xpath,'/div[1]/div/div[2]/a[2]/span'))	
		except NoSuchElementException:
			phone_vec.append("none found")
			'''attempts = 0
			while(attempts < 2):
				attempts+=1
				try:
					browser.find_element_by_xpath(base_xpath+'/div[1]/div/div[2]/h3/a').click()
					break
				except StaleElementReferenceException:
					print("retrying click")
			try:
				phone_vec .append(try_and_retry_append_phone('','','//*[@id="js-quick-view"]/div[1]/div[2]/header/div[3]/div[2]/div[1]/span[2]'))
			except NoSuchElementException:
				phone_vec.append(get_single_number())
			attempts = 0
			while(attempts < 2):
				try:
					browser.back()

					break
				except TimeoutException:
					print('retrying')
			# May need to add logic here to reset 'national'
			attempts += 1'''
		#browser.execute_script("window.history.go(-1)")
	df = pd.concat([pd.DataFrame(name_vec), pd.DataFrame(phone_vec), pd.DataFrame(location_vec), pd.DataFrame(address_vec), pd.DataFrame(city_vec), pd.DataFrame(state_vec), pd.DataFrame(zip_vec)], axis = 1)
	df.columns = ['Name', 'Phone', 'Practice_Name', 'Address', 'City', 'State', 'Zip']
	return df



def page_by_page(specialty_name):
	df = scrape_single_page()
	file = open("../dr_lists/" + specialty_name + "_list.csv", "w")
	df.to_csv(file, index=False)


	next_Elem = browser.find_element_by_xpath('//*[@id="card-carousel-search"]/div[2]/div/a/span[1]')
	next_Elem.click()

	iter = 0
	while(EC.presence_of_element_located((By.XPATH,'//*[@id="card-carousel-search"]/div[2]/div/a[2]/span[1]'))):
		df1 = scrape_single_page()
		df = df.append(df1)
		iter+=1
		if iter > 50:
			file = open("../dr_lists/" + specialty_name + "_list.csv", "a")
			df.to_csv(file, header=False,index=False)
			iter = 0

		next_Elem = browser.find_element_by_xpath('//*[@id="card-carousel-search"]/div[2]/div/a[2]/span[1]')
		next_Elem.click()

	df = scrape_single_page()
	file = open("../dr_lists/" + specialty_name + "_list.csv", "a")
	df.to_csv(file, header=False,index=False)


	return print("Finished" + specialty_name)


browser = get_started("Family Practice")

page_by_page("Family_Practice")

