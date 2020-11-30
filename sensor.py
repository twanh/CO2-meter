from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

import time
from datetime import datetime 

class Sensor:

  def __init__(self, uuid: str, webdriver_path: str, headless=True):

    url = f"https://pulse.strukton.com/comfortsensor/{uuid}"
    self._url = url
    self._uuid = uuid 

    self._webdriver_path = webdriver_path
    self._driver_options = webdriver.ChromeOptions() 
    if headless:
      self._driver_options.add_argument("headless")

    self._wait_time = 5 # Secconds
    self._onload_args = []
    self._last_update = datetime.now() 

    # Update the data when initialized
    # self._update_data()


  def update_now(self):
    """Update and get the lastes values from the sensor

    Returns:
        tuple: (temperature, humidity, air_quality)
    """

    self._update_data()
    return self.temperature, self.humidity, self.air_quality

  def _update_data(self) -> None:
    """Update's the sensor's data

    - Create's a new web driver
    - Reaches out to the sensor and gets value of the onload tag
    - Sets the self._onloads_args variable with the updated value

    """
    # Create a new driver connection
    driver = webdriver.Chrome(executable_path=self._webdriver_path, chrome_options=self._driver_options)
    # Get the URL - Load the page
    driver.get(self._url)
    # Give the page time to load 
    time.sleep(self._wait_time)

    # onload_value is defined up here to be able to access it 
    # outside of the try/catch block
    onload_value = ''

    try:
      # Find the first iframe on the page
      ifame_elem = driver.find_elements_by_tag_name('iframe')[0]
      # Switch the driver to that iframe
      driver.switch_to.frame(ifame_elem)
      # Get the body elements
      body_elem = driver.find_elements_by_tag_name("body")[0]
      # The `onload` attribute contains the value that needs to be parsed
      onload_value = body_elem.get_attribute("onload")
    except NoSuchElementException:
      # TODO: Figure out exception handling!
      print("Iframe could not be found!")
      pass

    # Close the webdriver
    driver.close()

    # Parse the onload value into the args
    # Check it is not empty
    if len(onload_value) > 0:
      self._onload_args = onload_value.split(',')

    # Update the time
    self._last_update = datetime.now() 

  # Sensor Value Getters
  @property
  def temperature(self) -> int:
    """The current temperature measured by the sensor

    Returns:
        int: The temperature in degrees celcius
    """
    if len(self._onload_args) < 1:
      return 0
    # The temperature is the 3th element in the onload_args array
    # The first and last character are quotation marks, so these need to
    # be removed
    return int(self._onload_args[3][1:-1])

  @property
  def humidity(self) -> int:
    """The current humidity measured by the sensor

    Returns:
        int: The air humidity in % 
    """
    if len(self._onload_args) < 1:
      return 0# The humidity value is the 5th element in the onload_args array
    # The first and last character are quotation marks, so these need to
    # be removed
    return int(self._onload_args[5][1:-1])

  @property
  def air_quality(self) -> int:
    """The current air quality measured by the sensor

    Returns:
        int: The air quality in ppm
    """
    if len(self._onload_args) < 1:
      return 0# The air quality value is the 7th element in the onload_args array
    # The first and last character are quotation marks, so these need to
    # be removed and there is alse a ) at the end.
    return int(self._onload_args[7][1:-2])

