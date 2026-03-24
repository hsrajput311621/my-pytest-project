from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    TITLE = (By.XPATH, "//span[@class = 'title']")
    CHECKOUT_BTN = (By.ID,"checkout")

    def assert_loaded(self):
        assert "Your Cart" in self.text_of(self.TITLE), "Cart is Missing"

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BTN)

