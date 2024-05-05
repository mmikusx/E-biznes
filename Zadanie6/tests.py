import unittest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import requests


class TestWebsite(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_right_click_popup(self):
        self.driver.get('https://the-internet.herokuapp.com/context_menu')

        element_to_right_click = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'hot-spot'))
        )

        action = ActionChains(self.driver)
        action.context_click(element_to_right_click).perform()

        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            self.fail("Test failed")

    def test_checkboxes(self):
        self.driver.get('https://the-internet.herokuapp.com/checkboxes')

        checkboxes = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'input[type="checkbox"]'))
        )

        checkboxes[0].click()

        self.assertTrue(checkboxes[0].is_selected(), "Test failed")

    def test_dropdown(self):
        self.driver.get('https://the-internet.herokuapp.com/dropdown')

        dropdown = Select(WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'dropdown'))
        ))

        dropdown.select_by_value('1')

        selected_option = dropdown.first_selected_option
        self.assertEqual(selected_option.get_attribute('value'), '1', "Test failed")

    def test_status_code_200(self):
        self.check_status_code('200')

    def test_status_code_301(self):
        self.check_status_code('301')

    def test_status_code_404(self):
        self.check_status_code('404')

    def test_status_code_500(self):
        self.check_status_code('500')

    def check_status_code(self, code):
        self.driver.get('https://the-internet.herokuapp.com/status_codes')

        link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, code))
        )
        link.click()

        response = requests.get(self.driver.current_url)
        self.assertEqual(response.status_code, int(code), "Test failed")

    def test_js_alert(self):
        self.driver.get('https://the-internet.herokuapp.com/javascript_alerts')

        button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Click for JS Alert"]'))
        )
        button.click()

        alert = self.driver.switch_to.alert
        alert.accept()

        result = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'result'))
        )
        self.assertEqual(result.text, "You successfully clicked an alert", "Test failed")

    def test_js_confirm(self):
        self.driver.get('https://the-internet.herokuapp.com/javascript_alerts')

        button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Click for JS Confirm"]'))
        )
        button.click()

        alert = self.driver.switch_to.alert
        alert.dismiss()

        result = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'result'))
        )
        self.assertEqual(result.text, "You clicked: Cancel", "Test failed")

    def test_js_prompt(self):
        self.driver.get('https://the-internet.herokuapp.com/javascript_alerts')

        button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Click for JS Prompt"]'))
        )
        button.click()

        alert = self.driver.switch_to.alert
        alert.send_keys('123')
        alert.accept()

        result = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'result'))
        )
        self.assertEqual(result.text, "You entered: 123", "Test failed")

    def check_hover(self):
        self.driver.get('https://the-internet.herokuapp.com/hovers')

        figures = WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.figure'))
        )

        action = ActionChains(self.driver)
        action.move_to_element(figures[0]).perform()

        figcaption = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.figure .figcaption'))
        )
        self.assertTrue(figcaption.is_displayed(), "Test failed")

    def test_invalid_login(self):
        self.driver.get('https://the-internet.herokuapp.com/login')

        username = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        password = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )

        username.send_keys('Login')
        password.send_keys('Haslo')

        login_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        login_button.click()

        error_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'flash'))
        )
        self.assertTrue("Your username is invalid!" in error_message.text, "Test failed")

    def test_valid_login(self):
        self.driver.get('https://the-internet.herokuapp.com/login')

        username = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        password = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'password'))
        )

        username.send_keys('tomsmith')
        password.send_keys('SuperSecretPassword!')

        login_button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        login_button.click()

        success_message = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'flash'))
        )
        self.assertTrue("You logged into a secure area!" in success_message.text, "Test failed")

    def test_floating_menu(self):
        self.driver.get('https://the-internet.herokuapp.com/floating_menu')

        home_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Home'))
        )
        home_link.click()

        self.assertTrue(self.driver.current_url.endswith('#home'), "Test failed")

    def test_key_presses(self):
        self.driver.get('https://the-internet.herokuapp.com/key_presses')

        input_field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'target'))
        )
        input_field.send_keys('A')

        result = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'result'))
        )
        self.assertEqual(result.text, "You entered: A", "Test failed")

    def test_new_window(self):
        self.driver.get('https://the-internet.herokuapp.com/windows')

        link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Click Here'))
        )
        link.click()

        WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))

        self.driver.switch_to.window(self.driver.window_handles[-1])

        WebDriverWait(self.driver, 10).until(EC.url_to_be('https://the-internet.herokuapp.com/windows/new'))

        self.assertEqual(self.driver.current_url, 'https://the-internet.herokuapp.com/windows/new', "Test failed")

    def test_notification_message(self):
        self.driver.get('https://the-internet.herokuapp.com/notification_message_rendered')

        link = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="Click here" and @href="/notification_message"]'))
        )
        link.click()

        message = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, 'flash'))
        )
        self.assertTrue("Action successful" in message.text, "Test failed")

    def test_redirector(self):
        self.driver.get('https://the-internet.herokuapp.com/redirector')

        link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'here'))
        )
        link.click()

        WebDriverWait(self.driver, 5).until(EC.url_to_be('https://the-internet.herokuapp.com/status_codes'))

        self.assertEqual(self.driver.current_url, 'https://the-internet.herokuapp.com/status_codes', "Test failed")

    def test_dynamic_loading(self):
        self.driver.get('https://the-internet.herokuapp.com/dynamic_loading/2')

        start_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Start"]'))
        )
        start_button.click()

        message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="finish"]/h4[text()="Hello World!"]'))
        )
        self.assertTrue(message.is_displayed(), "Test failed")

    def test_disappearing_elements(self):
        self.driver.get('https://the-internet.herokuapp.com/disappearing_elements')

        about_link = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'About'))
        )
        about_link.click()

        with self.assertRaises(TimeoutException):
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'About'))
            )

    def test_image_location(self):
        self.driver.get('https://the-internet.herokuapp.com/shifting_content/image')

        image = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        )
        location_before_refresh = image.location

        self.driver.refresh()

        image = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'img'))
        )
        location_after_refresh = image.location

        self.assertEqual(location_before_refresh, location_after_refresh, "Test failed")


if __name__ == "__main__":
    unittest.main()
