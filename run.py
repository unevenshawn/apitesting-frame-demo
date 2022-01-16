import os
from datetime import datetime


import pytest

from api import yamlUtil

if __name__ == '__main__':
    alluredir=f"./reports/report_{str(datetime.today().date())}"
    pytest.main()
    os.system(f"allure generate ./temps -o  {alluredir} --clean")
