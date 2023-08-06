Python CryptoCoin
=================

This python3 script is based on the `coinmarketcap
API <https://coinmarketcap.com/api/>`__

For getting coin data you can use the shortcodes for the coins.

So you don't have to use 'Basic Attention Token' but 'bat' is enough to
get the coin data.

Limits
------

Please limit requests to no more than 10 per minute.

Endpoints update every 5 minutes.

Create your own caching mechanism to keep requests to minimum

How do I get set up?
--------------------

-  Install this script with:

   -  pip3 py\_cryptocoin --upgrade (or pip py\_nsapi --upgrade )

-  ready to use it!

Current Coins
-------------

'btc' : 'Bitcoin', 'eth' : 'Ethereum', 'xrp' : 'Ripple', 'bch' :
'Bitcoin Cash', 'ada' : 'Cardano', 'ltc' : 'Litecoin', 'xem' : 'NEM',
'neo' : 'NEO', 'xlm' : 'Stellar', 'eos' : 'EOS', 'miota' : 'IOTA',
'dash' : 'Dash', 'xmr' : 'Monero', 'trx' : 'TRON', 'btg' : 'Bitcoin
Gold', 'icx' : 'ICON', 'qtum' : 'Qtum', 'etc' : 'Ethereum Classic',
'lsk' : 'Lisk', 'xrb' : 'RaiBlocks', 'ven' : 'VeChain', 'omg' :
'OmiseGO', 'usdt' : 'Tether', 'ppt' : 'Populous', 'zec' : 'Zcash', 'xvg'
: 'Verge', 'sc' : 'Siacoin', 'bnb' : 'Binance Coin', 'strat' :
'Stratis', 'bcn' : 'Bytecoin', 'steem' : 'Steem', 'ardr' : 'Ardor',
'snt' : 'Status', 'mkr' : 'Maker', 'rep' : 'Augur', 'bts' : 'BitShares',
'kcs' : 'KuCoin Shares', 'waves' : 'Waves', 'zrx' : '0x', 'doge' :
'Dogecoin', 'etn' : 'Electroneum', 'veri' : 'Veritaseum', 'kmd' :
'Komodo', 'dcr' : 'Decred', 'drgn' : 'Dragonchain', 'wtc' : 'Walton',
'dcn' : 'Dentacoin', 'lrc' : 'Loopring', 'ark' : 'Ark', 'salt' : 'SALT',
'qash' : 'QASH', 'dgb' : 'DigiByte', 'bat' : 'Basic Attention Token',
'gnt' : 'Golem', 'hsr' : 'Hshare', 'knc' : 'Kyber Network', 'gas' :
'Gas', 'wax' : 'WAX', 'ethos' : 'Ethos', 'pivx' : 'PIVX', 'gbyte' :
'Byteball Bytes', 'fun' : 'FunFair', 'aion' : 'Aion', 'rhoc' : 'RChain',
'zcl' : 'ZClassic', 'fct' : 'Factom', 'smart' : 'SmartCash', 'dent' :
'Dent', 'mona' : 'MonaCoin', 'elf' : 'aelf', 'powr' : 'Power Ledger',
'dgd' : 'DigixDAO', 'kin' : 'Kin', 'rdd' : 'ReddCoin', 'ae' :
'Aeternity', 'btm' : 'Bytom', 'nas' : 'Nebulas', 'sys' : 'Syscoin',
'req' : 'Request Network', 'nebl' : 'Neblio', 'link' : 'ChainLink',
'eng' : 'Enigma', 'xp' : 'Experience Points', 'gxs' : 'GXShares', 'maid'
: 'MaidSafeCoin', 'sub' : 'Substratum', 'xzc' : 'ZCoin', 'nxs' :
'Nexus', 'nxt' : 'Nxt', 'med' : 'MediBloc', 'emc' : 'Emercoin', 'btx' :
'Bitcore', 'bnt' : 'Bancor', 'cnd' : 'Cindicator', 'qsp' : 'Quantstamp',
'cnx' : 'Cryptonex', 'icn' : 'Iconomi', 'game' : 'GameCredits', 'pay' :
'TenX', 'part' : 'Particl'

Global Data
-----------

