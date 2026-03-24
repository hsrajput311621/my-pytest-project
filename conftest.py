from logging import INFO

import pytest
from fontTools.misc.timeTools import timestampNow
from requests import session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.ie.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

import json
import logging
import os
from datetime import datetime
from pathlib import Path


#@----------config fixture----------------------#
@pytest.fixture(scope="session")
def config():
    """
        Reads config.json once and shares it with all tests.
        """
    cfg_path = Path(__file__).parent / "config.json"
    with open(cfg_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


# encoding="utf-8:It tells Python, “Please read this file using the UTF-8 alphabet,
# which can handle all kinds of characters (like Hindi, emojis, symbols).
# data = json.load(f): reads the file (which has JSON text) and turns it into Python data
# (like a dictionary).
# Open the file at cfg_path  and : "r" means “open it to read.
# as f gives the opened file a short name f so we can use it.
#Path(__file__).parent : means “the folder where this file lives.”

# ---------- LOGGING SETUP ----------

#This is a pytest decorator (a special tag) that turns the function into a fixture.
#scope="session" → Run this once for the whole test run (not for every test).
#autouse=True → Run this automatically without us asking for it in tests.

@pytest.fixture(scope="session", autouse=True)
def configure_logging():

    """
    Creates logs folder and configures root logger once.
    """
#Path("logs") means: “Point to a folder named logs in the current place.”
#We save that path in a variable called logs_dir.
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
#exist_ok=True means: “If the folder already exists, don’t crash, it’s okay.”
#So this line creates the logs folder if it’s not there.
    log_file = logs_dir / f"run_{datetime().now().strftime('y%m%d_%H%M%S')}.log"
#datetime.now() → get the current date and time.
# .strftime('%Y%m%d_%H%M%S') → format it like 20260323_105530 (YearMonthDay_HourMinuteSecond).
# f"run_{...}.log" → make a file name like run_20260323_105530.log.
# logs_dir / <filename> → put the file inside the logs folder.
# So log_file becomes something like:
# logs/run_20260323_105530.log

#We are setting up the logging system with some options:
#This decides what to log, how it looks, and where to save it.

    logging.basicConfig(
        level = logging.INFO,
#This says: “Record messages that are INFO level and above.”
#DEBUG < INFO < WARNING < ERROR < CRITICAL.

# """This controls how each log line looks.
#  %(asctime)s → time when the log happened.
#  %(levelname)s → level like INFO/WARNING/ERROR.
#  %(name)s → which logger sent it.
#  %(message)s → the actual message text.
#  Example log line:
# 2026-03-23 10:55:30,123 | INFO | my_test | Starting checkout flow """
        format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
#Handlers decide where the logs go.
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
#Also show logs in the console (the terminal window).
        ],
    )
    logging.getLogger("selenium").setLevel(logging.warning())
# Some libraries print too many logs (like Selenium).
# This line says: “For the logger named selenium, only show WARNING and above.”
    return log_file

'''This fixture runs once at the start of all tests, makes a logs folder,
# creates a timestamped log file, sets up logging to go both to the file and the console,
# and reduces noisy logs from Selenium'''

# ---------- BROWSER FIXTURE ----------

''' This is a pytest decorator (a special sticker) that tells pytest:
# “The thing below is a fixture.”
# A fixture is like a helper that sets up something before a test and cleans it up after'''

@pytest.fixture()
def driver(config):

    """
    Creates Chrome based on config flags, returns driver, and quits after test.
    """
    options = Options()
# We create an Options object.

    if config.get("headless", False):
        options.add_argument("--headless=new")
        options.add_argument("--indow-size=1920,1080")

    if config.get("incognito", True):
        options.add_argument("--incognito")

    if config.get("disable_notifications", True):
        options.add_argument("--disable_notifications")
# Turn off annoying browser pop-up notifications that can block buttons in tests.

    if config.get("start_maximized", True):
        options.add_argument("--start_maximized")

# modern selenium can auto-manage the driver (no Service needed)

    driver = WebDriver.Chorme(options = options)
#Start a Chrome browser using all the options we added.
#Save it in a variable called driver.

    driver.implicitly_wait(0)
    yield driver
#yield driver :  gives the driver to the test to use.
    driver.quit()

#This fixture creates a Chrome browser using settings from config.json,
''''# gives it to the test, and shuts it down at the end—using good defaults
(incognito, no notifications, maximized, explicit waits)'''

