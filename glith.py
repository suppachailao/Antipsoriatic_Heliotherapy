from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

dataP = Path.cwd() / 'dat_full' 
listdata = [child for child in dataP.iterdir()] 

def plot(file):

	with open(file, 'r') as f:
		listI = list(f)

	xlines, ylines = [], []

	for str_line in listI[:-1]:
		if str_line.strip():
			list_line = str_line.split()
			xlines.append(float(list_line[0]))
			ylines.append(float(list_line[1]) /1000)

	plt.plot(xlines, ylines)
	plt.title(file.name)

# plot(listdata[700])
# plt.show()


g = np.array([1, 3, 5, 1])
f = (np.abs(np.diff(g)))
print (f)
print (f.max())


def maxDiff():

	dataP = Path.cwd() / 'dat_full' 
	listdata = [child for child in dataP.iterdir()]
	box_max = []

	for i in range(len(listdata)):

		with open(listdata[i], 'r') as f:
			listA = list(f)
			# print (f.name)

		Ir = np.array([float(line.strip().split()[1]) /1000 for line in listA[:-1]]) #Irradiance(wl)
		diff = (np.abs(np.diff(Ir)))
		box_max.append(diff.max())

	box_max = np.array(box_max)

	return box_max


# maxDiffA = maxDiff()
if not (Path.cwd() / 'result' / 'maxDiffA.npy').exists(): 
	np.save(Path.cwd() / 'result' / 'maxDiffA.npy', maxDiffA)

if not (Path.cwd() / 'result' / 'maxDiffA.npy').exists():
	maxDiffB = np.load(Path.cwd() / 'result' / 'maxDiffA.npy')
print (maxDiffB.max())
	print (maxDiffB.min())