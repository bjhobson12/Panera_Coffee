# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from sys import exit, platform, argv, stderr
import os
import time
import argparse

# Gather args
parser = argparse.ArgumentParser(description='Get Panera Coffee.')
required = parser.add_argument_group('required arguments')
required.add_argument('--username', help='My Panera Username', required=True)
required.add_argument('--password', help='My Panera Password', required=True)
required.add_argument('--zip', help='Your zip code', required=True)
required.add_argument('--type', help="""Type of coffee you want. Choose from:
Iced Coffee,
Light Roast Coffee,
Hazelnut Coffee,
Dark Roast Coffee,
Decaf Coffee,
Hot Tea""", required=True)
parser.add_argument('--headless', help='Add this flag if you want to keep your browser closed', action='store_true')
args = parser.parse_args()

# Chooses and unzips a local chromedriver zip file (defaults to system platform)
def platform_action(plat=platform):

    # Assigns commands and generic system name
    if plat=="darwin" or plat=="mac":
        machine_name = "mac"
        local_file_commands = ["unzip chromedriver_mac64.zip"] #, "chmod 755 chromedriver"]
    elif plat=="win32" or plat=="windows":
        machine_name = "windows computer"
        local_file_commands = ["Expand-Archive -Force ./chromedriver_win32.zip ./"] #, "chmod 755 chromedriver"]
    elif plat=="linux" or plat=="linux2":
        machine_name = "linux machine"
        local_file_commands = ["unzip chromedriver_linux64.zip"] #, "chmod 755 chromedriver"]
    else:
        raise Error("Your computer platform wasn't recognized, and a local zip file could not be chosen for your chromedriver.")

    # Execute unzip commands
    for command in local_file_commands:
        try:
            os.system(command)
        except:
            print("The zip file " + '\033[1m' + local_file_commands[0].split(" ")[-1] + '\033[0m' + " could not be unzipped on your {}. Please manually unzip it, and rerun the program.".format(machine_name))
            exit()

# Checks for existing chromedriver in directory
if not os.path.exists("./chromedriver"):

    # Attempts unzip using platform
    try:
        platform_action()
    # Unzips using user input
    except:
        inp = str(input("Are you running mac, linux, or windows?: "))
        while (input not in ["mac", "linux", "windows"]):
            inp = str(input("Please try again: (mac), (linux), or (windows)?: "))
        platform_action(plat=inp)

# Delete zip files
# os.system('rm *.zip')

# Get driver
chrome_options = Options()
chrome_options.add_argument("--incognito")
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['acceptSslCerts'] = True
capabilities['acceptInsecureCerts'] = True
if args.headless is not None and args.headless:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless=True
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
driver = webdriver.Chrome("./chromedriver", options=chrome_options, desired_capabilities=capabilities)

# Panera
driver.get("https://delivery.panerabread.com/")
time.sleep(2)
try:
    # Login
    driver.find_element_by_xpath("//a[contains(., 'Sign In')]").click()
    time.sleep(1)
    username_elem = driver.find_element_by_xpath("//input[@placeholder='Email Address'] | //input[@id='signInUsername']")
    time.sleep(1)
    username_elem.clear()
    username_elem.send_keys(args.username)
    password_elem = driver.find_element_by_xpath("//input[@placeholder='Password'] | //input[@id='signInPassword']")
    time.sleep(1)
    password_elem.clear()
    password_elem.send_keys(args.password)
    time.sleep(1)
    submit = driver.find_element_by_xpath("//input[@type='submit'] | //button[@type='submit']")
    driver.execute_script("arguments[0].click();", submit)
except:
    print('\033[93m' + "Could not log in. Please try again." + '\033[0m')
    exit()

#Occasional intermediate screen
time.sleep(2)
try:
    driver.find_element_by_xpath("//span[contains(., 'Rapid')]").click()
except:
    pass
try:
    driver.find_element_by_xpath("//h5[contains(., 'Rapid')]").click()
except:
    pass
try:
    driver.find_element_by_xpath("//a[contains(@title, 'Start an order')]").click()
except:
    pass
time.sleep(2)


