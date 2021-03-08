import os, binascii, json

def random_id():
	return binascii.b2a_hex(os.urandom(16)).decode()

class Team:
	def __init__(self, name, participants, team_id=random_id(), score={'0':0, '1':0, '2':0}):
		self.id = random_id()
		self.name = name
		self.participants = participants
		self.score = score

	def __repr__(self):
		return f'{self.name}({self.get_score()})'

	def to_dict(self):
		return vars(self)

	def get_score(self):
		return sum(self.score.values())

def from_json(data):
	score = {i:int(data['score'][i]) for i in data['score']}
	return Team(data['name'], data['participants'], data['id'], score)


if __name__ == '__main__':
	print(sum({'0':6, '1':6, '2':6}.values()))