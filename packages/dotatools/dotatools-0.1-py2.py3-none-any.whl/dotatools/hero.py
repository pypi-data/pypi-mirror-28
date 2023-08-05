#!/usr/bin/env python

import requests, json, re

class Hero(object):
	try:
		r = requests.get("https://api.opendota.com/api/heroes", timeout=30)
	except requests.exceptions.ReadTimeout:
		print("Request timed out!")
		exit(1)

	__data = json.loads(r.text)

	def __init__(self, hero_id):
		self.hero_id = hero_id

		for i in self.__data:
			if i["id"] == hero_id:
				self.id = i["id"]


	@property
	def name(cls):
		try:
			return cls.__data[cls.id]["name"][14:]
		except:
			pass


	@property
	def localname(cls):
		try:
			return cls.__data[cls.id]["localized_name"]
		except:
			pass

	@property
	def stats(cls):
		try:
			r = requests.get("https://api.opendota.com/api/heroStats", timeout=30)
			herostats = json.loads(r.text)

		except requests.exceptions.ReadTimeout:
			print("Request timed out!")
			exit(1)

		for hero in herostats:
			picks = 0
			wins = 0
			for stat in hero:
				if re.search('^\d+_pick', stat):
					picks += int(hero[stat])
				if re.search('^\d+_win', stat):
					wins += int(hero[stat])
			winrate = wins*100.0 / picks
			hero.update({"pub_picks": picks})
			hero.update({"pub_wins": wins})
			hero.update({"pub_winrate": winrate})

		for h in herostats:
			if h["id"] == cls.id:
				return h
