from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    Username = (By.ID, "user-name")
    Password = (By.ID, "password")
    Login_btn = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "h3[data-test = 'error']")
    #            By.CSS_SELECTOR,  "tag[attribut_name = 'value']"
    def open_login(self):
        self.open(self.URL)


    def login_as(self, username, password):
        self.type(self.Username, username)
        self.type(self.Password, password)
        self.click(self.Login_btn)

    def get_error(self):
        if self.is_visible(self.ERROR_MSG):
            return self.text_of(self.ERROR_MSG)
        return  ""


