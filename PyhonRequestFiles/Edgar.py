from bs4 import BeautifulSoup as bs
import requests


def browse_edgar(ticker_sym):
    """
    This function takes in a stock ticker symbol and browses edgar for all form types
    :param: ticker_sym: Symbol we want to get documents for
    :return: HTML Content Containing all documents
    """
    response = requests.get(
        'https://www.sec.gov/cgi-bin/browse-edgar',
        params={'CIK': ticker_sym, 'owner': 'exclude', 'action': 'getcompany', 'Find': 'search'},
    )

    print(response.content)
    return response.content


def search_edgar(search_str, year_beg, year_end):
    """
    This function takes in a search string and browses edgar for forms
    :param: search_str: Search string
    :param: year_beg: Start Year to fetch for
    :param: year_end: End year to fetch for
    :return: HTML Content Containing all documents
    """

    response = requests.get(
        'https://www.sec.gov/cgi-bin/srch-edgar',
        params={'text': search_str.upper(), 'first': year_beg, 'last': year_end},
    )

    print(response.content)
    return response.content


def get_cik_ascension_number_for_10Q(html_content):
    """
    This function gets the cik number and  ascension number for the 10-Q for the ticker symbol passed in
    :param: html_content: HTML Content to parse
    :return: cik and ascension number in a list [cik, ascension_number]
    """
    soup = bs(html_content, 'html')

    cik_whole_text = soup.find("span", {"class": "companyName"}).findChildren("a", recursive=False)[0].get_text()
    cik_number = ''.join(ch for ch in cik_whole_text if ch.isdigit())
    print(cik_number)

    ascension_number_whole_text = soup.find(text="10-Q").findNext('td').findNext('td').contents[2]
    ascension_number_split = ascension_number_whole_text.split('(')[0]
    ascension_number = ''.join(ch for ch in ascension_number_split if ch.isdigit())
    print(ascension_number)

    return [cik_number, ascension_number]


def get_ncsrs(ticker):
    """
    This function returns the HTML format of form n-CSRS which reports on an ETF or Mutual Fund Holdsings
    :param: ticker: Ticker of ETF Or Mutual Fund
    :return: cik and ascension number in a list [cik, ascension_number]
    """

    html_content = search_edgar(ticker + " N-CSRS", 2019, 2020)
    soup = bs(html_content, 'html')

    # Link should be in the fourth table, row 2, column 2
    link = 'https://www.sec.gov' + soup.findAll('table')[4].findChildren('tr')[1].findChildren('td')[1]\
           .findChildren("a", recursive=False)[0].get('href')
    print(link)

    html_content = requests.get(link).content
    soup = bs(html_content, 'html')
    # Link should in the first table row 2, column 3
    link = 'https://www.sec.gov' + soup.findAll('table')[0].findChildren('tr')[1].findChildren('td')[2]\
           .findChildren("a", recursive=False)[0].get('href')
    print(link)

    html_content = requests.get(link).content
    # print(html_content)

    return html_content


def get_filing_summary_xml_content(ascension_number, cik_number):
    """
    This function takes in a CIK and Ascension Number and returns the xml content of the filling summary
    :param: ascension_number: Unique Identifier for Each File On Edgar
    :param: cik_number: Unique Identifier for Each Company that Files on Edgar
    :return: XML Content of filing summary
    """
    response = requests.get(
        'https://www.sec.gov/Archives/edgar/data/' + cik_number + '/'+ascension_number + '/FilingSummary.xml',
    )

    print(response.content)
    return response.content


def get_segment_information_link(xml_content):
    """
    This function finds the segment information link from the xml content passed in
    :param: xml_content: XML Content to parse
    :return: HTML File that contains segment information
    """
    soup = bs(xml_content, 'xml')

    short_names = soup.find_all('ShortName')
    short_name = ''
    for item in short_names:
        if 'SEGMENT' in item.get_text().upper():
            short_name = item
            break

    html_file = short_name.parent.find('HtmlFileName').get_text()
    print(html_file)
    return html_file


def get_segments_information(ascension_number, cik_number, html_file_name):
    """
    This function finds the segment information ( i.e. what a company does ) from the provided html file
    :param: ascension_number: Unique Identifier for Each File On Edgar
    :param: cik_number: Unique Identifier for Each Company that Files on Edgar
    :param: html_file_name: HTML File Containing Segment info
    :return: Segment Information
    """

    url = 'https://www.sec.gov/Archives/edgar/data/' + cik_number + '/' + ascension_number + "/" + html_file_name
    print(url)
    response = requests.get(url)
    print(response.content)
    return response.content


# [cik_num, asc_num] = get_cik_ascension_number_for_10Q(browse_edgar("GRMN"))
# html_file_name = get_segment_information_link(get_filing_summary_xml_content(asc_num, cik_num))
# get_segments_information(asc_num, cik_num, html_file_name)
get_ncsrs('VOO')
