from time import sleep
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import pygetwindow as gw
import pyperclip
import random
from bs4 import BeautifulSoup
import pickle
import json
import random
import pandas as pd
import xml.etree.ElementTree as ET


def connect(html_path, vpn_extension_path):
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--load-extension={}'.format(vpn_extension_path))

    chromedriver = ChromeService(ChromeDriverManager().install())

    driver = Chrome(service=chromedriver, options=chrome_options)

    sleep(5)
    current_tab = driver.current_window_handle

    all_tabs = driver.window_handles
    for tab in all_tabs:
        if tab != current_tab:
            driver.switch_to.window(tab)
            driver.close()

    driver.switch_to.window(all_tabs[0])
    driver.maximize_window()
    
    driver.get(html_path)
    return driver


def turn_on_vpn():
    sleep(5)

    target_x = 1750
    target_y = 90
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()

    target_x = 1500
    target_y = 300
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()
    
    sleep(2)
    target_y = 380
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()
    
    target_y = 300
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()

    target_y = 500
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()

    sleep(5)
    target_x = 1000
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()
    
    
def unusual_activity(driver, link):
    while "We've noticed some unusual activity" in driver.page_source:
        click_link(driver) 
        driver.get(link)
        
    return driver


def click_us():
    sleep(5)

    target_x = 1750
    target_y = 200
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()

    target_x = 580
    target_y = 640
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()
    pyautogui.click()
    
    
def click_link(driver):
    sleep(5)

    target_x = 150
    target_y = 200
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.rightClick()

    target_y = 220
    pyautogui.moveTo(target_x, target_y, duration=random.uniform(0.2, 1.0))
    pyautogui.click()
    
    sleep(5)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    sleep(5)
    
    
def cookies(driver):
    pickle.dump(driver.get_cookies(), open("cookies.txt", "wb"))
    
    for cookie in pickle.load(open('cookies.txt', 'rb')):
        driver.add_cookie(cookie)

    sleep(3)
    
    return driver


def item_links(driver, site_path):
    item_links_list=[]
    driver.get(site_path)
    count=0
    page=1
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            item_links_list.append("https://www.nordstrom.com"+article.find_all('a')[0].get('href').split("?")[0])

            count+=1
            if count==120:
                break
        if count==120:
                break
        page+=1
        driver.get(f"{site_path}?page={page}")
        sleep(5)

    return driver, item_links_list


def product_types(product, taxonomy_path):
    with open(taxonomy_path, 'r') as file:
        lines = file.read().split('\n')

    del lines[0]
    del lines[-1]
    
    type_dict = {}
    for line in lines:
        key, values_str = line.split(' - ')
        values_list = values_str.split(' > ')
        type_dict[int(key)] = values_list
        
    for key in type_dict.keys():
        if product==type_dict[key][-1]:
            product_type = ' > '.join(type_dict[key])
            google_product_category = key
            return google_product_category, product_type
        
        
def data_by_key(diff, key, product_dict, additional_images_list):
    
    id_pl=diff[key]['id']
    color=diff[key]['colorDisplayValue']
    color_id=diff[key]['colorId']
    size=diff[key]['sizeDisplayValue']
    size_id=diff[key]['sizeId']
    availability=diff[key]['isAvailable']
    price=diff[key]['price']
    
    additional_images=additional_images_list[color_id]
    image_link=additional_images[0]
    
    product_dict['id']=product_dict['id']+"_"+id_pl
    product_dict['link']=f"{product_dict['link']}?color={color_id}&size={size_id.replace(' ', '%20')}"
    product_dict['color']=color
    product_dict['size']=size
    product_dict['availability']=availability
    product_dict['price']=price
    product_dict['image_link']=image_link
    product_dict['additional_images']=additional_images
    
    return product_dict


def take_product_subtype(product_dict, json_data, link):
    diff={}
    diff.update(json_data['viewData']['skus']['byId'])
    
    for key in diff.keys():
        current_price_type=json_data['viewData']['price']['bySkuId'][key]['currentPriceType'].lower()
        price_units = json_data['viewData']['price']['bySkuId'][key][current_price_type]['price']['units']
        currency_code = json_data['viewData']['price']['bySkuId'][key][current_price_type]['price']['currencyCode']
        diff[key]['price'] = f"{price_units} {currency_code}"
        
    price_colors = {}
    for key in diff.keys():
        price_colors[diff[key]['colorId']]=diff[key]['price']
        
    diff_sold=json_data['viewData']['soldOutSkus']['byId']
    for key in diff_sold.keys():
        try:
            diff_sold[key]['price']=price_colors[diff_sold[key]['colorId']]
        except:
            diff_sold[key]['price']=diff[list(diff.keys())[0]]['price']
            
        
    diff.update(diff_sold)
    
    additional_images_list={}
    for jn in json_data['viewData']['mediaExperiences']['carouselsByColor']:
        additional_images_list[jn['colorCode']]=[]
        for img in jn['orderedShots']:
            additional_images_list[jn['colorCode']].append(img['url'])
    
    product_dict_list=[]
    for key in diff.keys():
        product_dict_list.append(data_by_key(diff, key, product_dict.copy(), additional_images_list).copy())
        
    return product_dict_list


def take_product(driver, link, taxonomy_path):
    def contains_initial_config(tag):
        return tag.name == 'script' and 'window.__INITIAL_CONFIG__' in tag.text
    
    sleep(random.uniform(2, 10))
    driver.get(link)
    driver=unusual_activity(driver, link)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    script = soup.find_all(contains_initial_config)[0].text
    
    json_data=json.loads(script[len("window.__INITIAL_CONFIG__ = "):])
    
    id=json_data['viewData']['id']
    item_group_id=json_data['viewData']['id']
    mpn=json_data['viewData']['filters']['group']['byId'][list(json_data['viewData']['filters']['group']['byId'].keys())[0]]['originalStyleNumber']
    title=json_data['viewData']['productTitle']
    description=json_data['viewData']['description']
    gender=json_data['viewData']['gender']
    age_group=json_data['viewData']['ageGroups'][0].lower()
    brand=json_data['viewData']['brand']['brandName']
    condition=None
    gtin=None
    product=json_data['viewData']['productTypeParentName']
    google_product_category, product_type=product_types(product, taxonomy_path)
    
    product_dict={
        'id': id,
        'item_group_id': item_group_id,
        'mpn': mpn,
        'title': title,
        'description': description,
        'gender': gender,
        'age_group': age_group,
        'link': link,
        'brand': brand,
        'condition': condition,
        'gtin': gtin,
        'product_type': product_type,
        'google_product_category': google_product_category
    }
    
    return take_product_subtype(product_dict, json_data, link)


def main(html_path, vpn_extension_path, taxonomy_path):
    driver=connect(html_path, vpn_extension_path)
    turn_on_vpn()
    click_link(driver)
    
    while "We've noticed some unusual activity" in driver.page_source:
        driver.get(html_path)
        click_link(driver)  
        
    sleep(10)    
    if "We Ship to" in driver.page_source:
        pyautogui.click()
    
    click_us()
    
    driver=cookies(driver)
    driver, item_links_list=item_links(driver, site_path)
    
    results=[]
    for link in item_links_list:
        if len(results)>=120:
            break
        
        results=results+take_product(driver, link, taxonomy_path)
    
    driver.close()
    return results[:120]


def convert_xml(result, result_path):
    df = pd.DataFrame(result)
    df['additional_images'] = df['additional_images'].apply(lambda x: ', '.join(x))

    root = ET.Element('channel')
    description = ET.SubElement(root, 'description')
    description.text="Nordstrom"

    for i, row in df.iterrows():
        item = ET.SubElement(root, 'item')
        for col in df.columns:
            elem = ET.SubElement(item, col)
            elem.text = str(row[col])

    tree = ET.ElementTree(root)
    with open(result_path, 'wb') as f:
        tree.write(f)
        
        
html_path="C:\\Users\\User\\test_task\\result\\link.html"
vpn_extension_path = 'C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\bihmplhobchoageeokmgbdihknkjbknd\\5.0.18_0'
site_path = "https://www.nordstrom.com/browse/women/clothing/dresses"
result_path = "C:\\Users\\User\\test_task\\result\\fid.xml"
taxonomy_path = "C:\\Users\\User\\test_task\\result\\taxonomy-with-ids.en-US.txt"

result = main(html_path, vpn_extension_path, taxonomy_path)
convert_xml(result, result_path)
print("Done!")