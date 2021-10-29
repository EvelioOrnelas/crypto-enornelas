#!/usr/bin/env python

from bitcoin.rpc import RawProxy

url=None
port=18332 # testnet, use None for main net client
conf="/home/evelioornelas/.bitcoin/bitcoin.conf"

proxy = RawProxy(url,port,conf)

txid = "569391ffeb1724210aab003cc3b40783c6fcd4166aba22b1b7a70d435210e48b"
info = proxy.gettransaction(txid)
print(info)
