import socketserver
import json
import teams

from exceptions import TeamAlreadyExistsException
from validator import Validator
from datetime import time as datetime

class Handler (socketserver.StreamRequestHandler):
	maps = [ 'maps/busy_day.in', 'maps/mother_of_all_warehouses.in', 'maps/redundancy.in' ]

	def send_message(self, message):
		self.wfile.write(message.encode() + b'\r\n')

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

		self.send_message('Successfully connected...')
		m = self.rfile.readline()

		if not m:
			self.send_message('Please, for the love of god, don\'t send empty requests.')
			return

		try:
			data = json.loads(m)
		except Exception as e:
			print(e)
			self.send_message(f'Could not parse json entry.\n{e}')
			return

		method = data['method']
		if method == 'register':
			try:
				self.register(data)
			except:
				self.send_message('Unknown error in registration, please try again.')
				raise
		elif method == 'challenge':
			t = self.identify(data['team_id'])
			if t is None:
				self.send_message(f'Could not identify team with id {data["team_id"]}')
				return

			if not t.verify_delay():
				self.send_message('Please wait at least 30 seconds between requests.')
				return

			try:
				challenge = self.maps[int(data['chall_id'])]
			except:
				chall = data['chall_id']
				self.send_message(f'Unknown challenge: {chall}')
				return

			with open(challenge, 'r') as f:
				chall_data = f.read().splitlines()

			v = Validator()

			try:
				score = v.verify(chall_data, data['solution'].splitlines())
				self.send_message(f'Success! Your score is: {score}')
				t.score[data['chall_id']] = max(score, t.score[data['chall_id']])
				t.update_last_validation()
				self.server.save_teams()
				
			except Exception as e:
				self.send_message(str(e))
				raise e
		else:
			self.send_message(f'Unknown method: {method}')

	def register(self, data):
		team = teams.Team(data['team_name'], data['participants'])

		while True:
			try:
				self.server.register_team(team)
				mess = f'Successfully registered team "{team.name}". Unique identifier: {team.id}'
				self.send_message(mess)
				break
			except TeamAlreadyExistsException:
				print('Trying again...')

	def identify(self, identifier):
		try:
			return self.server.get_team(identifier)
		except:
			self.send_message(f'Unknown team identifier: {identifier}')

