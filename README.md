-v → Show test names clearly
-s → Show print/log outputs
-m smoke → Run only smoke tests

pytest -v -s -m smoke

Run only smoke tests with HTML report
pytest -v -s -m smoke --html=reports/smoke.html --self-contained-html

Run regression with Allure
pytest -v -s -m regression --alluredir=allure-results
allure serve allure-results

pytest -v -s -m smoke --html=reports/report.html --self-contained-html

Reports (pytest‑html & Allure)
pytest -v -s --html=reports/report.html --self-contained-html


Allure (richer, if you want)Run tests and save results:
pytest -v -s --alluredir=allure-results