import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait	
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd

def get_started(specialty_name):

	browser = webdriver.Firefox()
	browser.get('https://www.healthgrades.com')

	browser.wait = WebDriverWait(browser, 45)
	element = browser.wait.until(EC.presence_of_element_located((By.ID, 'search-term-selector-child')))

	search_Elem = browser.find_element_by_id('search-term-selector-child')
	search_Elem.send_keys(specialty_name)
	search_Elem.submit()

	browser.wait = WebDriverWait(browser, 45)
	element = browser.wait.until(EC.presence_of_element_located((By.ID, 'select-filter-Distance')))

	distance_Elem = Select(browser.find_element_by_id('select-filter-Distance'))
	distance_Elem.select_by_visible_text('National')
	browser.wait = WebDriverWait(browser, 10)
	element = browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'uCard__name')))
	return(browser)

# Pull a single phone number from a doctor's personal page
def get_single_number():
	browser.wait = WebDriverWait(browser, 45)
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
def get_single_item(class_name):
	browser.wait = WebDriverWait(browser, 20)
	browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
	Elem = browser.find_element_by_class_name(class_name)
	return Elem.text

# Pull some element from the list of doctors page
def retrying_find_element(class_name, class_vec):
	attempts = 0
	while(attempts < 2):
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
def click_thru_phone_numbers(click_class_name):
	phone_vec = []
	name_vec =[]
	location_vec = []
	address_vec = []

	attempts = 0
	while(attempts < 2):
		attempts += 1
		try:
			Elems = browser.find_elements_by_class_name(click_class_name)
			break
		except StaleElementReferenceException:
			print('retrying...')
	browser.refresh()
	for i in range(0, len(Elems)-1):
		attempts = 0
		while(attempts < 2):
			attempts += 1
			try:
				elem_clicks = browser.find_elements_by_class_name(click_class_name)
				elem_clicks[i].click()
				break
			except StaleElementReferenceException:
				print('retrying...')
		while(attempts < 2):
			attempts += 1
			try:
				phone_num = get_single_number()
				name = get_single_item('provider-name')
				practice_name = get_single_item('location-name')
				address = get_single_item('street-address')
				break
			except StaleElementReferenceException:
				print('retrying...')
		#browser.execute_script("window.history.go(-1)")
		phone_vec.append(phone_num)
		name_vec.append(name)
		location_vec.append(practice_name)
		address_vec.append(address)
		browser.back()
		browser.refresh()
	df = pd.DataFrame([name_vec, phone_vec, location_vec, address_vec])
	df.columns = ['Name', 'Phone', 'Practice_Name', 'Address']
	return df

browser = get_started("Family Practice")

df = click_thru_phone_numbers('uCard__name')

print(df)
#next_Elem = browser.find_element_by_class_name('shuffle-text')


'''
next_Elem.click()

browser.wait = WebDriverWait(browser, 90)
element = browser.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'shuffle-text')))

while(len(browser.find_elements_by_class_name('shuffle-text'))==2):

	Names = retrying_find_element('uCard__name',Names)
    
	Specialties = retrying_find_element('uCard_Specialty', Specialties)
    
	Locations= retrying_find_element('office-location__address', Locations)
    
	nav_Buttons = browser.find_elements_by_class_name('shuffle-text')
	nav_Buttons[1].click()

Names = retrying_find_element('uCard__name',Names)
    
Specialties = retrying_find_element('uCard_Specialty', Specialties)
    
Locations= retrying_find_element('office-location__address', Locations)

# Getting phone numbers



City_State_Zips = []
Addresses = []
Practice_Names = []

Elem_LocationAddress = [x for x in Locations if x != '']
for elem in Elem_LocationAddress:
	loc_list = re.split("\n", elem)
	City_State_Zips.append(loc_list[-1])
	Addresses.append(loc_list[-2])
	if len(loc_list)==3:
		Practice_Names.append(loc_list[-3])
	else:
		Practice_Names.append("None Listed")

df = pd.concat([pd.DataFrame(Names), pd.DataFrame(Specialties), pd.DataFrame(Practice_Names), pd.DataFrame(Addresses), pd.DataFrame(City_State_Zips), pd.DataFrame(Phones)], axis = 1)
df.columns = ['Name', 'Specialty', 'Practice_Name', 'Address', 'City_State_Zip', 'Phone']
df.to_csv("specialties_with_phones_test.csv", index=False)'''