first_iter = True
while True: # Bad in practice yet python offers no do-while syntax
    # Send location
    try:
        zip_input = driver.find_element_by_xpath("//input[contains(@placeholder, 'Address, city, zip code, or cafe ID') or contains(@placeholder, 'Find a bakery-cafe with city, state, or zip')]")
        zip_input.clear()
        zip_input.send_keys(args.zip)
        time.sleep(1)
    except:
        print('\033[93m' + "Could not enter zip code. Please try again." + '\033[0m')
        exit()
    try:
        zip_input.send_keys(u'\ue007')
    except:
        pass
    try:
        zip_input.send_keys(Keys.RETURN)
    except:
        pass
    time.sleep(1)

    # Get restaurants nearby
    restaurant_list = driver.find_elements_by_xpath("//div[contains(@class, 'visible')]//div[@id='cafe-list']/div/div[2]/div[@ng-repeat] | //div[@class='cs-cafe-address-list']/div/div/div/div")

    # Petition for user's restaurant, and click it
    print('\033[1m' + "Filtering stores. Please type" + '\033[0m' + '\033[92m' + " yes " + '\033[0m' + '\033[1m' + "to confirm or click the enter button for next store..." + '\033[0m')
    for restaurant in restaurant_list:
        try:
            text = restaurant.find_element_by_xpath(".//span[@class='cafeName'] | ./div/p[@class='cs-cafe-heading']").get_attribute('innerHTML').strip().replace('&nbsp;', ' ')
            button = restaurant.find_element_by_xpath(".//span[@class='cafeName']/../../div[3]/div[2]/a | ./a[contains(@class, 'cs-cafe-selection')]")
            inp = str(input("Is this the correct store? " + text + ": ")).strip() in ["y", "Y", "Yes", "yes"]
            if inp:
                driver.execute_script("arguments[0].click();", button)
                break
        except:
            print('\033[93m' + "Could not get store names. Please try again." + '\033[0m')
            exit()
    else:
        print('\033[93m' + "Those are all the stores! Let's try this again." + '\033[0m')
        first_iter = False
        continue
    break

try:
    # Get food asap
    time.sleep(3)
    driver.find_element_by_xpath("//button[contains(.,'Start Ordering')]").click()
    # Beverages tab
    time.sleep(3)
    driver.find_element_by_xpath("//img[@alt='beverages']/../..").click()
except:
    print('\033[93m' + "Could not navigate to the beverages tab. Please try again." + '\033[0m')
    exit()

for category in driver.find_elements_by_xpath("//parent-category/section"):
    category_text = '\033[1m' + category.find_element_by_xpath("./div/div[1]/*").text + '\033[0m'
    for item in category.find_elements_by_xpath("./div/div[2]/div/div"):
        item_title = item.find_element_by_xpath(".//div[contains(@class, 'title')]").text.replace('&nbsp;', ' ')
        submit = item.find_element_by_xpath(".//span[contains(.,'Add Item')]/..")
        if args.type is not None and args.type==item_title:
            try:
                item.find_element_by_xpath(".//*[contains(., 'Item not available')]")
                print('\033[91m', item_title , '\033[0m', "is out of stock")
                exit()
            except:
                print("Found", item_title, "in stock!")
                item.find_element_by_xpath(".//button[contains(.,'Regular')]").click()
                item.find_element_by_xpath(".//button[contains(.,'Regular')]/../ul/li[contains(.,'Large')]").click()
                submit.click()
                break
    else:
        print("Item type not found in", category_text)
        continue
    break
else:
    print('\033[93m' + "The item {} could not be found on Panera. Please try again.".format(args.type) + '\033[0m')
    exit()

try:
    driver.find_element_by_xpath("//button[contains(.,'Checkout')]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//button[contains(.,'Select Rewards')]").click()
    time.sleep(1)
    driver.find_element_by_xpath("//button[contains(.,'Redeem')]").click()
except:
    print('\033[93m' + "Your My Panera rewards could not be redeemed on the website. Please try again." + '\033[0m')

if driver.find_element_by_xpath("//div[contains(@class,'form-group')]/label[1][contains(., 'Total')]/../label[2]").text != "$0.00":
    print('\033[93m' + "Your total did not come out to $0.00. Maybe you selected an item that is not free. The program will terminate." + '\033[0m')
    exit()

driver.find_element_by_xpath("//textarea[@placeholder='ex. car make/model/color, or red jacket']").send_keys(str(input('\033[1m' + """
Panera is limiting the number of people who can enter their dining rooms.
Tell them how to identify you when you arrive and they will meet you at the door or at your car.
Check your confirmation email for details on picking up at your cafe: \033[0m""".replace('\n', ''))))

#driver.find_element_by_xpath("//input[@type='submit'][@value='Place Your Order']").click()


print("Thanks for using command line coffee. Your free Panera coffee is waiting for you!")
