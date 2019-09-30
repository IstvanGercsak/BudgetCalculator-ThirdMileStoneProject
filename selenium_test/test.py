import unittest

from selenium import webdriver

# https://www.techbeamers.com/selenium-python-test-suite-unittest/

prod_url = "https://budgetcalculator-thirdproject.herokuapp.com"
local_url = "http://127.0.0.1:5000/"

username_id = "username"
password_id = "password"


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(inst):
        # create a new Chrome session
        inst.driver = webdriver.Chrome(executable_path=r'c:\chromedriver\chromedriver.exe')
        inst.driver.implicitly_wait(15)
        inst.driver.maximize_window()
        # navigate to the application home page
        inst.driver.get(local_url)

    @classmethod
    def tearDownClass(inst):
        # close the browser window
        inst.driver.quit()

    # Login page
    def test_username(self):
        assert self.driver.find_element_by_id(username_id).is_displayed()

    # Login page
    def test_password(self):
        assert self.driver.find_element_by_id(password_id).is_displayed()

    # Login page
    def test_asd(self):
        self.assertEqual(self.driver.find_element_by_class_name("nav-header-title").get_property(), "asd")


if __name__ == '__main__':
    unittest.main()
