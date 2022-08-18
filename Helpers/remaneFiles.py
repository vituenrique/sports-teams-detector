import os
path = '../Detection/dataset/teamB'
files = os.listdir(path)

c = 0
d = 0
u = 0

for file in files:
	os.rename(os.path.join(path, file), os.path.join(path, 'teamB' + str(c) + str(d) + str(u) + '.png'))
	if u < 9:
		u += 1
	else:
		u = 0
		if d < 9:
			d += 1
		else:
			d = 0
			c += 1