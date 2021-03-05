import json
import socket

address = ('localhost', 1337)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)
print(s.recv(2048).decode())

token = input('Insert team token: ')
chall = input('Insert challenge id: ')
sol = input('Insert solution filename: ')

sol_txt = ''
with open(sol, 'r') as f:
	sol_txt = f.read()

data = {
	'method': 'challenge',
	'team_id': token,
	'chall_id': chall,
	'solution': sol_txt
}

print(f'Trying challenge {chall} with token {token}...')

m = json.dumps(data).encode() + b'\n'
s.sendall(m)
print(s.recv(2048).decode())