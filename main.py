import os
import time
from datetime import datetime
import schedule 
from sensor import Sensor

webdriver_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "webdriver", "chromedriver.exe") 

def update_sensor_job(sensor: Sensor):
  cur_time = datetime.now() 
  cur_time_str = cur_time.strftime("%H:%M:%S")
  print(f"Updating the sensor @ {cur_time_str}")
  sensor.update_now()


if __name__ == "__main__":

    uuid = "7dfff801-4e6c-5a3e-9bd0-d6cefa79e17a" 
    sensor = Sensor(uuid, webdriver_path, headless=False)

    schedule.every(5).minutes.do(update_sensor_job, sensor)

    running = True
    while running:
      try:
        schedule.run_pending() 
        time.sleep(1)
      except KeyboardInterrupt:
        running = False