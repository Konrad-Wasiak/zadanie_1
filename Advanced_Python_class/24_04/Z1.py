# Task: download and plot a chart of last 10 candles.

import requests
import json
import pandas as pd
import mplfinance as mpl


# interval: number of months
def get_candles_data(interval: int, limit: int):
    url = ('https://www.mexc.com/open/api/v2/market/kline?symbol=ARBUZ_USDT&interval=' +
           str(interval) + 'm&limit=' + str(limit))
    response = requests.get(url)
    responseBody = response.text
    responseBodyJson = json.loads(responseBody)
    candles_data = responseBodyJson["data"]
    return candles_data


def process_candles_data(candles_data):
    formatted_candles_data = []
    for candle in candles_data:
        new_candle = {}
        new_candle_elements = [
            ('time', candle[0]), ('open', float(candle[1])), ('close', float(candle[2])),
            ('high', float(candle[3])), ('low', float(candle[4]))
        ]
        new_candle.update(new_candle_elements)
        formatted_candles_data.append(new_candle)
    return formatted_candles_data


def plot_candles(formatted_candles_data):
    df = pd.json_normalize(formatted_candles_data)  # przetwarzamy dane w formacie json
    df.time = pd.to_datetime(df.time,
                             unit='s')  # ponieważ oczekiwany format daty w kolumnie "time" jest inny niż oczekiwany przez bibliotekę to musimy go skonwertować
    df = df.set_index("time")  # ustawiamy index naszych danych na kolumnę "time"

    mpl.plot(
        df,  # przekazujemy obiekt z danymi
        type="candle",  # określamy typ wykresu.
        title="Candle chart",  # nadajemy tytuł naszego wykresu.
        style="binance",  # wersja kolorystyczna wykresu.
        mav=(3, 6, 9)  # atrybut który włączy automatyczne obliczanie oraz rysowanie średni kroczących.
    )


plot_candles(
    process_candles_data(
        get_candles_data(60, 10)
    )
)
