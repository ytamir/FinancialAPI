import openpyxl
import os
import pandas as pd
import wget


class SheetType:
    CASH_FLOW_STATEMENT = "Cash%20Flow"
    BALANCE_SHEET = "Balance%20Sheet"
    INCOME_STATEMENT = "Income%20Statement"
    METRICS = "Metrics"


class Frequency:
    QUARTERLY = "MRQ"
    ANNUAL = "MRY"


class StockRowData:

    # get_file - Gets Excel From from stockrow.com and stores in StockRowData directory
    # stock_symbol - Ticker symbol
    # type - Cash Flow Statement, Balance Sheet, Income Statement
    # frequency - Quarterly or Annual
    # returns - Data Frame with data
    @staticmethod
    def get_file(stock_symbol, type, frequency):

        download_url = "https://stockrow.com/api/companies/" + stock_symbol + "/financials.xlsx?dimension=" \
                       + frequency + "&" + "section=" + type + "&sort=desc"
        file_dir = "..\\QuarterlyAnnualData\\"

        temp_name = "Metrics" if SheetType.METRICS == type else type.split('%')[0] + type.split('0')[1]
        file_path = file_dir + "\\" + stock_symbol + temp_name + frequency[2] + ".xlsx"
        if os.path.exists(file_path):
            os.remove(file_path)

        wget.download(download_url, file_path)

        x_file = openpyxl.load_workbook(file_path)
        sheet = x_file[stock_symbol]
        sheet.cell(row=1, column=1).value = "DATE"
        x_file.save(file_path)

        balance_sheet_data = pd.read_excel(file_path, header=0, index_col=False, keep_default_na=True).T
        print(balance_sheet_data.head())
        return balance_sheet_data

#Example Usage
instance = StockRowData()
instance.get_file("GOOGL", SheetType.METRICS, Frequency.QUARTERLY)
