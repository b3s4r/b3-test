from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

t0 = time.time()

opts = webdriver.ChromeOptions()
opts.headless = True

port = sys.argv[1]
executor = 'http://localhost:' + port
print(executor)

#driver = webdriver.Chrome(options = opts)
driver = webdriver.Remote(command_executor=executor, options = opts)
t1 = time.time()
print('connect', t1 - t0)


driver.get("https://www.python.org")
assert "Python" in driver.title

t2 = time.time()
print('get', t2 - t1)

elem = driver.find_element_by_name("q")

elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

print('test', time.time() - t2)

assert "No results found." not in driver.page_source
driver.close()
