#!/usr/bin/env python

class Match(object):

	def __init__(self, match_id):
		import requests, json
		self.match_id = match_id

		r = requests.get("https://api.opendota.com/api/matches/{}".format(match_id))

		self._data = json.loads(r.text)

	@property
	def duration(cls):
		return cls._data["duration"]

	@property
	def players(cls):
		from .user import User

		for p in cls._data["players"]:
			try:
				yield User(p["account_id"])
			except AttributeError:
				yield "Anonymous"
