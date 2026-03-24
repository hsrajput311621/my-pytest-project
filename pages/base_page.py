# Base Page like a common toolbox for all your pages (Login page, Cart page, Checkout page).
#Instead of writing the same code again and again (like “wait for element”, “click”, “type”), we write it once in Base Page and reuse it everywhere.

from asyncio import timeout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import  logging

logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver, timeout  = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
#Constructor – setting up driver and waiter
#  the maximum waiting time

    def open(self, url):
        self.driver.get(url)
    #Open a website

    def find(self, locators):
        logger.debug(f"FIND element: {locators}")
        return self.wait.until(EC.visibility_of_element_located(locators))
# It waits until the element is visible (can be seen).Then returns the element. Find an element safely

    def click(self, locators):
        logger.info(f"CLICK element : {locators}")
        self.wait.until(EC.element_to_be_clickable(locators)).click()
#Waits until the element is clickable ; Click a button safely

    def type(self, locators, text):
        logger.info(f"TYPE into {locators}: '{text}'")
        el = self.find(locators)
        el.clear()
        el.send_keys(str(text))

#First, find the element (waits until visible). Type into an input box safely
#Then clear old text.
#Then type your text.
#str(text) makes sure numbers like 110030 also work.

    def text_of(self, locators):
        txt = self.find(locators).text
        logger.debug(f"TEXT of {locators}: '{txt}'")
        return txt
#Read text from an element
#Finds the element and returns its text (like reading the label: “Your Cart”).

    def url_container(self, fragment):
        logger.info(f"WAIT URL contains: {fragment}")
        return self.wait.until(EC.url_contains(fragment))

# Wait until the URL contains something
#Example: after login, URL should contain "inventory".
#This waits until that happens.