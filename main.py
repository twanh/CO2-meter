import os
import time
from datetime import datetime
import schedule 
import pandas as pd
from openpyxl import load_workbook
from sensor import Sensor

# CONSTANTS
EXCEL_FILE_NAME = 'data_test.xlsx'
UPDATE_INTERVAL = 1 # minutej
SENSOR_UUID = "7dfff801-4e6c-5a3e-9bd0-d6cefa79e17a" 

webdriver_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "webdriver", "chromedriver.exe") 


def create_excel_sheet():
  if os.path.isfile(EXCEL_FILE_NAME):
    print(f"{EXCEL_FILE_NAME} already exists.")
    return
  print("Creating excel file with name: ", EXCEL_FILE_NAME)
  df = pd.DataFrame({
    "tijd (s)": [],
    'temperatuur (celcius)': [],
    'luchtvochtigheid (%)': [],
    'luchkwaliteit (ppm)': [],
  })
  writer = pd.ExcelWriter(EXCEL_FILE_NAME, engine="xlsxwriter")
  # writer.save()
  df.to_excel(writer, header=True, startcol=0)
  writer.close()

def update_excel_sheet(time: str, temp: int, hum: int, aq: int):
  print('Updating excel sheet...')
  df = pd.DataFrame({
    'tijd (s)': [time],
    'temperatuur (celcius)': [temp],
    'luchtvochtigheid (%)': [hum],
    'luchkwaliteit (ppm)': [aq],
  })

  writer = pd.ExcelWriter(EXCEL_FILE_NAME, engine='openpyxl')

  writer.book = load_workbook(EXCEL_FILE_NAME)
  writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
  reader = pd.read_excel(EXCEL_FILE_NAME)
  df.to_excel(writer, index=False, header=False,startrow=len(reader)+1)
  writer.close()
  print("Done!")

def update_sensor_job(sensor: Sensor):
  cur_time = datetime.now() 
  cur_time_str = cur_time.strftime("%H:%M:%S")
  print(f"\n\nUpdating the sensor @ {cur_time_str}")
  temp, hum, aq = sensor.update_now()
  print(f"Temperature: {temp} \u2103")
  print(f"Humidity: {hum}%")
  print(f"Air Quality {aq} ppm")
  update_excel_sheet(cur_time_str, temp, hum, aq)

if __name__ == "__main__":

    print("Starting...")

    sensor = Sensor(SENSOR_UUID, webdriver_path)

    schedule.every(UPDATE_INTERVAL).minutes.do(update_sensor_job, sensor)

    create_excel_sheet()


    running = True
    while running:
      try:
        schedule.run_pending() 
        time.sleep(1)
      except KeyboardInterrupt:
        running = False