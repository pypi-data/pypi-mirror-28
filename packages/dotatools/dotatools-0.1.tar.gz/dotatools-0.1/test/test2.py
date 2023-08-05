#!/usr/bin/env python

import dotatools

print("Current heroes in Dota 2 are:")

failcount = 0
id_lookup = 0

while failcount < 10:
	h = dotatools.Hero(id_lookup)

	if h.localname:
		print("ID {:03d}: {:<25} 'Code' name: {}".format(id_lookup, h.localname, h.name.title()))
	else:
		failcount += 1

	id_lookup += 1
