#!/usr/bin/env python

from bitcoin.rpc import RawProxy

url=None
port=18332 # testnet, use None for main net client
conf="/home/evelioornelas/.bitcoin/bitcoin.conf"

proxy = RawProxy(url,port,conf)

info = proxy.getblockcount()
balance = proxy.getbalance()
print("Number of blocks: " + str(info))
print("Balance: " + str(balance))