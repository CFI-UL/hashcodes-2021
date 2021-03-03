import os, binascii, json

def random_id():
	return binascii.b2a_hex(os.urandom(16)).decode()

class Team:
	def __init__(self, name, participants, team_id=random_id(), best=0):
		self.id = random_id()
		self.name = name
		self.participants = participants
		self.best = 0

	def __repr__(self):
		return f'{self.name}({self.best})'

	def to_dict(self):
		return vars(self)

def from_json(data):
	return Team(data['name'], data['participants'], data['id'], int(data['best']))