import unittest

from selenium import webdriver

prod_url = "http://budgetcalculator-thirdproject.herokuapp.com"
local_url = "http://127.0.0.1:5000/"

# Login page
username_id = "username"
password_id = "password"
login_button_css_selector = "body > div.container-fluid > div > div > div > form > button"
sign_up_css_selector = "body > div.container-fluid > div > div > div > a > button"
sign_up_button_css_selector = "button.btn:nth-child(13)"

# Sign up page
back_button_css_selector = "button.btn:nth-child(1)"
add_group_button_css_selector = "button.btn-success"

# Dashboard items
view_details_button_css_selector = "body > div.table-size > table > tbody > tr:nth-child(2) > td:nth-child(4) > a > button"

# Test user details
testuser_username = "Test_user"
testuser_password = "test"

# Pop-up
add_new_group_button_css_selector = "button.btn-success"

# Edit Group
edit_group_button_css_selector = ".table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(5) > button:nth-child(1)"
edit_group_submit_button_xpath = "/html/body/div[3]/table/tbody/tr[2]/td[5]/div/div/div/div[2]/form/div/input"
edit_group_close_button_xpath = "/html/body/div[3]/table/tbody/tr[2]/td[5]/div/div/div/div[2]/form/div/button"

# Remove Group
remove_group_button_css_selector = ".table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(5) > button:nth-child(1)"
remove_button_xpath = "/html/body/div[3]/table/tbody/tr[2]/td[6]/div/div/div/div[3]/form/input"
remove_close_button_xpath = "/html/body/div[3]/table/tbody/tr[2]/td[6]/div/div/div/div[3]/button"

view_group_item_css_selector = ".table > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(4) > a:nth-child(1) > button:nth-child(1)"

add_new_sub_group_item_css_selector = "button.btn-success"
modify_sub_group_item_css_selector = ".table > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(4) > button:nth-child(1)"
delete_sub_group_item_css_selector = ".table > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(5) > button:nth-child(1)"


class setup_teardown(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')

        # create a new Chrome session
        # At work
        self.driver = webdriver.Chrome(executable_path=r'c:\chromedriver\chromedriver.exe', options=options)
        # At home
        # self.driver = webdriver.Chrome(executable_path=r'c:\chromedriver\chromedriver.exe', chrome_options=options)
        self.driver.implicitly_wait(5)
        # self.driver.maximize_window()
        # navigate to the application home page
        self.driver.get(prod_url)

    def tearDown(self):
        # close the browser window
        self.driver.quit()


def login(self):
    self.driver.find_element_by_id(username_id).send_keys(testuser_username)
    self.driver.find_element_by_id(password_id).send_keys(testuser_password)
    self.driver.find_element_by_css_selector(login_button_css_selector).click()


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
        # Navigate on the sign up page
        self.driver.find_element_by_css_selector(sign_up_css_selector).click()
        # Check the Sign up page url
        assert self.driver.current_url in prod_url + "/sign_up"
        # Check the Sign up elements
        assert self.driver.find_element_by_id("username").is_displayed()
        assert self.driver.find_element_by_id("password").is_displayed()
        assert self.driver.find_element_by_id("password-again").is_displayed()
        assert self.driver.find_element_by_name("currency").is_displayed()
        # Buttons
        assert self.driver.find_element_by_css_selector(sign_up_button_css_selector).is_displayed()
        assert self.driver.find_element_by_css_selector(back_button_css_selector).is_displayed()
        # Click on Back button
        self.driver.find_element_by_css_selector(back_button_css_selector).click()
        assert self.driver.current_url in prod_url + "/"

    # Login function - Arrive to the dashboard
    def test_password(self):
        login(self)
        assert self.driver.current_url in prod_url + "/dashboard"

    def test_dashboard_popups(self):
        login(self)

        # Add Group buttons
        self.driver.find_element_by_css_selector(add_group_button_css_selector).click()
        self.driver.find_element_by_css_selector("input.btn-success").is_displayed()
        self.driver.find_element_by_css_selector(".close-left-add").click()

    #
    def test_edit_group(self):
        login(self)

        # Edit Group buttons
        self.driver.find_element_by_css_selector(edit_group_button_css_selector).click()
        self.driver.find_element_by_xpath(edit_group_submit_button_xpath).is_displayed()
        self.driver.find_element_by_xpath(edit_group_close_button_xpath).click()

    def test_remove_group(self):
        login(self)

        # Remove group buttons
        self.driver.find_element_by_css_selector(remove_group_button_css_selector).click()
        self.driver.find_element_by_xpath(remove_button_xpath).is_displayed()
        self.driver.find_element_by_xpath(remove_close_button_xpath).is_displayed()

    # Landing on the view details page
    def test_view_details_page(self):
        login(self)

        self.driver.find_element_by_css_selector(view_details_button_css_selector).click()
        assert self.driver.current_url in prod_url + "/view_details/2019/September/Income"

    # Landing on the search result page
    def test_search_page(self):
        login(self)
        self.driver.find_element_by_id("search").send_keys("Test")
        self.driver.find_element_by_class_name("fa-search").click()
        assert self.driver.current_url in prod_url + "/search_result"


if __name__ == '__main__':
    unittest.main()
