import teams as teams_module
from handler import Handler
import socketserver
import json
import exceptions
import os

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def dump_teams_as_json(teams):
	return [teams[team_id].to_dict() for team_id in teams]

def read_teams_from_json(teams):
	return {team['id']: teams_module.from_json(team) for team in teams}

def read_teams():
	data = ''
	with open('teams.cfi', 'r') as f:
		try:
			data = json.loads(f.read())
		except:
			return {}
	return read_teams_from_json(data)

def dump_teams(teams):
	data = dump_teams_as_json(teams)
	with open('teams.cfi', 'w') as f:
			f.write(json.dumps(data, default=json_serial))

class HashcodeTCPServer(socketserver.TCPServer):
	def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
		super().__init__(server_address, RequestHandlerClass, bind_and_activate)
		self.teams = read_teams()
		
	def register_team(self, team):
		t = read_teams()

		if team.id in t:
			raise exceptions.TeamAlreadyExistsException()
		
		t[team.id] = team
		
		self.teams = t
		dump_teams(t)

	def get_team(self, team_id):
		return self.teams[team_id]

port = 1337
print(f'Starting server on internal port: {port}')
address = ('0.0.0.0', port)
s = HashcodeTCPServer(address, Handler)

print(f'Starting server with teams:\n{s.teams}')
s.serve_forever()