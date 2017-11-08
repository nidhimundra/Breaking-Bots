from selenium import webdriver

from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

path_to_geckodriver = '/home//vshejwalkar/Documents/Breaking-Bots/geckodriver' # change path as needed
browser = webdriver.Firefox(executable_path = path_to_geckodriver)
url = 'https://people.cs.umass.edu/~amir/'
browser.get(url)
# browser.get_screenshot_as_file("capture.png")

continue_link = browser.find_element_by_tag_name('a')
elems = browser.find_elements_by_xpath("//a[@href]")

for elem in elems:
    print elem.get_attribute("href")
browser.quit()
display.stop()