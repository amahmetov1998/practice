import xlrd
import os

directory = 'files'
files = os.listdir(directory)

d = {
    'Код инструмента': 1,
    'Наименование инструмента': 2,
    'Базис поставки': 3,
    'Объем договоров в единицах измерения': 4,
    'Объем договоров': 5,
    'Количество договоров': 14,
}


def set_type(value):
    if value.isdigit():
        return int(value)


def parse_excel():
    for file in files:
        try:
            xls = xlrd.open_workbook(f'files/{file}')
            sheet = xls.sheet_by_index(0)

            for i in range(sheet.nrows):
                if len(sheet.cell_value(i, 1)) != 11:
                    continue
                args = {
                    'exchange_product_id': sheet.cell_value(i, d['Код инструмента']),
                    'exchange_product_name': sheet.cell_value(i, d['Наименование инструмента']),
                    'oil_id': sheet.cell_value(i, d['Код инструмента'])[:4],
                    'delivery_basis_id': sheet.cell_value(i, d['Код инструмента'])[4:7],
                    'delivery_basis_name': sheet.cell_value(i, d['Базис поставки']),
                    'delivery_type_id': sheet.cell_value(i, d['Код инструмента'])[-1],
                    'volume': set_type(sheet.cell_value(i, d['Объем договоров в единицах измерения'])),
                    'total': set_type(sheet.cell_value(i, d['Объем договоров'])),
                    'count': set_type(sheet.cell_value(i, d['Количество договоров'])),
                    'date': file[3:-5],
                    'created_on': None,
                    'updated_on': None,
                }

                yield args

        except FileNotFoundError:
            print('File not Found!')

