import os
import pandas as pd


class ExcelSheet:

    def __init__(self, file_name: str):
        self.file_name = file_name

        self.headers = {
            "tijd (HH:MM:SS)": [],
            "temperatuur (celcius)": [],
            "luchtvochtigheid (%)": [],
            "luchkwaliteit (ppm)": [],
        }

    def _create(self):

        # Check if the the file already exists
        if os.path.isfile(self.file_name):
            print(f"{self.file_name} already exists.")
            return
        # If not create the file
        df = pd.DataFrame(self.headers)

        writer = pd.ExcelWriter(self.file_name, engine="openpyxl")
        df.to_excel(writer, header=True, startcol=0)
        writer.close()

    def update(room: str, time: str, temp: int, hum: int, aq: int):
        print("Updating excel sheet")


# def create_excel_sheet():
#   if os.path.isfile(EXCEL_FILE_NAME):
#     print(f"{EXCEL_FILE_NAME} already exists.")
#     return
#   print("Creating excel file with name: ", EXCEL_FILE_NAME)
#   df = pd.DataFrame({
#     "tijd (HH:MM:SS)": [],
#     'temperatuur (celcius)': [],
#     'luchtvochtigheid (%)': [],
#     'luchkwaliteit (ppm)': [],
#   })
#   writer = pd.ExcelWriter(EXCEL_FILE_NAME, engine="openpyxl")
#   # writer.save()
#   df.to_excel(writer, header=True, startcol=0)
#   writer.close()
#   print("Done!")

# def update_excel_sheet(time: str, temp: int, hum: int, aq: int):
#   print('Updating excel sheet...')
#   df = pd.DataFrame({
#     'tijd (HH:MM:SS)': [time],
#     'temperatuur (celcius)': [temp],
#     'luchtvochtigheid (%)': [hum],
#     'luchkwaliteit (ppm)': [aq],
#   })

#   writer = pd.ExcelWriter(EXCEL_FILE_NAME, engine='openpyxl')

#   writer.book = load_workbook(EXCEL_FILE_NAME)
#   writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
#   reader = pd.read_excel(EXCEL_FILE_NAME)
#   df.to_excel(writer, index=False, header=False,startrow=len(reader)+1)
#   writer.close()
#   print("Done!")

