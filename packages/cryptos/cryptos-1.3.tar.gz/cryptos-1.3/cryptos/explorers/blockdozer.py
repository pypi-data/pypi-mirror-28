from . import base_insight as insight

base_url = "http://%s.blockdozer.com/insight-api"

def unspent(*args, coin_symbol="btc"):
    base_url_for_coin = base_url % coin_symbol
    return insight.unspent(base_url_for_coin, *args)

def pushtx(tx,  coin_symbol="btc"):
    base_url_for_coin = base_url % coin_symbol
    return insight.pushtx(base_url_for_coin, coin_symbol, tx)

def fetchtx(tx, coin_symbol="btc"):
    base_url_for_coin = base_url % coin_symbol
    return insight.fetchtx(base_url_for_coin, tx)

def txinputs(tx, coin_symbol="btc"):
    base_url_for_coin = base_url % coin_symbol
    return insight.txinputs(base_url_for_coin, tx)

def history(*args,  coin_symbol="btc"):
    base_url_for_coin = base_url % coin_symbol
    return insight.history(base_url_for_coin, *args)
