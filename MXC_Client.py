import datetime

import hmac
import time
import requests
import hashlib
from typing import Union, Literal
from urllib.parse import urlencode


api_key =  'YOUR_API_KEY'  
secret_key = 'YOUR_SECRET_KEY' 


import json

class mexcClient:
    """INITIALIZER-CONSTRUCTOR"""
    def __init__(self, api_key, secret_key):
        self.session = futures.HTTP(api_key, secret_key)
        self.requests = requests.Session()
        self.api_key=api_key
        self.secret_key=secret_key
        self.requests.headers.update({
            "Content-Type": "application/json",})
        self.base_url = "https://contract.mexc.com"
    #CORE STUFF


    """ UTIL FUNCTION TO SIGN THE REQUEST"""
    def sign(self, timestamp: str, param_string: str) -> str:
        """
        Generates a signature for an API request using HMAC SHA256 encryption.

        :param timestamp: A string representing the timestamp of the request.
        :type timestamp: str
        :param param_string: The parameter string to be signed.
        :type param_string: str

        :return: A hexadecimal string representing the signature of the request.
        :rtype: str
        """
        query_string = self.api_key + timestamp + param_string
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature

    """ALL ENDPOINTS SHOULD BE CALLED THROUGH THIS -- SIGNS THE REQUEST"""

    def call(self, method: Union[Literal["GET"], Literal["POST"], Literal["PUT"], Literal["DELETE"]], router: str,
             *args, **kwargs) -> dict:
        """
        Makes a request to the specified HTTP method and router using the provided arguments.

        :param method: A string that represents the HTTP method (GET, POST, PUT, or DELETE) to be used.
        :type method: str
        :param router: A string that represents the API endpoint to be called.
        :type router: str
        :param *args: Variable length argument list.
        :type *args: list
        :param **kwargs: Arbitrary keyword arguments.
        :type **kwargs: dict

        :return: A dictionary containing the JSON response of the request.
        """
        if not router.startswith("/"):
            router = f"/{router}"

        # clear None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if self.api_key and self.secret_key:
            timestamp = str(int(time.time() * 1000))
            param_string = ""
            headers = {
                "Request-Time": timestamp,
                "ApiKey": self.api_key
            }

            if method in ["GET", "DELETE"]:
                param_string = urlencode(sorted(kwargs.get('params', {}).items()))
            elif method in ["POST", "PUT"]:
                param_string = kwargs.get('json', "")
                headers["Content-Type"] = "application/json"


                # json_data = kwargs.get('json', {})
                # param_string = json.dumps(json_data, separators=(',', ':'))
                # headers["Content-Type"] = "application/json"
                # kwargs['json'] = json_data

            signature = self.sign(timestamp, param_string)
            headers["Signature"] = signature
            kwargs['headers'] = headers

            # print(timestamp)
            # print(signature)

        response = requests.request(method, f"{self.base_url}{router}", *args, **kwargs)
        return response.json()



    """GETS CURRENT FUTURE PRICE ON SUPPORTED CURRENCY -- RATE LIMIT 10 TIMES PER 1 SECOND -- USE TIME.SLEEP(1)"""
    def get_future_price(self, symbol): #WORKS
        try:
            response = self.call("GET", f"/api/v1/contract/index_price/{symbol}")
            response = response['data']
            return float(response['indexPrice'])
        except Exception as e:
            print(e)

    """SEE PREVIOUS POSITIONS"""

    def history_positions(self, symbol=None, type=None, page_num=1, page_size=20):
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        if symbol:
            params["symbol"] = symbol
        if type:
            params["type"] = type

        response =  self.call("GET", "/api/v1/private/position/list/history_positions", params=params)
        #print(response)
        response = response['data'][0]
        coin = response['symbol']
        open = response['openAvgPrice']
        close = response['closeAvgPrice']
        return coin, open, close

    """ACCESSES WHOLE WALLET -- REQUIRES SIGNATURE"""
    def see_wallet(self):
        response = self.call("GET", "api/v1/private/account/assets")
        return response

    """ACCESSES WALLET ON REQUESTED CURRENCY -- REQUIRES SIGNATURE"""
    def see_wallet_on_symbol(self, symbol):
        try:
            response = self.call("GET", f"api/v1/private/account/asset/{symbol}")
            data = response['data']
            amount = data['cashBalance']
            return float(amount)
        except Exception as e:
            print(e)

    """ GETS/SETS LEVERAGE FOR A FUTURES TRADE PAIR -- BOTH RATE LIMIT 10 TIMES PER 1 SECOND"""
    def get_leverage(self, symbol):
        response =  self.call("GET", "api/v1/private/position/leverage",
                             params=dict(
                                 symbol=symbol
                             ))
        position_type = response['data'][0]['positionType']
        data = response['data'][0]
        return float(data['leverage'])#, int(position_type)
    """ SET LEVERAGE IS CURRENTLY UNSUPPORTED, PLEASE PROCEED TO DO SO MANUALLY"""
    def set_leverage(self, symbol, lev):
        current_lev, posType = self.get_leverage(symbol)
        response = self.call("POST", "api/v1/private/position/change_leverage",
                         params=dict(
                             positionId=None,
                             leverage= lev,
                             openType=2,
                             symbol=symbol,
                             positionType=posType
                         ))
        print(response)

    """ OPEN POSITION -- DIRECTIONS: 1=OPEN LONG, 2=CLOSE SHORT, 3=OPEN SHORT, 4=CLOSE LONG"""
    """NOTE:order direction 1 open long ,2close short,3open short ,4 close long"""
    #TODO: add different call for POST REQUESTS!!!
    def open_market(self,
              symbol: str,
              vol: float,
              side: int) -> dict:
        time.sleep(1)
        return self.call("POST", "api/v1/private/order/submit",
                            # params = dict(
                            #         symbol = symbol,
                            #         price = 0.9,
                            #         vol = vol,
                            #         side = side,
                            #         type = 5,
                            #         openType = 2,
                            #         positionId = None,
                            #         leverage = None,
                            #         externalOid = None,
                            #         stopLossPrice = None,
                            #         takeProfitPrice = None,
                            #         positionMode = None,
                            #         reduceOnly = None
                            # ))
                         params={
                             "symbol": symbol,
                             "price": 0.9,
                             "vol": vol,
                             "side": side,
                             "type": 5,
                             "openType": 2,
                             "positionId": None,
                             "leverage": None,
                             "externalOid": None,
                             "stopLossPrice": None,
                             "takeProfitPrice": None,
                             "positionMode": None,
                             "reduceOnly": None
                         })
    def change_risk_level(self) -> dict:
        """
        ### Switch the risk level

        https://mexcdevelop.github.io/apidocs/contract_v1_en/#switch-the-risk-level

        :return: None
        :rtype: None
        """

        return self.call("POST", "api/v1/private/account/change_risk_level")

    def orderbook(self, symbol, limit):
        response = self.call("GET", f"api/v1/contract/depth_commits/{symbol}/{limit}")
        if response['code'] == 0 and response['data']:
            aggregated_bids = []
            aggregated_asks = []
            for snapshot in response['data']:
                aggregated_bids.extend(snapshot['bids'])
                aggregated_asks.extend(snapshot['asks'])

            # Sort and deduplicate
            aggregated_bids = sorted(set(tuple(bid) for bid in aggregated_bids), key=lambda x: x[0], reverse=True)
            aggregated_asks = sorted(set(tuple(ask) for ask in aggregated_asks), key=lambda x: x[0])

            # Get the timestamp from the response
            timestamp = int(datetime.datetime.now().timestamp() * 1000)

            return {
                'bids': aggregated_bids,
                'asks': aggregated_asks,
                'timestamp': timestamp,
                'datetime': datetime.datetime.utcfromtimestamp(timestamp / 1000).isoformat(),
                'nonce': response['data'][0]['version'] if response['data'] else None
            }
        else:
            timestamp = int(datetime.datetime.now().timestamp() * 1000)
            return {
                'bids': [],
                'asks': [],
                'timestamp': timestamp,
                'datetime': datetime.datetime.utcfromtimestamp(timestamp / 1000).isoformat(),
                'nonce': None
            }


