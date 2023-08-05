#!/usr/bin/env python

import argparse
import json

import requests

import dotatools

print("Let's begin!")

r = requests.get('https://api.opendota.com/api/publicMatches')
data = json.loads(r.text)

print("Random public match gathered!")

m = dotatools.Match(data[0]["match_id"])

print("Compiling list of player names...\n")

for u in list(p.personaname for p in m.players):
	print(u)
