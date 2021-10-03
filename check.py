from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest
import sys


def connect_driver():
    t0 = time.time()

    opts = webdriver.ChromeOptions()
    #opts.headless = True
    opts.add_argument("--incognito")

    port = '9515'
    if len(sys.argv) > 1:
        port = sys.argv[1]

    executor = 'http://localhost:' + port
    print(executor)

    #driver = webdriver.Chrome(options = opts)
    driver = webdriver.Remote(command_executor=executor, options = opts)
    t1 = time.time()
    print('connect', t1 - t0)
    return driver


class TestPythonOrg(unittest.TestCase):
    def test_end_to_end(self):
        driver = connect_driver()
        t1 = time.time()

        driver.get('https://www.python.org')
        assert 'Python' in driver.title

        t2 = time.time()
        print('get', t2 - t1)

        elem = driver.find_element_by_name('q')

        elem.clear()
        elem.send_keys('pycon')
        elem.send_keys(Keys.RETURN)

        print('test', time.time() - t2)

        assert 'No results found.' not in driver.page_source
        driver.close()



class TestAftonbladet(unittest.TestCase):
    def setUp(self):
        self.wd = connect_driver()
        self.wd.get('https://www.aftonbladet.se')

    def tearDown(self):
        self.wd.close()

    def test_get_content(self):
        # OK as long as the section contains some elements in the main section.
        section = self.wd.find_element_by_tag_name('section')
        divs = section.find_elements_by_tag_name('div')
        self.assertNotEqual(0, len(divs))

        # OK as long as the side panel have some elements.
        side = self.wd.find_element_by_tag_name('aside')
        divs = side.find_elements_by_tag_name('div')
        self.assertNotEqual(0, len(divs))



class TestWhitePouches(unittest.TestCase):
    def setUp(self):
        self.wd = connect_driver()
        self.wd.get('https://www.whitepouches.com')

    def tearDown(self):
        self.wd.close()

    def test_age_confirmation(self):
        confirm = self.wd.find_element_by_class_name('age-confirmation')
        btn = confirm.find_element_by_tag_name('button')
        btn.click()

        # print(c0)

        # confirmation = WebDriverWait(self.wd, 3).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "age-confirmation"))
        # )

        #confirmation.find_element_by_class_name(


if __name__ == '__main__':
    unittest.main(warnings='ignore')
