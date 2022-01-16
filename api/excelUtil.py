import openpyxl

from api import fileUtil

def get_cell_value(cell_key,sheet_name="Sheet1"):
    sheets=openpyxl.load_workbook(fileUtil.join(fileUtil.get_path(),"data/xxxll.xlsx"))
    sheet=sheets[sheet_name]
    return sheet[cell_key].value
