#!/usr/bin/env python

import argparse

import dotatools

parser = argparse.ArgumentParser()
parser.add_argument('user_id')
u = dotatools.User(parser.parse_args().user_id)

if u.lastmatch:
	print("Found last match successfully!")
