from PyhonRequestFiles import FinancialMetricsScraper

# TODO ADD CONFIG GENERATOR FOR OTHER THINGS WE NEED LIKE STOCK SYMBOLS, CASH FLOW STATEMENT, BALANCE SHEET

# Clear File
open('Config.py', 'w').close()

# GENERATE INCOME STATEMENT METRICS
income_statement_out_str = "income_statement_metrics = ["
data = FinancialMetricsScraper.StockRowData.get_file("AAPL", FinancialMetricsScraper.SheetType.INCOME_STATEMENT,
                                                     FinancialMetricsScraper.Frequency.QUARTERLY)
for i in range(0, len(data.iloc[0, :])):
    # Don't need comma on last item
    metric_to_str = "\"" + data.iloc[0, i] + "\", " if i != len(data.iloc[0, :]) - 1 else "\"" + data.iloc[0, i] + "\""
    income_statement_out_str += metric_to_str
income_statement_out_str += "]"
f = open("Config.py", "a")
f.write(income_statement_out_str)


f.close()