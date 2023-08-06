import ccxt
import yaml


def open_coinbase(key, secret):
    from coinbase.wallet.client import Client

    class Coinbase(object):

        def __init__(self):
            self.client = Client(key, secret)

        def fetch_balance(self):
            total = {}
            for account in self.client.get_accounts()["data"]:
                balance = account["balance"]
                total[balance["currency"]] = float(balance["amount"])
            return {'total': total}

    return Coinbase()


def open_exchange(name, key, secret, uid):
    if name == 'coinbase':
        return open_coinbase(key, secret)
    klass = getattr(ccxt, name)
    credentials = {
        'apiKey': key,
        'secret': secret
    }
    if uid is not None:
        credentials['uid'] = str(uid)
    return klass(credentials)


def load_exchanges(yaml_file):
    exchange_balances = {}
    with open(yaml_file, 'rb') as f:
        config = yaml.load(f.read())
        for exchange in config:
            name = exchange['name']
            instance = open_exchange(name,
                                     exchange['key'],
                                     exchange['secret'],
                                     exchange.get('uid'))

            balances = instance.fetch_balance()['total']
            exchange_balances[name] = {coin: q for coin, q in balances.items()
                                       if q != 0.0}
    return exchange_balances