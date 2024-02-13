from pprint import pprint

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'


def htmlColorToJSON(htmlColor):
    if htmlColor.startswith("#"):
        htmlColor = htmlColor[1:]
    return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0, "blue": int(htmlColor[4:6], 16) / 255.0}


class Spreadsheet:
    def __init__(self, json_filename):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            json_filename, ['https://www.googleapis.com/auth/spreadsheets',
                            'https://www.googleapis.com/auth/drive'])
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)
        self.driveService = None
        self.spreadsheetId = None
        self.sheetId = None
        self.sheetTitle = None
        self.requests = []
        self.valueRanges = []

    def create(self, title, sheet_title, rows=1000, cols=26, locale='en_US', time_zone='Etc/GMT'):
        spreadsheet = self.service.spreadsheets().create(body={
            'properties': {
                'title': title,
                'locale': locale,
            },
            'sheets': [
                {
                    'properties': {
                        'sheetType': 'GRID', 'sheetId': 0,
                        'title': sheet_title,
                        'gridProperties': {
                            'rowCount': rows,
                            'columnCount': cols
                        }
                    }
                }
            ]
        }
        ).execute()
        self.spreadsheetId = spreadsheet['spreadsheetId']
        self.sheetId = spreadsheet['sheets'][0]['properties']['sheetId']
        self.sheetTitle = spreadsheet['sheets'][0]['properties']['title']

    def share(self, share_request_body):
        if self.driveService is None:
            self.driveService = apiclient.discovery.build('drive', 'v3', http=self.httpAuth)
        share_res = self.driveService.permissions().create(
            fileId=self.spreadsheetId,
            body=share_request_body,
            fields='id'
        ).execute()

    def shareWithAnybodyForWriting(self):
        self.share({'type': 'anyone', 'role': 'writer'})

    def get_sheet_url(self):
        return 'https://docs.google.com/spreadsheets/d/' + self.spreadsheetId + '/edit#gid=' + str(self.sheetId)

    def run_prepared(self, value_input_option="USER_ENTERED"):
        upd1Res = {'replies': []}
        upd2Res = {'responses': []}
        try:
            if len(self.requests) > 0:
                upd1Res = self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                  body={"requests": self.requests}).execute()
            if len(self.valueRanges) > 0:
                upd2Res = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId,
                                                                           body={"valueInputOption": value_input_option,
                                                                                 "data": self.valueRanges}).execute()
        finally:
            self.requests = []
            self.valueRanges = []
        return upd1Res['replies'], upd2Res['responses']

    def set_dimension(self, dimension, startIndex, endIndex, pixelSize):
        self.requests.append({"updateDimensionProperties": {
            "range": {"sheetId": self.sheetId,
                      "dimension": dimension,
                      "startIndex": startIndex,
                      "endIndex": endIndex},
            "properties": {"pixelSize": pixelSize},
            "fields": "pixelSize"}})

    def set_columns_width(self, start_col, end_col, width):
        self.set_dimension("COLUMNS", start_col, end_col + 1, width)

    def set_column_width(self, col, width):
        self.set_columns_width(col, col, width)

    def set_rows_height(self, start_row, end_row, height):
        self.set_dimension("ROWS", start_row, end_row + 1, height)

    def set_row_height(self, row, height):
        self.set_rows_height(row, row, height)

    def convert_to_grid_range(self, cellsRange):
        if isinstance(cellsRange, str):
            startCell, endCell = cellsRange.split(":")[0:2]
            cellsRange = {}
            rangeAZ = range(ord('A'), ord('Z') + 1)
            if ord(startCell[0]) in rangeAZ:
                cellsRange["startColumnIndex"] = ord(startCell[0]) - ord('A')
                startCell = startCell[1:]
            if ord(endCell[0]) in rangeAZ:
                cellsRange["endColumnIndex"] = ord(endCell[0]) - ord('A') + 1
                endCell = endCell[1:]
            if len(startCell) > 0:
                cellsRange["startRowIndex"] = int(startCell) - 1
            if len(endCell) > 0:
                cellsRange["endRowIndex"] = int(endCell)
        cellsRange["sheetId"] = self.sheetId
        return cellsRange

    def prepare_setValues(self, cellsRange, values, major_dimension="ROWS"):
        self.valueRanges.append(
            {"range": self.sheetTitle + "!" + cellsRange, "majorDimension": major_dimension, "values": values})

    def prepare_mergeCells(self, cellsRange, merge_type="MERGE_ALL"):
        self.requests.append({"mergeCells": {"range": self.convert_to_grid_range(cellsRange), "mergeType": merge_type}})

    def prepare_setCellsFormat(self, cellsRange, formatJSON, fields = "userEnteredFormat"):
        self.requests.append({"repeatCell": {"range": self.convert_to_grid_range(cellsRange), "cell": {"userEnteredFormat": formatJSON}, "fields": fields}})

    # formatsJSON should be list of lists of dicts with userEnteredFormat for each cell in each row
    def prepare_setCellsFormats(self, cellsRange, formatsJSON, fields = "userEnteredFormat"):
        self.requests.append({"updateCells": {"range": self.convert_to_grid_range(cellsRange),
                                              "rows": [{"values": [{"userEnteredFormat": cellFormat} for cellFormat in rowFormats]} for rowFormats in formatsJSON],
                                              "fields": fields}})



