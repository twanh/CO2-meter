import os
import time
import argparse
from datetime import datetime
import schedule
import pandas as pd
from openpyxl import load_workbook
from sensor import Sensor

# CONSTANTS
EXCEL_FILE_NAME = 'data_test.xlsx'

webdriver_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "webdriver", "chromedriver.exe")

arguments_parser = argparse.ArgumentParser()
arguments_parser.add_argument('uuid', help="De UUID van de sensor")
arguments_parser.add_argument('output',  help="Het excel bestand waarin de metingen moeten worden opgeslagen")
arguments_parser.add_argument("interval",  default=5, help="De interval tussen de metingen")

def create_excel_sheet():
  if os.path.isfile(EXCEL_FILE_NAME):
    print(f"{EXCEL_FILE_NAME} already exists.")
    return
  print("Creating excel file with name: ", EXCEL_FILE_NAME)
  df = pd.DataFrame({
    "tijd (HH:MM:SS)": [],
    'temperatuur (celcius)': [],
    'luchtvochtigheid (%)': [],
    'luchkwaliteit (ppm)': [],
  })
  writer = pd.ExcelWriter(EXCEL_FILE_NAME, engine="openpyxl")
  # writer.save()
  df.to_excel(writer, header=True, startcol=0)
  writer.close()
  print("Done!")

def update_excel_sheet(time: str, temp: int, hum: int, aq: int):
  print('Updating excel sheet...')
  df = pd.DataFrame({
    'tijd (HH:MM:SS)': [time],
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

    args = arguments_parser.parse_args()
    EXCEL_FILE_NAME = args.output
    print("Starting...")

    sensor = Sensor(args.uuid, webdriver_path)

    schedule.every(int(args.interval)).minutes.do(update_sensor_job, sensor)

    create_excel_sheet()


    running = True
    while running:
      try:
        schedule.run_pending()
        time.sleep(1)
      except KeyboardInterrupt:
        running = False
