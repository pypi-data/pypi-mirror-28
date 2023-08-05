# -*- encoding: utf8 -*-
# © Toons

"""
Usage: 
    network use [<name> -b <number> -l <ms>]
    network browse [-t|-a <id>]
    network publickey <secret>
    network address <secret>
    network wif <secret>
    network delegates
    network staking

Options:
-b <number> --broadcast <number> peer number to use for broadcast       [default: 10]
-l <ms> --latency <ms>           maximum latency allowed in miliseconds [default: 5000]
-t <id> --transaction <id>       transaction id to browse
-a <id> --address <id>           address id to browse

Subcommands:
    use       : select network.
    browse    : browse network.
    publickey : returns public key from secret.
    address   : returns address from secret.
    delegates : show delegate list.
    staking   : show coin-supply ratio used on delegate voting.
"""

from .. import rest
from .. import cfg
from .. import util

from . import DATA

import arky
import sys
import imp
import webbrowser

def _whereami():
	return "network"


def use(param):
	if not param["<name>"]:
		choices = util.findNetworks()
		if choices:
			param["<name>"] = util.chooseItem("Network(s) found:", *choices)
		else:
			sys.stdout.write("No Network found\n")
			return False

	DATA.initialize()

	rest.use(
		param.get("<name>"),
		broadcast=int(param.get("--broadcast", 10)),
		timeout=float(param.get("--latency", 5000))/1000
	)


def browse(param):
	if param["--transaction"]:
		webbrowser.open(cfg.explorer + "/tx/" + param["--transaction"])
	elif param["--address"]:
		webbrowser.open(cfg.explorer + "/address/" + param["--address"])
	else:
		webbrowser.open(cfg.explorer)


def address(param):
	sys.stdout.write("    %s\n" % arky.core.crypto.getAddress(arky.core.crypto.getKeys(param["<secret>"].encode("ascii"))["publicKey"]))


def publickey(param):
	sys.stdout.write("    %s\n" % arky.core.crypto.getKeys(param["<secret>"].encode("ascii"))["publicKey"])


def wif(param):
	sys.stdout.write("    %s\n" % arky.core.crypto.getKeys(param["<secret>"].encode("ascii")).get("wif", "This blockchaine does not use WIF"))


def delegates(param):
	resp = rest.GET.api.delegates()
	if resp["success"]:
		delegates = resp["delegates"]
		maxlen = max([len(d["username"]) for d in delegates])
		i = 1
		for name, vote in sorted([(d["username"], float(d["vote"])/100000000) for d in delegates], key=lambda e: e[-1], reverse=True):
			sys.stdout.write("    #%02d - %s: %.3f\n" % (i, name.ljust(maxlen), vote))
			i += 1
	else:
		sys.stdout.write("%s\n    Error occured using peer %s... retry !\n" % (resp["error"], resp.get("peer", "???")))


def staking(param):
	sys.stdout.write("    %.2f%% of coin supply used to vote for delegates\n" % sum(d["approval"] for d in util.getCandidates()))