def testCreateTimeManagementReport():
    docTitle = "Тестовый документ"
    sheetTitle = "Учет времени работы двигателей для расчета амортизации"
    values = [["Марка", "Количество валов", "Пуск в работу", "Остановка", "Время в работе"],
              ["МТК-30-12", "Одновальная", "18 авг 2023 17:57:12", "25 авг 2023 18:40:20", "=D4-C4"],
              ["ГПС-31-ВА03", "Многовальная", "02 сент 2023 13:41:44", "16 окт 2023 23:13:54", "=D5-C5"],
              ["ГТК-32-02", "Многовальная", "14 мар 2023 18:53:39", "15 апр 2023 17:00:23", "=D6-C6"],
              ["МКП-223-21", "Одновальная", "13 окт 2023 08:12:32", "09 дек 2023 12:03:13", "=D7-C7"],
              ["МТК-30-12", "Одновальная", "03 авг 2023 13:23:45", "14 авг 2023 16:38:20", "=D8-C8"],
              ["АЛ-43-13", "Многовальная", "03 апр 2023 12:54:33", "16 июн 2023 13:33:20", "=D9-C9"],
              ["МТК-30-12", "Одновальная", "05 авг 2023 17:57:12", "14 авг 2023 18:40:20", "=D10-C10"],
              ["ГПС-21-ВА03", "Многовальная", "23 сент 2023 13:41:44", "04 окт 2023 23:13:54", "=D11-C11"],
              ["ГТК-45-02", "Многовальная", "04 мар 2023 18:53:39", "01 апр 2023 17:00:23", "=D12-C12"],
              ["МКП-223-23", "Одновальная", "06 окт 2023 08:12:32", "14 дек 2023 12:03:13", "=D13-C13"],
              ["МТК-30-12", "Одновальная", "18 авг 2023 13:23:45", "31 авг 2023 16:38:20", "=D14-C14"],
              ["АЛ-31-13", "Многовальная", "05 апр 2023 12:54:33", "13 июн 2023 13:43:31", "=D15-C15"],
              ["АЛ-31-13", "Многовальная", "23 апр 2023 12:54:33", "21 июн 2023 13:12:52", "=D16-C16"],
              ["МТК-25-12", "Одновальная", "01 авг 2023 17:57:12", "14 авг 2023 18:40:20", "=D17-C17"],
              ["ГПС-32-ВА03", "Многовальная", "22 сент 2023 13:41:44", "13 окт 2023 23:13:54", "=D18-C18"],
              ["ГТК-32-02", "Многовальная", "04 мар 2023 18:53:39", "01 апр 2023 17:00:31", "=D19-C19"],
              ["МКП-220-21", "Одновальная", "06 окт 2023 08:12:32", "14 дек 2023 12:03:53", "=D20-C20"],
              ["МТК-30-12", "Одновальная", "18 янв 2023 13:23:43", "31 янв 2023 16:34:54", "=D21-C21"],
              ["АЛ-31-13", "Многовальная", "08 янв 2023 12:54:33", "01 февр 2023 13:54:20", "=D22-C22"],
              ["МКП-223-21", "Одновальная", "13 окт 2023 08:12:32", "09 дек 2023 11:03:13", "=D23-C23"],
              ["МТК-30-12", "Одновальная", "27 авг 2023 13:23:45", "28 авг 2023 04:23:35", "=D24-C24"],
              ["АЛ-43-13", "Многовальная", "30 апр 2023 12:54:33", "01 июн 2023 13:33:20", "=D25-C25"],
              ["МТК-30-12", "Одновальная", "14 авг 2023 17:57:12", "23 авг 2023 18:40:20", "=D26-C26"],
              ["ГПС-21-ВА03", "Многовальная", "12 сент 2023 13:41:44", "22 окт 2023 23:13:54", "=D27-C27"],
              ["ГТК-45-02", "Многовальная", "04 окт 2023 14:34:39", "01 дек 2023 16:34:23", "=D28-C28"],
              ]
    rowCount = len(values) - 1
    colorsForCategories = {"Одновальная": htmlColorToJSON("#CCFFCC"),
                           "Многовальная": htmlColorToJSON("#CCCCFF")}

    ss = Spreadsheet(CREDENTIALS_FILE)
    ss.create(docTitle, sheetTitle, rows = rowCount + 3, cols=8, locale="ru_RU")
    ss.shareWithAnybodyForWriting()

    ss.set_column_width(0, 400)
    ss.set_column_width(1, 200)
    ss.set_columns_width(2, 3, 165)
    ss.set_column_width(4, 100)
    ss.prepare_mergeCells("A1:E1")  # Merge A1:E1

    rowColors = [colorsForCategories[valueRow[1]] for valueRow in values[1:]]

    ss.prepare_setCellsFormat("A1:A1", {"textFormat": {"fontSize": 14},
                                        "horizontalAlignment": "CENTER"})  # Font size 14 and center aligment for A1 cell
    ss.prepare_setCellsFormat("A3:E3", {"textFormat": {"bold": True},
                                        "horizontalAlignment": "CENTER"})  # Bold and center aligment for A3:E3 row
    ss.prepare_setCellsFormats("A4:E%d" % (rowCount + 3), [[{"backgroundColor": color}] * 5 for color in rowColors])
    ss.prepare_setCellsFormat("A4:B%d" % (rowCount + 3), {"numberFormat": {'type': 'TEXT'}},
                              fields="userEnteredFormat.numberFormat")  # Text format for A4:B* columns
    ss.prepare_setCellsFormat("E4:E%d" % (rowCount + 3), {"numberFormat": {'pattern': '[h]:mm:ss', 'type': 'TIME'}},
                              fields="userEnteredFormat.numberFormat")  # Duration number format for E4:E* column
    # Bottom border for A3:E3 row
    ss.requests.append({"updateBorders": {"range": {"sheetId": ss.sheetId, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": 0, "endColumnIndex": 5},
                                          "bottom": {"style": "SOLID", "width": 1, "color": htmlColorToJSON("#000001")}}})

    ss.prepare_setValues("A1:A1", [[sheetTitle]])
    ss.prepare_setValues("A3:E%d" % (rowCount + 3), values)

    ss.set_column_width(6, 200)
    ss.set_column_width(7, 100)
    ss.prepare_mergeCells("G1:H1")  # Merge G1:H1


    ss.run_prepared()
    print(ss.get_sheet_url())


if __name__ == "__main__":
    testCreateTimeManagementReport()
