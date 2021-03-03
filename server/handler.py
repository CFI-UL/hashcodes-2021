import socketserver
import json
import teams

from exceptions import TeamAlreadyExistsException

class Handler (socketserver.StreamRequestHandler):

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

		self.wfile.write(b'Listening...\n')
		m = self.rfile.readline()
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
			self.identify(data)
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
			self.register(data)

	def identify(self, identifier):
		try:
			self.server.get_team(identifier)
		except:
			self.wfile.write(f'Unknown team identifier: {identifier}'.encode())
