#!/usr/bin/env python

import requests, json

class User(object):

	def __init__(self, steamID):
		self.steamID = steamID

		# Load profile data upon defining class object to reduce load on API
		r = requests.get("https://api.opendota.com/api/players/{}".format(self.steamID))
		self._data = json.loads(r.text)

	@property
	def personaname(self):
		"""Returns the 'personaname' or Steam nickname. This is only updated up until the most recent tracked match"""
		data = self._data

		try:
			return data["profile"]["personaname"].encode('utf-8')
		except KeyError:
			return "Anonymous"

	@property
	def lastmatch(cls, significant=1):
		r = requests.get("https://api.opendota.com/api/players/{}/matches?significant={}&limit=1".format(cls.steamID, significant))
		j = json.loads(r.text)

		return (j[0]["match_id"])
