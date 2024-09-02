# 🚀 Crypto Trading Bots & API Clients

Welcome to my **CryptoClients** repository! This repository houses a collection of sophisticated clients and automation scripts tailored for cryptocurrency trading on popular exchanges such as **MEXC** and **Bybit**. Whether you're automating trades, collecting data, or building custom trading strategies, this repository has the tools you need.

NOTE:**PLEASE UPPON NOTICING ANYTHING UNUSUAL CONTACT ME TO CHECK IT OUT. I CARRY NO RESPONSIBILITY FOR ANYTHING THAT HAPPENS TO YOUR TRADING ACCOUNTS.**
## 📁 Projects Overview

### 1. **MEXC Client with HTTP Requests**
This client interfaces with the MEXC exchange using direct HTTP requests. It's designed to be lightweight and efficient, perfect for scenarios where speed and resource management are crucial.

- **Features**:
  - 📈 **Market Data Retrieval**: Fetch live market data, order book details, and more.
  - 💼 **Account Management**: Manage your account, including balances, orders, and positions.
  - 🤖 **Automated Trading**: Execute automated trades based on predefined strategies. --ENDPOINT UNDER MAINTANCE (FROM EXCHANGE'S SIDE)

- **Initialization**:
  ```bash
  api_key = "REPLACE_WITH_YOUR_ACTUAL_API_KEY"
  api_secret = "REPLACE_WITH_YOUR_ACTUAL_API_SECRET"
  mexcApi = mexcClient(api_key, secret_key)
  
  #TESTING ORDERBOOK RETRIEVAL
  print(mexcApi.orderbook('AEVO_USDT',100))
  
  #TESTING HISTORY OF POSITIONS
  print(mexcApi.history_positions())
  
  #TESTING PRICE RETRIEVAL FUNCTION (FOR FUTURES ENDPOINT)
  print(mexcApi.get_future_price('AEVO_USDT'))
  
  #TESTING ALL ASSETS WALLET ENDPOINT
  print(mexcApi.see_wallet())
  
  #TESTING SPECIFIC ASSET WALLET ENDPOINT (USDT)
  print(mexcApi.see_wallet_on_symbol('USDT'))
  
  TESTING LEVERAGE RETRIEVAL ON COIN (AEVO)
  # print(mexcApi.get_leverage('AEVO_USDT'))
  
  #TESTING OPEN NEW POSITION ON COIN (AEVO)
  print(mexcApi.open_market('AEVO_USDT', 1,1))
  
  #TESTING RISK LEVEL CHANGE (ACTUALLY JUST GENERAL POST REQUESTS)
  # print(mexcApi.change_risk_level())
  
  #TESTING LEVERAGE CHANGE ON COIN (AEVO)
  print(mexcApi.set_leverage('AEVO_USDT',20))

### 2. **MEXC Client with SELENIUM**
This client interfaces with the MEXC webpage using the selenium library (kinda like interface).It's designed because trading futures endpoint in MEXC is under Maintance. Please view Policies of the exchange before using it.
It requires a webpage to wrap (logged in and having selected a trading pair)

- **Features**:
  - 📈 **Setting Quantites**: Set Quantity to trade.
  - 🤖 **Positions Opening**: Open positions (both long and short)
  - 🤖 **Positions Handling**: Handle your positions (currently only close all supported)

- **Initialization**:
  ```bash
   #FETCH PRICE OF COIN (THAT IS VISUAL AVAIALBLE IN WEBPAGE)
  price_shown_in_webpage=print(float(get_future_price()))
  
  #LOAD QUANTITY FOR TRADE
  set_quantity(quantity)
  
  #OPEN A POSITION HAVING THE QUANTITY LOADED
  open_position_quantity_loaded('LONG')
  
  #OPEN A POSITION WITHOUT HAVING THE QUANTITY LOADED
  open_position('LONG', quantity)
  
  #FLASH/COMPLETLY CLOSE ALL POSITIONS
  close_all_positions()

 ### 3. **Bybit Client using pre-existent Libraries**
Personally found it really hard to navigate to pybits undocumented and chaotic library (it's so maybe because it's unofficial, bybit's official api documentation will guide you for HTTP requests) so I created my own to do the task. I share it with everyone, as it's plain simple and does the job!

- **Features**:
  - 📈 **Market Data Retrieval**: Fetch live market data, order book details, and more.
  - 💼 **Account Management**: Manage your account, including balances, orders, and positions.
  - 🤖 **Automated Trading**: Execute automated trades based on predefined strategies.

- **Initialization**:
  ```bash
  bybit_api = BybitClient(api_key="REPLACE_WITH_YOUR_ACTUAL_KEY", api_secret="REPLACE_WITH_YOUR_ACTUAL_SECRET")
  
  #TEST RETRIEVING FUTURE PRICE
  print(bybit_api.get_future_price('BTCUSDT'))
  
  #TEST RETRIEVING SPOT PRICE
  print(bybit_api.get_spot_price('BTCUSDT'))
  
  #TEST RETRIEVING SPECIFIC BALANCE ON SYMBOL
  print(bybit_api.get_wallet_balance_on_symbol('USDT'))
  
  #TEST RETREIVING OVERALL BALANCE
  print(bybit_api.get_wallet_balance())
  
  #TEST RETRIEVING INFO ON OPEN FUTURE POSITION
  print(bybit_api.get_future_position_info('BTCUSDT'))
  
  #TEST RETRIEVING INFO ON ALL FUTURE POSITIONS
  print(bybit_api.get_all_futures_positions())
  
  #TEST SETTING LEVERAGE FOR TRADING PAIR (BOTH SPOT AND FUTURES)
  print(bybit_api.set_leverage('BTCUSDT', buyLev, sellLev))
  
  #TEST OPENING MARKET POSITION ON FUTURES
  print(bybit_api.open_futures_position('BTCUSDT', 'LONG', quantity))
  
  #VOLUME RETRIEVAL TEST
  print(bybit_api.get_volume('BTCUSDT', category='spot'))
  print(bybit_api.get_volume('BTCUSD', category='linear'))
  
  #VOLATILITY RETRIEVAL TEST
  print(bybit_api.get_volatility('ETH/USD'))
  
  
  #ORDERBOOK FOR OPTIONS FETCH TEST
  print(bybit_api.orderbook(symbol='BTC-27JUN25-160000-P', category='option', limit=25))
  
  #FETCH OPTIONS WITH EXPIRY DATE TEST --I THINK COIN IS ALSOA PARAMETER AND SET TO BTC AS DEFAULT
  options = bybit_api.get_options_with_date(desired_date='2SEP24')
