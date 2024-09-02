import pybit
import requests
import pandas as pd
import numpy as np
from Futures_Statistics.Services import UiUiTheAnalyser as uiui
from urllib.parse import quote
from pybit.unified_trading import HTTP
from pybit.unified_trading import MarketHTTP
from pybit.unified_trading import AccountHTTP
from pybit.unified_trading import PositionHTTP
from pybit.unified_trading import TradeHTTP
from pybit.unified_trading import AssetHTTP

class BybitClient:
    def __init__(self, api_key, api_secret, testnet=False):
        self.session = HTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.market_session = MarketHTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.account_session = AccountHTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.position_session= PositionHTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.trading_session = TradeHTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
        )
        self.asset_session = AssetHTTP(
            testnet=testnet,
            api_key=api_key,
            api_secret=api_secret,
        )


        print("logged in")
        #print(dir(pybit.unified_trading))
        #print(dir(self.asset_session))#wihdraw?

    def get_future_price(self, symbol):
        try:
            response = self.market_session.get_tickers(category="inverse", symbol=symbol)
            if response['retCode'] == 0:
                futures_price = response['result']['list'][0]['markPrice']  # Access first item in the list
                #print("{} Futures Price: {}".format(symbol, futures_price))
                return futures_price
            else:
                #print("Failed to retrieve futures price. Error:", response['retMsg'])
                return None
        except Exception as e:
            #print("Error occurred while fetching futures price:", e)
            return None

    def get_spot_price(self, symbol):
        try:
            response = self.market_session.get_tickers(category="spot", symbol=symbol)
            if response['retCode'] == 0:
                spot_price = response['result']['list'][0]['usdIndexPrice']  # Access first item in the list
                #print("{} Spot Price: {}".format(symbol, spot_price))
                return spot_price
            else:
                #print("Failed to retrieve spot price. Error:", response['retMsg'])
                return None
        except Exception as e:
            #print("Error occurred while fetching spot price:", e)
            return None


    def get_wallet_balance_on_symbol(self, symbol):
        try:
            response = self.session.get_wallet_balance(coin=symbol).result()
            if response['ret_code'] == 0:
                print(response)
                return response
            else:
                print("Failed to retrieve wallet balance for {}: {}".format(symbol, response['ret_msg']))
                return None
        except Exception as e:
            print("Error occurred while fetching wallet balance for {}: {}".format(symbol, e))
            return None

    def get_wallet_balance(self):
        try:
            response = self.account_session.get_wallet_balance(accountType="UNIFIED",)
            if response['retCode'] == 0:

                totat_wallet_balance=response['result']['list'][0]['totalWalletBalance']
                availabe_balance=response['result']['list'][0]['totalAvailableBalance']
                unrealised_pnl=response['result']['list'][0]['totalPerpUPL']
                print("Total balance:{}, available balance:{}, unrealisedPNL:{}".format(totat_wallet_balance,availabe_balance,unrealised_pnl))
                #print(response)
                return response
            else:
                print("Failed to retrieve wallet balance. Error:", response['retMsg'])
                return None
        except Exception as e:
            print("Error occurred while fetching wallet balance:", e)
            return None

    def get_future_position_info(self, symbol):
        try:
            response = self.position_session.get_positions(category="linear", symbol=symbol,)
            if response['retCode'] == 0:

                entry = response['result']['list'][0]['avgPrice']
                leverage = response['result']['list'][0]['leverage']
                tp = response['result']['list'][0]['takeProfit']
                sl = response['result']['list'][0]['stopLoss']
                un_pnl = response['result']['list'][0]['unrealisedPnl']
                price = response['result']['list'][0]['markPrice']
                margin = response['result']['list'][0]['positionIM']
                print("\nPosition:")
                print("COIN:{}, ENTRY:{}, MARGIN:{}$, LEV:{}x, UnrealisedPNL={}, CurrentPrice={}, TP:{}, SL:{}".format(symbol, entry, margin, leverage, un_pnl, price, tp, sl))
                #print(response)
                return response
            else:
                print("Failed to retrieve postition. Error:", response['retMsg'])
                return None
        except Exception as e:
            print("Error occurred while fetching position:", e)
            return None

    def get_all_futures_positions(self):
        page_cursor = None
        while True:
            if page_cursor == '':
                break
            try:
                response = self.position_session.get_positions(category="linear", settleCoin="USDT", cursor=page_cursor)
                #print(response)
            except Exception:
                print("session_get failed")

            if response['retCode'] != 0:
                print("Failed to retrieve positions. Error:", response['retMsg'])
                return None
            else:
                # Print positions for the current page
                positions = response['result']['list']
                print("\nPositions in this page:")
                for position in positions:
                    symbol = position['symbol']
                    entry = position['avgPrice']
                    leverage = position['leverage']
                    tp = position['takeProfit']
                    sl = position['stopLoss']
                    un_pnl = position['unrealisedPnl']
                    price = position['markPrice']
                    margin = position['positionIM']
                    print("\nPosition:")
                    print(
                        "COIN:{}, ENTRY:{}, MARGIN:{}$, LEV:{}x, UnrealisedPNL={}, CurrentPrice={}, TP:{}, SL:{}".format(
                            symbol, entry, margin, leverage, un_pnl, price, tp, sl))
                    #print( response['result']['nextPageCursor'])

                # Update page cursor for the next iteration
                if 'nextPageCursor' in response['result']:
                    page_cursor = response['result']['nextPageCursor']
                    #print(page_cursor)
                else:
                    break  # No more pages, exit the loop

    def set_leverage(self, symbol, buyLev, sellLev):
        response = self.position_session.set_leverage(
                        category='linear',
                        symbol=symbol,
                        buyLeverage=(buyLev),
                        sellLeverage=(sellLev)
        )

        if response["retMsg"] == "OK":
            print("success")
            return True
        else:
            print("failed")
            return False

    def open_futures_position(self, symbol, side, qty):
        if ("long" or "Long" or "LONG") in side:
            side = "Buy"
        if ("short" or "Short" or "SHORT") in side:
            side = "Sell"

        print(qty, type(qty))

        response = self.trading_session.place_order(category="linear",
                                        symbol=symbol,
                                        side=side,
                                        orderType="Market",
                                        qty=qty,
                                        isLeverage=1,
                                        positionIdx=0)
        #print(response)
        if response["retMsg"] == "OK":
            print("success")
            return response['result']['orderId']
        else:
            print("failed : {}".format(response["retMsg"]))


    def get_orderbook(self, symbol, category='linear',limit=25):
        response = self.market_session.get_orderbook(
                                            category=category,
                                            symbol=symbol,
                                            limit=limit
                                            )
        if response['retMsg'] == "OK":
            return response['result']['a'], response['result']['b']
        else:
            print(response['retMsg'])
            return None, None

    def orderbook(self, symbol, category='option', limit=25):
        try:
            response = self.market_session.get_orderbook(category=category, symbol=symbol, limit=limit)
            if response['retCode'] == 0:
                orderbook_data = response['result']
                parsed_orderbook = {
                    'symbol': orderbook_data['s'],
                    'bids': [{'price': float(bid[0]), 'size': float(bid[1])} for bid in orderbook_data['b']],
                    'asks': [{'price': float(ask[0]), 'size': float(ask[1])} for ask in orderbook_data['a']],
                    'timestamp': orderbook_data['ts']
                }
                return parsed_orderbook
            else:
                print(f"Error fetching orderbook: {response['retMsg']}")
                print(f"Full response: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def get_options_list(self, symbol='BTC'):
        try:
            url = "https://api.bybit.com/v5/market/instruments-info?category=option"
            response = requests.get(url)
            data = response.json()
            if data['retCode'] == 0 and 'result' in data:
                options = data['result']['list']
                return [option['symbol'] for option in options if option['symbol'].startswith(symbol)]
            else:
                print(f"Error fetching options list: {data['retMsg']}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return []

    def get_options_with_date(self, symbol='BTC', desired_date=None):
        try:
            url = "https://api.bybit.com/v5/market/instruments-info?category=option"
            response = requests.get(url)
            data = response.json()
            if data['retCode'] == 0 and 'result' in data:
                options = data['result']['list']
                filtered_options = [
                    option['symbol'] for option in options
                    if
                    option['symbol'].startswith(symbol) and (desired_date is None or desired_date in option['symbol'])
                ]
                return filtered_options
            else:
                print(f"Error fetching options list: {data['retMsg']}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return []

    def get_volume(self, symbol, category='spot', interval=60):
        if category == 'linear':
            if 'USDT' in symbol:
                raise ValueError("Linear category doesn't support USDT, needs USD")
            response = self.market_session.get_kline(category=category, symbol=symbol, interval=interval)
            response = response['result']
            response = response['list'][0]
            print(f"trading volume in USD: {response[5]} and in CoinVolume: {response[6]}")
            return float(response[5]), float(response[6])
        if category == 'spot':
            if not symbol.find('USDT'):
                raise ValueError("Spot category requires USDT")
            response = self.market_session.get_kline(category=category, symbol=symbol, interval=interval)
            response = response['result']
            response = response['list'][0]
            print(f"trading volume in USD: {response[6]} and in CoinVolume: {response[5]}")
            return float(response[6]), float(response[5])

    def get_volatility_options(self, symbol='BTC'):
        response = self.market_session.get_historical_volatility(category="option", baseCoin=symbol, period=30)
        # print(response)
        response = response['result'][0]
        return float(response['value'])

    #TODO: send it to uiui
    def get_volatility(self, symbol):
        """
        Calculate the annualized volatility of a symbol based on 1-hour OHLCV data from the past 30 days.

        Args:
            symbol (str): The symbol to fetch data for, in 'BASE/QUOTE' format (e.g., 'BTC/USDT').
            fetch_ohlcv_function (function): A function to fetch OHLCV data with parameters (symbol, timeframe, days).

        Returns:
            float: The annualized volatility of the symbol.
        """
        if '/' not in symbol:
            raise ValueError('Volatility function requires symbol in / format (e.g., BTC/USDT)')

        # Fetch OHLCV data for the past 30 days with 1-hour granularity
        ohlcv = uiui.fetch_ohlcv(symbol, '1h', hours=30*24)

        # Create DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Calculate percentage returns
        df['return'] = df['close'].pct_change()

        # Drop NaN values
        hourly_returns = df['return'].dropna()

        # Calculate the standard deviation of returns
        std_dev = hourly_returns.std()

        # Annualize the volatility (252 trading days * 24 hours per day)
        annualized_volatility = std_dev * np.sqrt(252 * 24)

        return annualized_volatility


#bybit_api_spy = BybitClient(api_key="LBVZOwpLoPyVe1iyya", api_secret="qJyRmW2DBfmrgkVk5YymcudZgDUArW3klILz")
# print(bybit_api_spy.get_volume('BTCUSDT', category='spot'))
# print(bybit_api_spy.get_volume('BTCUSD', category='linear'))
# print(bybit_api_spy.get_volatility('ETH/USD'))


# while True:
#    print(bybit_api_spy.orderbook(symbol='BTC-27JUN25-160000-P', category='option', limit=25))
# btc_options = bybit_api_spy.get_options_with_date(desired_date='2SEP24')
# print(f"len of available options : {len(btc_options)} and options {btc_options}")
# for option in btc_options:
#     print(bybit_api_spy.orderbook(symbol=option, category='option', limit=25))