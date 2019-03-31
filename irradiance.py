from pathlib import Path
import h5py
import numpy as np
from matplotlib import pyplot as plt

dName = 'dat_full'
filesInPath = [child for child in (Path(__file__).parent / dName).iterdir()] #list of file path in dat_full

#['0610_0759, '.._0959', '.._1159', '.._1359', '.._1559']
timeI =  9918 + 12*np.arange(5)
# print (timeI)

for i in timeI[0:1]:

	xlines, ylines = [], [] # print (file[20:-20])
	
	with open(filesInPath[i], 'r') as f:
		print (filesInPath[i])
		for str_line in list(f)[:-1]: #only care from 280 to 399
			if str_line.strip(): # only pass if line is not blank
				list_line = str_line.split() # make sample list, strip '\n' in trialling
				xlines.append(float(list_line[0])) # x is our uv lamda 
				ylines.append(float(list_line[1])) # y is its Irradiance,
                                                   # I suspect that data is in unit milli-W/m^2 
		print (xlines)
		print (ylines)

		plt.plot(xlines, ylines)
		plt.show()
# for ik in filesInPath:


