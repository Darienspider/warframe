"""
Warframe Bot
Created by Shadarien Williams

Terminal based bot that scans warframe markets for the item entered and returns either their hightest, lowest, and average price
or all auctions that have been made for said item.
"""

"""
UPDATES:

Date                                           Name                                         Description
5/12/2024                                  Shadarien Williams                              Initial upload
8/14/2024                                  Shadarien Williams                              updated code to use the engine globally and created a neww function that scans the wiki
"""


import requests as rq
import json 
import os 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#Torid acri-ignicron
class warframeApi:
    def __init__(self, chrome_path: str):
        # Initialize the Chrome driver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.engine = engine = webdriver.Chrome( options = chrome_options)
    

    def how_to_get_item(self,item_name : str):
        item_name = str(item_name).replace(" ",'_')
        site = f'https://warframe.fandom.com/wiki/{item_name}'

        aquisitionTable = 'article-table sortable acquisition-table jquery-tablesorter'
        craftingTable = 'foundrytable'

        content = rq.get(site).content
        scanner = BeautifulSoup(content,'lxml')
        # apparently you can do compounded searches like this
        # the [1:] is used to remove the header rows
        how_to_get = scanner.find('tbody').find_all('tr')[1:]
        
        acquisitions = []
        for index,value in enumerate(how_to_get):
            details = (how_to_get[index].text.strip().split('\n'))
            # convert extracted data to dictionary
            extraction = { 'Name':
                details[0], 
                'Details':
                    { 'location':
                        details[1],
                    'chance_of_drop':
                    details[2],
                    'expected_num_of_runs':
                    details[3],
                    'Gauranteed_num_of_runs':
                    details[-1]
                }
            }

            acquisitions.append(extraction)

        self.acquisition = acquisitions
        return self.acquisition



        # skip the first row as it has the headers
        # for i in how_to_get[1:]:
        #     how_to_getItem.append(str(i.text).strip())

        # may convert to a dictionary
        self.acquisition = how_to_getItem
        
        return self.acquisition

    def getRiven(self,arcaneName : str):
        try:
            weaponName = str(arcaneName).split()[0].lower()
            arcane = str(arcaneName).split()[1]
        except:
            return "Not an Arcane"
        site = f'https://warframe.market/auctions/search?type=riven&weapon_url_name={weaponName}&sort_by=price_desc'

        chromePath = "/home/shadarien/Downloads/chrome-linux64/"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        self.engine.get(site)
        WebDriverWait(self.engine, 10).until(EC.presence_of_element_located((By.ID, "application-state")))

        scanner = BeautifulSoup(self.engine.page_source,'lxml')
        script_tag = scanner.find('script', {"id": "application-state"})

        # print(script_tag)
        try:
            data = json.loads(script_tag.string)
            auctions = data['payload']['auctions']
            listedAuctions = []
    
            for auction in auctions:
                item_name = auction["item"]["name"]
                startingPrice = auction['starting_price']
                # top_bid = auction['top-bid']
                owner_ingame_name = auction['owner']['ingame_name']


                if (str(arcane.lower()) in str(item_name.lower())):
                    listedAuctions.append((item_name,  startingPrice, owner_ingame_name))
            
            if len(listedAuctions) >1:
                return True,listedAuctions
            else:
                return False,None
        except:
            return False, None
        
        engine.close()

    def get_arcane(self,arcane_name:str):
        data = {}
        site = f"https://api.warframestat.us/arcanes/search/{arcane_name}"
        content = rq.get(site)
        if content.status_code != 200:
            return False
        
        payload = str(content.content).replace('[','').replace(']','').replace("b'",'').replace("'",'')
        try: 
            answer = json.loads(payload)
            print(answer["name"])
            print(answer["effect"])
            print(answer["rarity"])
            
        except Exception as e:
            print(f'ERROR: {e} ')
            
    def scan_warframe(self,item_name):
        item_name = item_name.lower()
        item_name = str(item_name).replace(" ","_")

        API_template = f"https://api.warframe.market/v1/items/{item_name}/orders"
        src = rq.get(API_template).content
        src = str(src).strip()

        with open("output.json","w") as data_file:
            # Formats the src code to be in json format by removing a few extra
            data_file.write(src[2:-1])
            data_file.close()

        with open("output.json") as order_data:
            exported_data = json.load(order_data)
            order_data.close()

        found_data = exported_data['payload']['orders']

        total_price = 0
        order_count = 0
        prices = []

        for order in found_data:
            
            if order["order_type"] =="buy":
                order_count+=1
                found_price = order['platinum']
                prices.append(found_price)

                total_price += found_price
                prices.sort()

        average_price = total_price/order_count
        lowest_price = prices[0]
        highest_price = prices[-1]
        message = (f'Average: {average_price}\nTotal Orders: {order_count}\nLowest Price: {lowest_price}\nHighest Price: {highest_price}\n\n')
        return (True, message)

    def close(self):
        # Close the browser when done
        self.engine.quit()

chrome_path = "/home/shadarien/Downloads/chrome-linux64/chromedriver"  # Update this path
test = warframeApi(chrome_path)

executed = True
# test.get_arcane("Arcane grace")
counter = 0 

while executed:
    print("If you want to cancel script, enter 'y', exit, or an empty value (space)")
    
    choice = input('What mode would you like to use? \n\t [1] Scan Warframe market \n\t [2] Scan Item Details \n ENTER HERE: ')
    scan_item = input("\nPlease enter item to scan: ")

    if int(choice) == 1:
        # scan_item = 'Torid acri-ignicron'
        if str(scan_item).lower() in ["exit"," ","y"]:
            break
        
        else:
            counter +=1
            print(f"Scanning for {scan_item}")
            
            # Torid acri-ignicron

        output = test.getRiven(scan_item)
        if output[0] or not TypeError:
            print(output[1])
        try:
            output = test.scan_warframe(scan_item)[1]
        except Exception as e:
            try:
                newItem = scan_item + ' Blueprint'
                output = test.scan_warframe(newItem)[1]
            except Exception as e:
                print(f"Error : {e} \n Unable to locate item \n\n")
        
        print(output)
    elif int(choice) == 2:
        if str(scan_item).lower() in ["exit"," ","y"]:
            break
        test.get_item_details(scan_item)
    else:
        break

# scan_item = 'dante'
# test.how_to_get_item(scan_item)
# for i in test.acquisition:
#     print(i['Name'],' ',i['Details']['location'])