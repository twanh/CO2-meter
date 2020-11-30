import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup


url = "https://pulse.strukton.com/comfortsensor/7dfff801-4e6c-5a3e-9bd0-d6cefa79e17a"
webdriver_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "webdriver", "chromedriver.exe") 

if __name__ == "__main__":
  driver = webdriver.Chrome(executable_path=webdriver_path)
  driver.get(url)
  # Load time
  time.sleep(5)

  onload_value = ''


  # Get the contents of the iframe
  try:
    ifame_elem = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(ifame_elem)
    ifame_src = driver.page_source
    print(ifame_src)
    body_elem = driver.find_elements_by_tag_name("body")[0]
    # Save it to onload value, so that it can be used later, 
    # (we need to close the driver a soon as possuble)
    onload_value = body_elem.get_attribute("onload")
  except NoSuchElementException:
    print("Iframe could not be found!")
    pass

  driver.close()

  # Parse the onload value
  onload_args = onload_value.split(',')

  # Function signature is: 
  # function setValues(uuid,atime,itemp, vtemp, ihum, vhum, ico, vco) 
  # ["setValues('7dfff801-4e6c-5a3e-9bd0-d6cefa79e17a'", '0', '4', "'17'", '1', "'39'", '1', "'506')"]

  uuid = onload_args[0].split("'")[1]
  atime = onload_args[1]
  itemp = onload_args[2]
  vtemp = onload_args[3][1:-1]
  ihum = onload_args[4]
  vhum = onload_args[5][1:-1]
  ico = onload_args[6]
  vco = onload_args[7][1:-2]


  print(onload_args)

  print("UUID:", uuid)
  print("ATIME:", atime)
  print("ITEMP:", itemp)
  print("VTEMP:", vtemp) # THe actual temperature
  print("IHUM:", ihum)
  print("VHUM:", vhum) # Percentage humidity
  print("ICO:", ico)
  print("VCO:", vco) # Air quality