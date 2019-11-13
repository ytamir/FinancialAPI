from ConfigFiles import MetricsConfig
import requests


def build_url(quarterly_annual, metrics, stocks, symbols_to_ignore_for_metric):
    """
    This function takes in a frequency, metrics, and symbols and returns a list of dictionaries
    :param quarterly_annual: Quarterly or Annual
    :param metrics: List of metrics specified in the MetricsConfig.py file
    :param stocks: Stock symbols
    :param symbols_to_ignore_for_metric: Which symbols we do not need to pass to the url for a specified metric
    :return: Returns a dictionary of the urls needed and there associated metrics {'url' : url, 'metrics': [],
             'size_filtered_symbols': [] }
    """

    return_arr = []
    for metric in metrics:

        url = ""
        for key, value in MetricsConfig.main_dictionary.items():

            # If metric found
            if metric.upper() in value and key != "all_metrics" and key != "all_metrics_minus_ratios":

                # Get url from dictionary
                url += MetricsConfig.main_dictionary[key + '-url']

                # Append symbols we need
                size_filtered_symbols = 0
                for symbol in stocks:
                    # Do not append symbols that we can ignore for the specified metric
                    if not metric + "-" + symbol in symbols_to_ignore_for_metric:
                        url += symbol + ","
                        size_filtered_symbols += 1

                # Don't add frequency if it is a ratio since this request does not support it
                if key == "ratio-metrics":
                    url = url[:-1]

                # Remove last comma and add frequency
                else:
                    url = url[:-1]
                    url += "?period="
                    if quarterly_annual == MetricsConfig.Frequencies.QUARTERLY:
                        url += "quarter"
                    elif quarterly_annual == MetricsConfig.Frequencies.ANNUAL:
                        url += "annual"
        # If url is found, append a new dictionary with the url and the metric, else just add the metric to the list
        # associated with the url
        found = False
        index_found = 0
        for index, value in enumerate(return_arr):
            if value['url'] == url:
                found = True
                index_found = index
                break
        if not found:
            return_arr.append({'url': url, 'metrics': [metric], 'size_filtered_symbols': size_filtered_symbols})
        else:
            return_arr[index_found]['metrics'].append(metric)

    return return_arr


def parse_json(urls_dict):
    """
    Returns list of data
    :param urls_dict: Dict of api urls to hit and metrics associated with those urls along with how many symbols we have
    :return: List of the Form [{ "SYMBOL": "AAPL", "METRIC": "Revenue", "QUARTERLY_ANNUAL: "QUARTERLY",
     "DATES": [], "DATA": []}, {}, {}, ...]
    """
    # Returning array of dictionaries of form [{SYMBOL: "", METRIC: "", DATES: [], DATA: []}, SYMBOL2: "", METRIC: "",
    # DATES: [], DATA: [] } ]
    return_arr = []

    # Loop through all urls needed
    for item in urls_dict:
        response = requests.get(item['url'])
        response.raise_for_status()
        json_dictionary = response.json()
        # Loop through all metrics associated with the url
        for metric in item['metrics']:
            # First convert symbols and there metrics to an array of the form [{}, {}, {}, {}]
            # Loop through each symbol which will be of the format
            # [{}, {}, {}, {}] - This will give us each inner json
            for symbols_list in json_dictionary.get(list(json_dictionary)[0]) if item["size_filtered_symbols"] > 1\
                    else [] + [json_dictionary]:
                # One dictionary per symbol
                return_dict = {}

                # Get the symbol and the inner json array [should only be two keys and values]
                # { symbol: "",
                #   json_key : [{}] }
                return_dict["SYMBOL"] = list(symbols_list.values())[0]
                return_dict["METRIC"] = metric
                dates_metrics_json_array = list(symbols_list.values())[1]

                dates = []
                data = []
                # Loop through the array of dates and metrics to store them all
                # [{ DATE: "", json_key_1 : "", json_key_2: ""}, { DATE2: "", json_key_1 : "", json_key_2: ""}]
                for dates_metrics_json in dates_metrics_json_array:
                    # Loop all keys and values to get the date and the metric passed in
                    # Format 1 : { DATE: "", json_key_1 : "", json_key_2: ""}
                    # Format 2 : { DATE: "", json_key_1 : {}, json_key_2: {}}
                    for key, value in dates_metrics_json.items():
                        if key == "date":
                            dates.append(value)

                        else:
                            # Format 2 : { json_key_1 : {}, json_key_2: {}, ... }
                            if item['url'].startswith('https://financialmodelingprep.com/api/v3/financial-ratios/'):
                                ratios_json = value.items()
                                for ratio_key, ratio_value in ratios_json:
                                    if ratio_key.upper() == metric.upper():
                                        data.append(ratio_value)
                            else:
                                if key.upper() == metric.upper():
                                    data.append(value)
                return_dict["DATES"] = dates
                return_dict["DATA"] = data
                return_arr.append(return_dict)

    return return_arr


def fetch_data(quarterly_annual, metrics, stocks, symbols_to_ignore_for_metric):
    """
    Returns formatted json based on data requested
    :param quarterly_annual: Whether we want quarterly or annual data
    :param metrics: What metrics we want to fetch
    :param stocks: Which stocks we want to fetch
    :param symbols_to_ignore_for_metric: Which symbols we do not need to pass to the url for a specified metric
    :return: List of the Form [{ "SYMBOL": "AAPL", "METRIC": "Revenue", "DATES": [], "DATA": []}, {}, {}, ...]
    """

    if len(stocks) == 0 or len(metrics) == 0:
        return []
    else:
        urls_dict = build_url(quarterly_annual, metrics, stocks, symbols_to_ignore_for_metric)
        return parse_json(urls_dict)
