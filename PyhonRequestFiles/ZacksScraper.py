from bs4 import BeautifulSoup as beautSoup
from datetime import date as date_library
from fake_useragent import UserAgent as Ua
from pymongo import errors as MongoErrors
from redis import RedisError
import json
import requests
import re


def scrape_etf_holdings(ticker, mongo_db, redis_connection):
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

    # Get Current Date For Querying Redis and Mongo
    todays_date = date_library.today().strftime("%d/%m/%Y")

    # Try Redis Read First
    try:
        redis_data = read_redis(redis_connection, ticker+"-"+todays_date)
        if redis_data is not None:
            return redis_data
    except RedisError:
        pass

    # Try Mongo Read Second
    try:
        mongo_data = read_mongo(mongo_db, todays_date, ticker)
        if mongo_data is not None:
            mongo_json = json.dumps(mongo_data, indent=4)
            write_redis(redis_connection, ticker + "-" + todays_date, mongo_json)
            return mongo_json
    except MongoErrors.PyMongoError:
        pass
    try:
        # Make Request
        ua = Ua()
        request_result = requests.get('https://www.zacks.com/funds/etf/' + ticker + '/holding',
                                      headers={"User-Agent": ua.random})

        # Heavily Reliant on Current Page Architecture
        # First Get Data inside script tag which contains holding data
        html_content = beautSoup(request_result.content, features="lxml")

        # Get Content in The Script Tag, All Holding Data is in script tag that we need to parse as a string
        script_tag_string = html_content.findAll('script', text=re.compile('var etf_holdings'))[0]
        # Find the ETF Holdings Array In the Whole Script Tag String
        etf_holdings_array_string = re.search(r'etf_holdings\.formatted_data.+\] \]', str(script_tag_string)).group()

        # Find the ETF Table Header In the Whole Script Tag String to get the date
        etf_date_array_string = re.search(r'etf_holdings\.table_header.+;', str(script_tag_string)).group()

        # Replace the . in the javascript variable names so we can convert the array to python
        etf_holdings_text = re.sub(r'\.', '_', etf_holdings_array_string, count=1)
        etf_date_text = re.sub(r'\.', '_', etf_date_array_string, count=1)

        # EXEC NOT SAFE HOPFEULLY: ZACKS DOES NOT SEND US MALLICIOUS CODE
        # Convert the string to a python array using exec that will be stored in etf_holdings_formatted_data
        etf_holdings_text = "global etf_holdings_formatted_data; " + etf_holdings_text
        # Convert the javascript string to a python string using exec that will be stored in etf_holdings_table_header
        etf_date_text = "global etf_holdings_table_header; " + etf_date_text
        exec(etf_holdings_text)
        exec(etf_date_text)

        # Get ETF Date From the Table Header
        etf_date = etf_holdings_table_header.split("of ", 1)[1]

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
        python_dict = {"QueryDate": etf_date, "HoldingsLastUpdatedDate": etf_date,
                       "Ticker": ticker, "Holdings": holdings_dict}
        json_val = json.dumps(python_dict, indent=4)

        # Try Writing to redis
        try:
            write_redis(redis_connection, ticker+"-"+todays_date, json_val)
        except RedisError:
            pass

        # Try Writing to mongo
        try:
            write_mongo(mongo_db, python_dict)
        except MongoErrors.PyMongoError:
            pass

        # Return JSON Format
        return json_val

    # Return If Error
    except Exception:
        raise Exception('Error Fetching Data')


def read_mongo(mongo_db, date, ticker):
    """
    Queries Mongo by Date and Ticker to return holdings data
    :param: mongo_db - Mongo Connection
    :param: date - Used in Query
    :param: ticker - User In Query
    :return: Returns Non JSON Date if Found, raises error if no database connection or something went wrong
    """
    if mongo_db:
        try:
            result = mongo_db.ETFHoldings.find_one({"QueryDate": date, "Ticker": ticker},
                                                   {"_id": False, "Holdings": True})
            return result
        except MongoErrors:
            raise MongoErrors.PyMongoError
    else:
        raise MongoErrors.PyMongoError


def write_mongo(mongo_db, data):
    """
    Stores Holding Data in Mongo DB
    :param: mongo_db - Mongo Connection
    :param: data - JSON data

    :return: Raises Error if bad connection or something went wrong
    """
    if mongo_db:
        try:
            mongo_db.ETFHoldings.insert(data, check_keys=False)
        except MongoErrors:
            raise MongoErrors.PyMongoError
    else:
        raise MongoErrors.PyMongoError


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
        except RedisError:
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
        except RedisError:
            raise RedisError
    else:
        raise RedisError

# print(scrape_etf_holdings("VOO", None, None))
