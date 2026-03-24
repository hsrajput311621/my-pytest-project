import pytest
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from pages.checkout_pages import CheckoutStepOne, CheckoutStepTwo, CheckoutComplete

@pytest.mark.smoke
def test_complete_purchase_success(driver):
    #login page
    login = LoginPage(driver)
    login.open_login()
    login.login_as("standard_user", "secret_sauce")

    # inventory page
    inv = InventoryPage(driver)
    assert inv.is_loaded(), "Inverntory page not loaded after login"
    assert inv.url_contains("inventory"), "URL Not moved to inventory section"

    # add two products
    inv.add_products()
    inv.go_to_cart()

    #cart page
    cart = CartPage(driver)
    cart.assert_loaded()
    cart.go_to_checkout()

    #checkoutStepOne
    step1 = CheckoutStepOne(driver)
    step1.assert_loaded()
    step1.Fill_Form("Hitesh", "Rajput", "110030")
    assert step1.url_contains("checkout-step-two"), "Did not reach step 2"

    # Checkout step two
    step2 = CheckoutStepTwo(driver)
    step2.assert_loaded()
    step2.finish()
    assert step2.url_contains("checkout-complete"), "Did not complete complete page"

    # Complete page
    step3 = CheckoutComplete(driver)
    step3.assert_loaded()
    step3.back_home()
    assert "inventory" in driver.current_url, "Did not return to inventory"