'''
For CI: add --no-sandbox and --disable-dev-shm-usage when running in Linux containers
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

'''
# ---------- SCREENSHOT ON FAILURE + REPORT ATTACH ----------

'''It tells Pytest,I want to wrap my arms around the test."It lets the test run first,
   but stays close enough to see the result the moment it's finished.
   (hookwrapper=True : we wrap around pytest’s work — we let pytest do its job first, 
   then we do extra stuff after.(Think: “Let pytest run, then I’ll check what happened and act.”).'''

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_logreport(report):
    """This is the hook function.
Pytest calls this to create a report for each test phase.
item = the test item (info about the test).
call = details about the test phase that ran (setup/call/teardown).
fter each test phase, if it failed, take screenshot and attach to reports"""
    yield
    """Because we used hookwrapper=True, we must yield first.
    This lets pytest run its own logic.
    After pytest is done, we get back an outcome (result)."""
    if report.when != "call": return
    """Tests have a "Warm-up" (setup) and a "Clean-up" (teardown). 
    This line says: "If the failure happened during warm-up, I don't care. 
    I only want to take a photo if the failure
     happened during the actual race (the 'call')."""
    if report.failed:
        #If the test body failed, then we continue.
        #If it passed, we skip the screenshot steps.
        driver = item.funcargs.get("driver", None)
        #item.funcargs holds the fixtures used by this test.
        #We try to find the driver fixture (the Selenium browser).
        #If it’s there, we can take a screenshot. If not, we can’t.
        if driver:
            #Only do the screenshot work if we actually got a driver.
            ss_dir = Path("screenshot")
            #Path("screenshots") points to a folder named screenshots.
            ss_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.name.replace("/","_").replace("\\","_")
            ss_path = ss_dir /f"{test_name}_{timestamp}.png"
            """timestamp = current date/time like 20260323_112045.
test_name = the test’s name, but we replace / and \ so it’s safe for file names.
ss_path = screenshots/<test_name>_<timestamp>.png
(Example: screenshots/test_login_20260323_112045.png)"""
            try:
                driver.save_screenshot(str(ss_path))
                logging.getLogger(__name__).info(f"Saved Screenshot: {ss_path}")
            except Exception as e:
                logging.getLogger(__name__).exception(f"Failed to save screenshot: {e}")
                """driver.save_screenshot(...) → ask the browser to take a picture and save it.
                    If it works, we log “Saved screenshot …”.
                    If it fails (maybe driver is gone), we log an exception with the error message"""

            # Attach to pytest-html if plugin is active
            if item.config.pluginmanager.hasplugin("html"):
                from pytest_html import extras
                extra = getattr(rep, "extra", [])
                extra.append(extras.image(str(ss_path)))
                rep.extra = extra
                """Check if pytest-html plugin is active.
                If yes:
                Import helper extras.
                Get the current rep.extra list (or empty list).
                Add our image (screenshot).
                Put the list back into rep.extra.
                Result: The HTML test report will show the screenshot for the failed test."""

            # Attach to Allure if plugin is active
            if item.config.pluginmanager.hasplugin("allure-pytest"):
                try:
                    import allure
                    from allure_commons.types import AttachmentType
                    with open(ss_path, "rb") as f:
                        allure.attach(
                            f.read(),
                            name=f"Screenshot_{test_name}",
                            attachment_type=AttachmentType.PNG
                        )
                except Exception as e:
                    logging.getLogger(__name__).warning(f"Allure attach failed: {e}")

            """Check if Allure plugin is active.
            If yes:Open the screenshot file in binary mode ("rb").
            Use allure.attach(...) to add it to the Allure report with a friendly name.
            If something goes wrong, we log a warning (don’t crash the test run)."""
#After each test body finishes, if it failed, this hook takes a screenshot,
# saves it with a timestamped name, and attaches it to reports
# (pytest-html and/or Allure if they’re installed).


"""

    Fixture (The Equipment): To give something to the test (like a Browser).
                        : The test has to ask for it by name: def test_login(driver):
                        : Runs before or after a specific test.
    Hook (The Referee)  : To watch or change how Pytest works.
                        : It happens in the background.The test doesn't even know it's there!
                        :Can run at special times, like "exactly when the report is being made."





"""






