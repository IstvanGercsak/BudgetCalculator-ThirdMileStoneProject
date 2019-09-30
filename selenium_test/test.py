import unittest

from selenium import webdriver

# https://www.techbeamers.com/selenium-python-test-suite-unittest/

# URL
prod_url = "http://budgetcalculator-thirdproject.herokuapp.com"
local_url = "http://127.0.0.1:5000/"

# Login page
username_id = "username"
password_id = "password"
login_button_css_selector = "body > div.container-fluid > div > div > div > form > button"
sign_up_css_selector = "body > div.container-fluid > div > div > div > a > button"

# Sign up page

# Test user details
testuser_username = "Test_user"
testuser_password = "test"


class setup_teardown(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        # create a new Chrome session
        self.driver = webdriver.Chrome(executable_path=r'c:\chromedriver\chromedriver.exe', chrome_options=options)
        self.driver.implicitly_wait(5)
        # self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get(prod_url)

    def tearDown(self):
        # close the browser window
        self.driver.quit()


class test(setup_teardown):

    def setUp(self):
        super().setUp()

    # Login page field and buttons check
    def test_username(self):
        # username field
        assert self.driver.find_element_by_id(username_id).is_displayed()
        # password field
        assert self.driver.find_element_by_id(password_id).is_displayed()
        # Log in button
        assert self.driver.find_element_by_css_selector(login_button_css_selector).is_displayed()
        # Sign up page button
        assert self.driver.find_element_by_css_selector(sign_up_css_selector).is_displayed()

    # Sign up page
    def test_signup(self):
        self.driver.find_element_by_css_selector(sign_up_css_selector).click()
        assert self.driver.current_url in prod_url + "/sign_up"
        assert self.driver.find_element_by_id("username").is_displayed()
        assert self.driver.find_element_by_id("password").is_displayed()
        assert self.driver.find_element_by_id("password-again").is_displayed()
        assert self.driver.find_element_by_name("currency").is_displayed()

    # Login function - Arrive to the dashboard
    def test_password(self):
        self.driver.find_element_by_id(username_id).send_keys(testuser_username)
        self.driver.find_element_by_id(password_id).send_keys(testuser_password)
        self.driver.find_element_by_css_selector(login_button_css_selector).click()
        assert self.driver.current_url in prod_url + "/dashboard"

    # Landing on the view details page
    def test_view_details_page(self):
        self.driver.find_element_by_id(username_id).send_keys(testuser_username)
        self.driver.find_element_by_id(password_id).send_keys(testuser_password)
        self.driver.find_element_by_css_selector(login_button_css_selector).click()
        self.driver.find_element_by_css_selector(
            "body > div.table-size > table > tbody > tr:nth-child(2) > td:nth-child(4) > a > button").click()
        assert self.driver.current_url in prod_url + "/view_details/2019/September/Income"

    # Landing on the search result page
    def test_search_page(self):
        self.driver.find_element_by_id(username_id).send_keys(testuser_username)
        self.driver.find_element_by_id(password_id).send_keys(testuser_password)
        self.driver.find_element_by_css_selector(login_button_css_selector).click()
        self.driver.find_element_by_id("search").send_keys("Test")
        self.driver.find_element_by_class_name("fa-search").click()
        assert self.driver.current_url in prod_url + "/search_result"


if __name__ == '__main__':
    unittest.main()
