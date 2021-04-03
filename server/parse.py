import teams
import json

def team_sorter(t):
	return t.get_score()

data = ''
with open('teams.cfi', 'r') as f:
	data = json.load(f)

out = []
for team in data:
	out.append(teams.from_json(team))

podium = sorted(out, key=team_sorter, reverse=True)
print(podium)