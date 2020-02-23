from bs4 import BeautifulSoup as beautSoup
from fake_useragent import UserAgent
import json
import requests
import re

# Up here so Pycharm does not complain about errors
etf_holdings_formatted_data = []


def scrape_holdings(ticker, is_etf):
    """
    This function takes in an ETF/Mutual Fund Ticker along with a boolean and returns json format for holding data
    from Zacks
    :param: ticker: Ticker For ETF
    :param: is_etf: Is this an ETF or Mutual Fund
    :return: JSON Format "Holdings : { Holding 1: [ shares, %portfolio, 52week changed ], ... }"
    """

    # Use User Agent so Zacks Does Not Reject Our Request
    ua = UserAgent()

    # ETF Parsing
    if is_etf:

        request_result = requests.get('https://www.zacks.com/funds/etf/' + ticker + '/holding',
                                      headers={"User-Agent": ua.random})

        html_content = beautSoup(request_result.content, 'html')

        # Heavily Reliant on Current Page Architecture
        # First Get Data inside script tag which contains holding data

        # Get Content in The Script Tag, All Holding Data is in script tag that we need to parse as a string
        script_tag_string = html_content.findAll('script', text=re.compile('var etf_holdings'))[0]

        # Find the ETF Holdings Array In the Whole Script Tag String
        etf_holdings_array_string = re.search(r'etf_holdings\.formatted_data.+\] \]', str(script_tag_string)).group()

        # Replace the . in the javascript variable name so we can convert the array to python
        text = re.sub(r'\.', '_', etf_holdings_array_string, count=1)

        # Convert the string to a python array using exec that will be stored in etf_holdings_formatted_data
        # TODO: Exec not safe find alternative
        text = "global etf_holdings_formatted_data; " + text
        exec(text)

        # Convert Our Array to JSON
        # TODO: Maybe find a less clumsy way to do this
        json_string = "Holdings : { "
        # Loop through each holding in the array

        # TODO: Refactor This
        for holding_data in etf_holdings_formatted_data:

            # Sometime the holding name is to long on the page, so rather than show the string they use a javascript
            # tooltip so we need to parse that
            formatted_name = holding_data[0]
            if formatted_name.startswith('<span '):
                formatted_name = formatted_name[98:].split("\'", 1)[0].upper()

            # Add data to json string
            json_string = json_string + formatted_name + " : " + "[ " + holding_data[2] + ", " + holding_data[3] + \
                          ", " + holding_data[4] + " ], "

        # Format ending of json
        json_string = json_string[:-2]
        json_string = json_string + " }"

        # Return Json Value
        # print(json_val)
        return json_string


# scrape_holdings("ZIG", True)
