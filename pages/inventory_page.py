from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    TITLE = (By.XPATH, "//span[@class = 'title']")
    CART_LINK = (By.XPATH, "//a[@class = 'shopping_cart_link']")

# products button add the products now

    Add_BackPack = (By.ID, "add-to-cart-sauce-labs-backpack")
    Add_Fleece_Jacket = (By.ID, "add-to-cart-sauce-labs-fleece-jacket")

    def is_loaded(self):
        return "Products" in self.text_of(self.TITLE)

    def add_products(self):
        self.click(self.Add_BackPack)
        self.click(self.Add_Fleece_Jacket)

    def go_to_cart(self):
        self.click(self.CART_LINK)

#Using data-test means UI changes won’t break your tests.
