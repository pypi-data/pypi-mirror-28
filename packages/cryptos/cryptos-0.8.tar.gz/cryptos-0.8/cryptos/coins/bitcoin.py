from ..explorers import sochain
from ..transaction import SIGHASH_ALL, select, mksend
from .. import main, transaction
from .base import BaseCoin


class Bitcoin(BaseCoin):
    coin_symbol = "BTC"
    display_name = "Bitcoin"
    magicbyte = 0
    hashcode = SIGHASH_ALL

    def __init__(self, testnet=False, **kwargs):
        super(Bitcoin, self).__init__(testnet, **kwargs)
        if self.is_testnet:
            self.display_name = "Bitcoin Testnet"
            self.coin_symbol = "BTCTEST"
            self.magicbyte = 111

    def privtopub(self, privkey):
        return main.privtopub(privkey)

    def pubtoaddr(self, pubkey):
        return main.pubtoaddr(pubkey, magicbyte=self.magicbyte)

    def privtoaddr(self, privkey):
        return main.privtoaddr(privkey, magicbyte=self.magicbyte)

    def sign(self, tx, i, privkey):
        return transaction.sign(tx, i, privkey, magicbyte=self.magicbyte, hashcode=self.hashcode)

    def signall(self, tx, privkey):
        return transaction.signall(tx, privkey, magicbyte=self.magicbyte, hashcode=self.hashcode)

    def unspent(self, *addrs, **kwargs):
        return sochain.unspent(*addrs, coin_symbol=self.coin_symbol, **kwargs)

    def history(self, *addrs, **kwargs):
        return sochain.history(*addrs, coin_symbol=self.coin_symbol, **kwargs)

    def fetchtx(self, tx):
        return sochain.fetchtx(tx, coin_symbol=self.coin_symbol)

    def txinputs(self, tx):
        return sochain.txinputs(tx, coin_symbol=self.coin_symbol)

    def pushtx(self, tx):
        return sochain.pushtx(tx, coin_symbol=self.coin_symbol)

    # Takes privkey, address, value (satoshis), fee (satoshis)
    def send(self, privkey, to, value, fee=10000):
        return self.sendmultitx(privkey, to + ":" + str(value), fee)

    # Takes privkey, address1:value1,address2:value2 (satoshis), fee (satoshis)
    def sendmultitx(self, privkey, *args):
        frm = self.privtoaddr(privkey)
        tx = self.preparemultitx(frm, *args)
        tx2 = self.signall(tx, privkey)
        return self.pushtx(tx2)

    # Takes address, address, value (satoshis), fee(satoshis)
    def preparetx(self, frm, to, value, fee=10000):
        tovalues = to + ":" + str(value)
        return self.preparemultitx(frm, tovalues, fee)

    # Takes address, address:value, address:value ... (satoshis), fee(satoshis)
    def preparemultitx(self, frm, *args):
        tv, fee = args[:-1], int(args[-1])
        outs = []
        outvalue = 0
        for a in tv:
            outs.append(a)
            outvalue += int(a.split(":")[1])

        u = self.unspent(frm)
        u2 = select(u, int(outvalue) + int(fee))
        argz = u2 + outs + [frm, fee]
        return mksend(*argz)
