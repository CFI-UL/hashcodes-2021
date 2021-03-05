import socketserver
import json
import teams

from exceptions import TeamAlreadyExistsException
from validator import Validator

class Handler (socketserver.StreamRequestHandler):
	maps = [ 'maps/busy_day.in', 'maps/mother_of_all_warehouses.in', 'maps/redundancy.in' ]

	def handle(self):
		# 2 formats disponible

		# method: register
		# {
		# 	method: "register",
		# 	team_name: "enter name here",
		#	participants: ["part1", "part2", "part3", "part4"]
		# }
		# {"method":"register", "team_name":"yeet", "participants":["oli","leo"]}

		# method: challenge
		# {
		# 	method: "challenge",
		#	team_id: "team identifier",
		#	chall_id: "challenge identifier",
		#	solution: "solution"
		# }

		self.wfile.write(b'Successfully connected...\n')
		m = self.rfile.readline()

		if not m:
			return

		try:
			data = json.loads(m)
		except Exception as e:
			self.wfile.write(f'Could not parse json entry.\n{e}\n'.encode())
			return

		method = data['method']
		if method == 'register':
			try:
				self.register(data)
			except:
				self.wfile.write(b'Unknown error in registration, please try again.\n')
				raise
		elif method == 'challenge':
			t = self.identify(data['team_id'])
			if t is None: return

			try:
				challenge = self.maps[int(data['chall_id'])]
			except:
				chall = data['chall_id']
				self.wfile.write(f'Unknown challenge: {chall}'.encode())

			with open(challenge, 'r') as f:
				chall_data = f.read().splitlines()

			v = Validator()

			try:
				score = v.verify(chall_data, data['solution'].splitlines())
				self.wfile.write(f'Success! Your score is: {score}'.encode())
				t.score = max(score, t.score)
			except Exception as e:
				self.wfile.write(f'{e}\n'.encode())

		else:
			self.wfile.write(f'Unknown method: {method}\n'.encode())

	def register(self, data):
		team = teams.Team(data['team_name'], data['participants'])

		try:
			self.server.register_team(team)
			mess = f'Successfully registered team "{team.name}". Unique identifier: {team.id}\n'
			self.wfile.write(mess.encode())
		except TeamAlreadyExistsException:
			print('Trying again...')

	def identify(self, identifier):
		try:
			return self.server.get_team(identifier)
		except:
			self.wfile.write(f'Unknown team identifier: {identifier}'.encode())

