from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import os
import requests

GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSfq-5amsbi-iKMcpmVOOX4Vr5dTL6y13QkrcX1gbHR8jier5g/viewform?usp=sf_link"
ZILLOW_HOMEPAGE = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22%3A37.59760327847264%2C%22north%22%3A37.952553591859726%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
CHROME_WEB_DRIVER = os.environ.get("CHROME_DRIVER_PATH")

pause = time.sleep(1)
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7"

}
response = requests.get(ZILLOW_HOMEPAGE, headers=headers)
response.raise_for_status()

# Get the price, address and link to all the listings
zillow_homepage = response.text
soup = BeautifulSoup(zillow_homepage, "html.parser")

all_links = []
all_prices = []

all_addresses_search = soup.findAll("address", class_="list-card-addr")

all_addresses = [address.getText() for address in all_addresses_search]

all_links_search = soup.findAll("a", class_="list-card-img")

for article in all_links_search:
    link = article.get("href")
    if "https://www.zillow.com" not in link:
        link = f"https://www.zillow.com{link}"
    all_links.append(link)

all_prices_search = soup.findAll("div", class_="list-card-price")

for article in all_prices_search:
    price = article.getText().split()[0]
    if "/mo" in price:
        price = price.replace("/mo", "")
    if "+" in price:
        price = price.replace("+", "")
    all_prices.append(price)


# Put the data in google form

def find_xpath_element(xpath):
    is_found = False
    element = None
    while not is_found:
        try:
            element = driver.find_element_by_xpath(xpath)
            is_found = True
        except NoSuchElementException:
            time.sleep(2)
            pass
    return element


driver = webdriver.Chrome(executable_path=CHROME_WEB_DRIVER)

for n in range(len(all_addresses)):
    driver.get(GOOGLE_FORM_LINK)

    time.sleep(3)

    entry_address = find_xpath_element('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    entry_address.send_keys(all_addresses[n])
    time.sleep(1)

    entry_price = find_xpath_element('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    entry_price.send_keys(all_prices[n])
    time.sleep(1)

    entry_link = find_xpath_element('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    entry_link.send_keys(all_links[n])
    time.sleep(1)

    confirm_button = find_xpath_element('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    confirm_button.click()
