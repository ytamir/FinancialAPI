from enum import Enum
import requests


class RequestType(Enum):
    FINANCIAL_RATIOS = 0
    ALL_OTHER = 1


def list_to_dict_item(key, file_buffer, my_list):
    """
    This takes a list and writes it to a file as a dictionary item of the form key : my_list
    :param key: Dictionary key that will be created
    :param file_buffer: Buffer of file to write to
    :param my_list: List to store as value of dictionary item
    """
    out_str = "    \"" + key + "\"" + ": [\n"

    for idx, val in enumerate(my_list):
        # Don't need comma on last item
        temp_str = "        \"" + val + "\",\n" if idx != len(my_list)-1 else "        \"" + val + "\"\n"
        out_str += temp_str

    out_str += "    ]"

    file_buffer.write(out_str)


def parse_json(url, request_type):
    """
    Takes a url and scrapes the metrics into a list
    :param url: API url
    :param request_type: Type of json request we have to parse
    :return: List of metrics parsed from the API
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_dictionary = response.json()

        key_list = []

        for key, value in list(json_dictionary.values())[1][0].items():
            if key.upper() != "DATE":
                if request_type == RequestType.ALL_OTHER:
                    key_list.append(key.upper())
                else:
                    for inner_key, inner_value in value.items():
                        key_list.append(inner_key.upper())
        return key_list
    except Exception as err:
        print(f'Error occurred: {err}')


def run():
    """
    Writes API metrics to a dictionary along with helper enum classes
    """
    all_metrics = []
    all_metrics_minus_ratios = []

    config_file_name = "MetricsConfig.py"
    open(config_file_name, 'w').close()
    file_buffer = open(config_file_name, "a")

    # Enum import
    file_buffer.write("from enum import Enum\n\n\n")
    # We can request quarterly or annual data
    file_buffer.write("class Frequencies(Enum):\n    QUARTERLY = 0\n    ANNUAL = 1\n\n\n")
    # We have to types of json responses to parse
    file_buffer.write("class RequestType(Enum):\n    FINANCIAL_RATIOS = 0\n    ALL_OTHER = 1\n\n\n")

    # Start metrics dictionary
    file_buffer.write("main_dictionary = { \n")

    try:

        # Balance Sheet Metrics
        metrics = parse_json("https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/AAPL",
                             RequestType.ALL_OTHER)
        all_metrics += metrics
        all_metrics_minus_ratios += metrics
        list_to_dict_item("balance-sheet-metrics", file_buffer, sorted(metrics))
        file_buffer.write(",\n")
        file_buffer.write("    \"balance-sheet-metrics-url\": "
                          "\"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/\"")
        file_buffer.write(",\n")

        # Cash Flow Metrics
        metrics = parse_json("https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/AAPL",
                             RequestType.ALL_OTHER)
        all_metrics += metrics
        all_metrics_minus_ratios += metrics
        list_to_dict_item("cash-flow-metrics", file_buffer, sorted(metrics))
        file_buffer.write(",\n")
        file_buffer.write("    \"cash-flow-metrics-url\": "
                          "\"https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/\"")
        file_buffer.write(",\n")

        # Key Metrics
        metrics = parse_json("https://financialmodelingprep.com/api/v3/company-key-metrics/AAPL",
                             RequestType.ALL_OTHER)
        all_metrics += metrics
        all_metrics_minus_ratios += metrics
        list_to_dict_item("company-metrics", file_buffer, sorted(metrics))
        file_buffer.write(",\n")
        file_buffer.write("    \"company-metrics-url\": "
                          "\"https://financialmodelingprep.com/api/v3/company-key-metrics/\"")
        file_buffer.write(",\n")

        # Enterprise Value Metrics
        metrics = parse_json("https://financialmodelingprep.com/api/v3/enterprise-value/AAPL",
                             RequestType.ALL_OTHER)
        all_metrics += metrics
        all_metrics_minus_ratios += metrics
        list_to_dict_item("enterprise-value-metrics", file_buffer, sorted(metrics))
        file_buffer.write(",\n")
        file_buffer.write("    \"enterprise-value-metrics-url\": "
                          "\"https://financialmodelingprep.com/api/v3/enterprise-value/\"")
        file_buffer.write(",\n")

        # Growth Metrics
        metrics = parse_json("https://financialmodelingprep.com/api/v3/financial-statement-growth/AAPL",
                             RequestType.ALL_OTHER)
        all_metrics += metrics
        all_metrics_minus_ratios += metrics
        list_to_dict_item("growth-metrics", file_buffer, sorted(metrics))
        file_buffer.write(",\n")
        file_buffer.write("    \"growth-metrics-url\": "
                          "\"https://financialmodelingprep.com/api/v3/financial-statement-growth/\"")
        file_buffer.write(",\n")

        # Income Statement Metrics
        metrics = parse_json("https://financialmodelingprep.com/api/v3/financials/income-statement/AAPL",
                             RequestType.ALL_OTHER)
        all_metrics += metrics
        all_metrics_minus_ratios += metrics
        list_to_dict_item("income-statement-metrics", file_buffer, sorted(metrics))
        file_buffer.write(",\n")
        file_buffer.write("    \"income-statement-metrics-url\": "
                          "\"https://financialmodelingprep.com/api/v3/financials/income-statement/\"")
        file_buffer.write(",\n")

        # Ratios
        metrics = parse_json("https://financialmodelingprep.com/api/v3/financial-ratios/AAPL",
                             RequestType.FINANCIAL_RATIOS)
        all_metrics += metrics
        list_to_dict_item("ratio-metrics", file_buffer, sorted(metrics))
        file_buffer.write(",\n")
        file_buffer.write("    \"ratio-metrics-url\": "
                          "\"https://financialmodelingprep.com/api/v3/financial-ratios/\"")
        file_buffer.write(",\n")

        # List of all metrics
        list_to_dict_item("all_metrics", file_buffer, sorted(all_metrics))
        file_buffer.write(",\n")

        # List of all metrics minus ratios
        list_to_dict_item("all_metrics_minus_ratios", file_buffer, sorted(all_metrics_minus_ratios))
        file_buffer.write("}\n")

        file_buffer.close()
    except Exception as err:

        # If error empty file
        print(f'Error Generating Config: {err}')
        file_buffer.close()
        open(config_file_name, 'w').close()


run()
