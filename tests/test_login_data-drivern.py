import csv
import json
from csv import DictReader

import pytest
from pathlib import Path
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
import os

def load_json_data():
#Make a path like: “go to the folder where this script is,
# then into data, then open users.json”.

    path = Path(__file__).parent / "data" / "users.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
#Read the JSON file and turn it into Python data (a list of records).
# Then give it back.


def load_csv_data():
    file_path = os.path.join("tests", "data", login_data.csv")
   # path = Path(__file__).parent / "data" / "users.csv"
    rows = []
    with open(file_path, mode = "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
#Read the CSV where each row becomes a dictionary using the header names.
        for row in reader:
            #Defensive check: skip empty rows and strip white spaces from keys
            row = {k.strip(): v for k, v in row.items() if k is not None}
            if "expected" in row:
                row["expected"] = str(row["expected"]).strip().lower() == "true"
                rows.append(row)
            else:
                print(f"Warnin: 'expected' key missing in row: {row}")
#"Look at the 'expected' column.Clean up any extra spaces and make it lowercase."
            #val = row.get("expected", "").strip().lower()
#"This is a clever check! If the file says 'true', '1', or 'yes', we count it as a success."
            #is_success = val in {"true", "1", "yes", "success", "pass"}
            #outcome = "success" if is_success else "failure"
#"If the check above was true,
# label this as 'success'. Otherwise, label it as 'failure'."
            #rows.append((row["username"], row["password"], outcome))
#Pack the username, password, and our new label into a tiny
# 'gift box' (a tuple) and add it to our list."
    return rows

@pytest.mark.smoke
@pytest.mark.parametrize("record", load_json_data())
#@pytest.mark.parametrize("username,password,expected", load_json_data())
def test_login_data_json(driver, config, record):
    """driver → the browser fixture (Chrome).
config → your settings.
record → one row from JSON."""
#def test_login_data_json(driver, username, password,expected):
    login = LoginPage(driver)
    inv = InventoryPage(driver)
    login.open_login()
    login.login_as(record["username"], record["password"])
    if record["expected"] :
        assert inv.url_contains("inventory"), f"Expected success for {record}"
     #   assert "inventory" in driver.current_url, f"Expected success for {record}"
    else:
    # Check that an error message appears
        from selenium.webdriver.common.by import By
        ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")
        msg = login.text_of(ERROR)
    #We read the text from it: msg.
        assert "Epic sadface" in msg or "locked out" in msg.lower(), f"Expected failure for {record}"
        #err = login.get_error()
        #assert err and ("epic sadface" in err.lower() or "locked out" in err.lower()), \
        #f"Expected failure for {record}, got: {err!r}"

#-------------- CSV-driven test ----------------
@pytest.mark.regression
@pytest.mark.parametrize("record", load_csv_data())
#@pytest.mark.parametrize("username,password,expected", load_csv_data())
#This is like a "Copy-Paste Machine." It tells Pytest:
# "Take every 'gift box' from our list and run the test below using the items inside."
#def test_login_data_csv(driver, username, password,expected):
def test_login_data_csv(driver, config, record):
    login = LoginPage(driver)
    inv = InventoryPage(driver)

    login.open_login()
    login.login_as(record["username"], record["password"])
    if record["expected"] :
        assert "inventory" in driver.current_url, f"Expected success for {record}"
#then make sure the website address changed to the 'inventory' page. If not, the test failed!"
    else:
    # Check that an error message appears
        from selenium.webdriver.common.by import By
        ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")
        msg = login.text_of(ERROR)
        assert "Epic sadface" in msg or "locked out" in msg.lower(), f"Expected failure for {record}"

        # err = login.get_error()
        # assert err and ("epic sadface" in err.lower() or "locked out" in err.lower()), \
        # f"Expected failure for {username}, got: {err!r}"
