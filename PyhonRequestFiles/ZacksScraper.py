from bs4 import BeautifulSoup as beautSoup
from fake_useragent import UserAgent
from redis import RedisError
import json
import requests
import re


def scrape_etf_holdings(ticker, redis_connection):
    """
    This function takes in an ETF/Mutual Fund Ticker along with a boolean and returns json format for holding data
    from Zacks
    :param: ticker: Ticker For ETF
    :param: redis_connection: Connection to Redis DB
    :return: JSON Format {"Holdings": {"Microsoft Corp.": {"Number of Shares": "154,277,455",
                                                            "Percentage of Portfolio": "4.81",
                                                            "Annual Percentage Change": "54.00"
                                                          }, ...
                                      }
                        }
    """

    # Try Redis Read First
    try:
        redis_data = read_redis(redis_connection, ticker)
        if redis_data is not None:
            return redis_data
    except RedisError:
        pass

    # Use User Agent so Zacks Does Not Reject Our Request and send request
    ua = UserAgent()

    try:
        request_result = requests.get('https://www.zacks.com/funds/etf/' + ticker + '/holding',
                                      headers={"User-Agent": ua.random})

        # Heavily Reliant on Current Page Architecture
        # First Get Data inside script tag which contains holding data
        html_content = beautSoup(request_result.content, 'html')
        # Get Content in The Script Tag, All Holding Data is in script tag that we need to parse as a string
        script_tag_string = html_content.findAll('script', text=re.compile('var etf_holdings'))[0]
        # Find the ETF Holdings Array In the Whole Script Tag String
        etf_holdings_array_string = re.search(r'etf_holdings\.formatted_data.+\] \]', str(script_tag_string)).group()
        # Replace the . in the javascript variable name so we can convert the array to python
        text = re.sub(r'\.', '_', etf_holdings_array_string, count=1)

        # Convert the string to a python array using exec that will be stored in etf_holdings_formatted_data
        # EXEC NOT SAFE HOPFEULLY: ZACKS DOES NOT SEND US MALLICIOUS CODE
        text = "global etf_holdings_formatted_data; " + text
        exec(text)

        # Get Data into dict format which is convertible to JSON
        holdings_dict = {}
        # Loop through each holding in the array
        for holding_data in etf_holdings_formatted_data:

            # Sometime the holding name is to long on the page, so rather than show the string they use a javascript
            # tooltip so we need to parse that
            formatted_name = holding_data[0]
            if formatted_name.startswith('<span '):
                formatted_name = formatted_name[92:].split("\'", 1)[0].upper()

            # Ticker is Wrapped in a link if it is available, otherwise store an empty string
            formatted_ticker = holding_data[1]
            if formatted_ticker.startswith('<a '):
                formatted_ticker = formatted_ticker[40:].split("\"", 1)[0].upper()
            else:
                formatted_ticker = ""

            # Store Information in dict and append to holdings dict
            stock_dict = {formatted_name: {"Ticker": formatted_ticker,
                                           "Number of Shares": holding_data[2],
                                           "Percentage of Portfolio": holding_data[3],
                                           "Annual Percentage Change": holding_data[4]
                                           }
                          }
            holdings_dict.update(stock_dict)

        # Store JSON
        json_val = json.dumps({"Holdings": holdings_dict}, indent=4, sort_keys=True)

        # Try Writing to redis
        try:
            write_redis(redis_connection, ticker, json_val)
        except RedisError:
            pass

        # Return JSON Format
        return json_val

    # Return If Error
    except:
        raise Exception('Error Fetching Data')


def read_redis(redis_connection, key):
    """
    Collects Data from Redis Database
    :param: redis_connection - Redis Connection
    :param: key - Key to Store
    :param: data - Data to Store
    :return: Return Data if successful, Raise Error Otherwise
    """
    if redis_connection:
        try:
            return redis_connection.execute_command('JSON.GET', key)
        except:
            raise RedisError
    else:
        raise RedisError


def write_redis(redis_connection, key, data):
    """
    Stores Data in Redis Database
    :param: redis_connection - Redis Connection
    :param: key - Key to Store
    :param: data - Data to Store
    :return: Return None, Raise Error Otherwise
    """
    if redis_connection:
        try:
            redis_connection.execute_command('JSON.SET', key, '.', data)
            return None
        except:
            raise RedisError
    else:
        raise RedisError

# print(scrape_etf_holdings("ZIG"))
