from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import platform, exit
import os
import zipfile
import time
import argparse

parser = argparse.ArgumentParser(description='Get Panera Coffee.')
parser.add_argument('--username', help='My Panera Username')
parser.add_argument('--password', help='My Panera Password')
args = parser.parse_args()

exit()
# Returns the correct zip file name based on plat (defaults to system platform)
def platform_action(plat=platform, write_permissions=False):
    if plat=="mac" or plat=="darwin":
        if write_permissions:
            os.system("chmod 755 chromedriver")
        else:
            return "chromedriver_mac64.zip"
    elif plat=="win32" or plat=="windows":
        if write_permissions:
            pass
        else:
            return "chromedriver_win32.zip"
    elif plat=="linux" or plat=="linux2":
        if write_permissions:
            pass
        else:
            return "chromedriver_linux64.zip"
    raise Error("The platform wasn't recognized, and a local zip file could not be chosen for your chromedriver.")

# Checks for existing chromedriver in directory
if not os.path.exists("./chromedriver"):

    # Attempts unzip using platform
    try:
        local_file = platform_action()
    # Unzips using user input
    except:
        inp = str(input("Are you running mac, linux, or windows?: "))
        while (input not in ["mac", "linux", "windows"]):
            inp = str(input("Please try again: (mac), (linux), or (windows)?: "))
        local_file = platform_action(inp)

    with zipfile.ZipFile(local_file,"r") as zip_ref:
        zip_ref.extractall()

    try:
        inp
    except NameError:
        platform_action(write_permissions=True)
    else:
        platform_action(plat=inp, write_permissions=True)


# Delete zip files
# os.system('rm *.zip')


driver = webdriver.Chrome("./chromedriver")
# Aesthetic coffee url
driver.get("https://www.panerabread.com/en-us/mypanera/mypanera-coffee-subscription.html")
time.sleep(2)
# Entering auth page
driver.get("https://www.panerabread.com/en-us/app/subscription/registration.html")

time.sleep(1)
driver.find_element_by_xpath("//input[@id='signInUsername']").send_keys(args.username)
driver.find_element_by_xpath("//input[@id='signInPassword']").send_keys(args.password)
driver.find_element_by_xpath("//button[@type='submit']").click()


time.sleep(3)
try:
    driver.find_element_by_xpath("//button[@title='Start an order']").click()
except:
    pass
time.sleep(2)
try:
    driver.find_element_by_xpath("//h5[contains(@class, 'text-left') and contains(., 'Rapid')]").click()
except:
    pass


time.sleep(2)
zip_input = driver.find_element_by_xpath("//input[@placeholder='Address, city, zip code, or cafe ID']")
zip_input.send_keys("43221")

time.sleep(1)
try:
    zip_input.send_keys(u'\ue007')
except:
    pass
try:
    zip_input.send_keys(Keys.RETURN)
except:
    pass


time.sleep(2)
restaurant_list = driver.find_element_by_xpath("//div[@class='cs-cafe-address-list']/div/div")

print('\033[1m' + "Filtering stores. Please type" + '\033[0m' + '\033[92m' + " yes " + '\033[0m' + '\033[1m' + "to confirm or click the enter button for next store..." + '\033[0m')
for restaurant in restaurant_list.find_elements_by_xpath("./div"):
    text = restaurant.find_element_by_xpath(".//div//p[@class='cs-cafe-heading']/span[1]").text
    button = restaurant.find_element_by_xpath("./div/a")
    inp = str(input("Is this the correct store? " + text + ": ")) in ["y", "Y", "Yes", "yes"]
    print(inp)
    if inp:
        button.click()
        break

driver.find_element_by_xpath("//button[contains(., 'Select this cafe')]").click()
driver.find_element_by_xpath("//a[@title='ASAP - About 5 - 10 minutes after checkout']").click()
driver.find_element_by_xpath("//a[@title='Beverages']").find_element_by_xpath('..').click()
