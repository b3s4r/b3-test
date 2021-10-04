from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import unittest
import sys


maybe_port = None


def connect_driver():
    t0 = time.time()

    caps = DesiredCapabilities.CHROME.copy()
    #caps["debuggerAddress"] = "localhost"

    opts = webdriver.ChromeOptions()
    opts.headless = True
    opts.debugger_address = "localhost:9222"
    #opts.add_argument("--incognito")
    #opts.add_argument("--no-proxy-server")

    port = '9515'
    if maybe_port != None:
        port = maybe_port

    executor = 'http://localhost:' + port
    print(executor)

    #driver = webdriver.Chrome(options = opts)
    driver = webdriver.Remote(command_executor=executor, options = opts, desired_capabilities = caps)
    print(driver.desired_capabilities)
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
        #driver.close()



class TestAftonbladet(unittest.TestCase):
    def setUp(self):
        self.wd = connect_driver()
        self.wd.get('https://www.aftonbladet.se')

    def tearDown(self):
        #self.wd.close()
        pass

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
        #self.wd.close()
        pass

    def find_age_confirmation(self):
        try:
            return self.wd.find_element_by_class_name('age-confirmation')
        except:
            return None

    def test_age_confirmation(self):
        # Age confirmation should always be shown on the first load
        # but then hidden on all subsequent loads. When shown and clicked
        # it should be hidden.
        confirm = self.find_age_confirmation()
        btn = confirm.find_element_by_tag_name('button')
        btn.click()

        c2 = None
        for i in range(10):
            c2 = self.find_age_confirmation()

        self.assertIsNone(c2)

        self.wd.get('https://www.whitepouches.com')
        c3 = self.find_age_confirmation()

        self.assertIsNone(c3)


if __name__ == '__main__':
    # the second passed argument might me the port; if so then we need to remove
    # if from sys.argv or it break the assumption in unittest.main(...)
    if len(sys.argv) > 1:
        # if port then the first argument after the binary name
        # should be a port; so let's try to parse it as an int.
        try:
            port = int(sys.argv[1])
            maybe_port = sys.argv[1]
            sys.argv.pop(1)
            print('modified sys.argv to work with unittest.main(...)')
        except:
            # parse failed, ok to ignore? I think :)
            pass


    unittest.main(warnings='ignore')
