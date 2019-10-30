# Used to build a JSON object that contain the ticker, name, and link to image
# also downloads images and stores them in folder images

import requests
import shutil

import json

newobj = []

with open('stocks.json') as json_file:
    stocks = json.load(json_file)

for stock in stocks['symbolsList']:
    stock["image"] = "https://financialmodelingprep.com/images-New-jpg/" + stock['symbol'] +".jpg"
    del stock["price"]
    # # Open the url image, set stream to True, this will return the stream content.
    # resp = requests.get(stock["image"], stream=True)
    # # Open a local file with wb ( write binary ) permission.
    # imagepath = "images/" + stock["symbol"] +".jpg"
    # local_file = open(imagepath, 'wb')
    # # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    # resp.raw.decode_content = True
    # # Copy the response stream raw data to local image file.
    # shutil.copyfileobj(resp.raw, local_file)
    # #
    newobj.append(stock)

finjson = json.dumps(newobj)

import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(finjson, f, ensure_ascii=False, indent=4)