The global data return a Dictionary (DICT) with total market cap and
volume of currencies

Parameters
~~~~~~~~~~

Optional parameters: - (string) convert - return 24h volume, and market
cap in terms of another currency. Valid values are: - "AUD", "BRL",
"CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD", "HUF",
"IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD", "PHP",
"PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"

Return Fields
~~~~~~~~~~~~~

You will get a DICT with the followin fields

-  total\_market\_cap\_usd
-  total\_24h\_volume\_usd
-  bitcoin\_percentage\_of\_market\_cap
-  active\_currencies
-  active\_assets
-  active\_markets
-  last\_updated

Example code
~~~~~~~~~~~~

.. code:: python3

    import CryptoCoin

    cc = CryptoCoin()
    data = cc.getGlobalData() #standard currency (USD)

    #or

    data = cc.getGlobalData('EUR') #to get by currency

    print(data)

Coin Data
---------

Returns al information about one cryptocoin and the pricing

If you add the convert parameter it will return the cryptocoin price in
that currency

Parameters
~~~~~~~~~~

-  (string) cryptocoin shortcode, see Current Coins above what to use

Optional parameters: -(string) currency - return price, 24h volume, and
market cap in terms of another currency. Valid values are: - "AUD",
"BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR", "GBP", "HKD",
"HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR", "NOK", "NZD",
"PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR"

Return Fields
~~~~~~~~~~~~~

You will get a DICT with the followin fields

-  id
-  name
-  symbol
-  rank
-  price\_usd [depening on convert / currency]
-  price\_btc
-  24h\_volume\_usd [depening on convert / currency]
-  market\_cap\_usd [depening on convert / currency]
-  available\_supply
-  total\_supply
-  max\_supply
-  percent\_change\_1h
-  percent\_change\_24h
-  percent\_change\_7d
-  last\_updated

Example code
~~~~~~~~~~~~

.. code:: python3

    import CryptoCoin

    coin = "bat"

    cc = CryptoCoin()
    data = cc.(coin) # standard US Dollars

    #or

    data = cc.(coin, "EUR") #get the coin price back in Euro's

    print(data)

All Coins Data
--------------

Returns al information about all current know cryptocoins and the
pricing

If you add the convert parameter it will return the cryptocoin price in
that currency

Parameters
~~~~~~~~~~

Optional parameters: - (int) start - return results from rank [start]
and above - (int) limit - return a maximum of [limit] results (default
is 100, use 0 to return all results) - (string) currency - return price,
24h volume, and market cap in terms of another currency. Valid values
are: - "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK", "EUR",
"GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN", "MYR",
"NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY",
"TWD", "ZAR"

Return Fields
~~~~~~~~~~~~~

You will get a DICT with the followin fields

-  id
-  name
-  symbol
-  rank
-  price\_usd [depening on convert / currency]
-  price\_btc
-  24h\_volume\_usd [depening on convert / currency]
-  market\_cap\_usd [depening on convert / currency]
-  available\_supply
-  total\_supply
-  max\_supply
-  percent\_change\_1h
-  percent\_change\_24h
-  percent\_change\_7d
-  last\_updated

Example code
~~~~~~~~~~~~

.. code:: python3

    import CryptoCoin

    cc = CryptoCoin()
    data = cc.getAllCoinData() # Get default data in US Dollars

    start = 100
    limit = 10
    currency = "EUR"

    data = cc.getAllCoinData(start, limit, currrency)

    print(data)

Who do I talk to?
-----------------

-  Theodorus van der Sluijs
-  theo@vandersluijs.nl

License
-------

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

You are free to:
~~~~~~~~~~~~~~~~

-  Share — copy and redistribute the material in any medium or format
-  Adapt — remix, transform, and build upon the material

-The licensor cannot revoke these freedoms as long as you follow the
license terms.-

Under the following terms:
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Attribution — You must give appropriate credit, provide a link to the
   license, and indicate if changes were made. You may do so in any
   reasonable manner, but not in any way that suggests the licensor
   endorses you or your use.
-  NonCommercial — You may not use the material for commercial purposes.
-  ShareAlike — If you remix, transform, or build upon the material, you
   must distribute your contributions under the same license as the
   original.

