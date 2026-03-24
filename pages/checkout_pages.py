from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutStepOne(BasePage):
    TITLE = (By.XPATH, "//span[@class = 'title']")
    CONTINUE_BTN = (By.ID, "continue")
    FIRSTNAME = (By.ID, "first-name")
    LASTNAME = (By.ID, "last-name")
    POSTAL = (By.ID, "postal-code")

    def assert_loaded(self):
        assert "Checkout: Your Information" in self.text_of(self.TITLE), "Not on Step One"

    def Fill_Form(self, first, last, zip_code):
        self.type(self.FIRSTNAME, first)
        self.type(self.LASTNAME,last)
        self.type(self.POSTAL, zip_code)
        self.click(self.CONTINUE_BTN)

class CheckoutStepTwo(BasePage):
    TITLE = (By.XPATH, "//span[@class = 'title']")
    Finished_btn = (By.ID, "finish")
    Payment_info = (By.XPATH, "//div[normalize-space() = 'Payment Information:']")

    def assert_loaded(self):
        assert "Checkout: Overview" in self.text_of(self.TITLE), "Not on Step Two"
        assert "Payment Information:" in self.text_of(self.Payment_info), "Payment info missing"

    def finish(self):
        self.click(self.Finished_btn)

class CheckoutComplete(BasePage):
    TITLE = (By.XPATH, "//span[@class = 'title']")
    SuccessMessage = (By.XPATH, "//h2[normalize-space() = 'Thank you for your order!']")
    Back_Home = (By.ID, "back-to-products")

    def assert_loaded(self):
        assert "Checkout: Complete!" in self.text_of(self.TITLE), "Checkout Failed to Complete"
        assert "Thank you for your order!" in self.text_of(self.SuccessMessage), "Success message missing"

    def back_home(self):
        self.click(self.Back_Home)
