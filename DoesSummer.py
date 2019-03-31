from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import shutil
from block import genColBlock
from convertUnit import MdToDay

#Main Goal: Output 2 x-axis graph specifically



#Variables
br = 'smooth'
does = pd.read_hdf(Path.cwd() / 'result'/ 'does' /br/'does.h5')
itime = {'9':'0900-0930', '93':'0930-1000', '10':'1000-1030', '103':'1030-1100'}

#Summer season (9.00-10.00)
summer3_91 = does.loc['0301':'0731', '0900-0930':'0930-1000'] 
summer3_101 = does.loc['0301':'0731', '1000-1030':'1030-1100']
summer3_111 = does.loc['0301':'0731', '1100-1130':'1130-1200']
summer3_121 = does.loc['0301':'0731', '1200-1230':'1230-1300']
summer3_131 = does.loc['0301':'0731', '1300-1330':'1330-1400']
summer3_141 = does.loc['0301':'0731', '1400-1430':'1430-1500']
summer8_91 = does.loc['0801':'1031', '0900-0930':'0930-1000']
summer8_101 = does.loc['0801':'1031', '1000-1030':'1030-1100']
summer8_111 = does.loc['0801':'1031', '1100-1130':'1130-1200']
summer8_121 = does.loc['0801':'1031', '1200-1230':'1230-1300']
summer8_131 = does.loc['0801':'1031', '1300-1330':'1330-1400']
summer8_141 = does.loc['0801':'1031', '1400-1430':'1430-1500']
summer11_91 = pd.concat([does.loc['1101':'1228', '0900-0930':'0930-1000'], does.loc['0206':'0228', '0900-0930':'0930-1000']])
summer11_101 = pd.concat([does.loc['1101':'1228', '1000-1030':'1030-1100'], does.loc['0206':'0228', '1000-1030':'1030-1100']])
summer11_111 = pd.concat([does.loc['1101':'1228', '1100-1130':'1130-1200'], does.loc['0206':'0228', '1100-1130':'1130-1200']])
summer11_121 = pd.concat([does.loc['1101':'1228', '1200-1230':'1230-1300'], does.loc['0206':'0228', '1200-1230':'1230-1300']])
summer11_131 = pd.concat([does.loc['1101':'1228', '1300-1330':'1330-1400'], does.loc['0206':'0228', '1300-1330':'1330-1400']])
summer11_141 = pd.concat([does.loc['1101':'1228', '1400-1430':'1430-1500'], does.loc['0206':'0228', '1400-1430':'1430-1500']])

# print (does.loc[['1101':'1228', '0206':'0228'], '1400-1430':'1430-1500'])
# print (summer)

#dict
dt3 = {'3-7n9-10':summer3_91, '3-7n10-11':summer3_101, '3-7n11-12':summer3_111, 
		'3-7n12-13':summer3_121, '3-7n13-14':summer3_131, '3-7n14-15':summer3_141}
dt8 = {'8-10n9-10':summer8_91,'8-10n10-11':summer8_101, '8-10n11-12':summer8_111, '8-10n12-13':summer8_121, '8-10n13-14':summer8_131, '8-10n14-15':summer8_141}
dt11 = {'11-2n9-10':summer11_91,'11-2n10-11':summer11_101,'11-2n11-12':summer11_111,'11-2n12-13':summer11_121, '11-2n13-14':summer11_131,'11-2n14-15':summer11_141 }
newtick3, newloc3 = [0, 31, 61, 92, 122], ['Mar01', 'Apr01', 'May01', 'June01', 'July01']
newtick4, newloc4 = [0, 30, 61, 91], ['Apr01', 'May01', 'June01', 'July01']
newtick8, newloc8 = [0, 31, 61], ['Aug01', 'Sep01', 'Oct01']
newtick11, newloc11 = [0, 30, 58], ['Nov01', 'Dec01', 'Feb01'] 

def plot2xaxis(dt, name, newtick, newloc):

	#Figure
	#name is folder name

	for key in dt.keys():

		
		fig = plt.figure()
		ax1 = fig.add_axes((0.1,0.3,0.8,0.6)) # create an Axes with some room below
		dt[key].loc[:, 'Total'] = dt[key].sum(axis=1) #row sum

		print (dt[key].iloc[[0, -1]]) #check
		print ('prob ', np.around(np.count_nonzero(dt[key].loc[:, 'Total'] > 2.0) /len(dt[key].index), decimals=2) ) #probability that does exceed 2.0
		prob = np.around(np.count_nonzero(dt[key].loc[:, 'Total'] > 2.0) /len(dt[key].index), decimals=2)

		X = np.arange(0., len(dt[key].index)) 
		Y = dt[key].loc[:, 'Total'].values #The Total Column

		ax1.plot(X,Y) 
		ax1.plot([], [], ' ', label='probability exceed 2 SAPD '+str(prob))

		nindex = key.find('n') #int 
		ax1.set_title('Does on Month '+key[:nindex] +' at time ' + key[nindex+1:])
		avgY = np.around(np.mean(Y), decimals=2) 

		ax1.axhline(avgY, label='average: '+str(avgY),linestyle='--', color='r')
		ax1.axhline(1.0, label='1 SAPD',linestyle='--', color='green')
		ax1.axhline(2.0, label='2 SAPD', linestyle='--',color='gold')
		ax1.legend(fontsize='small')

		# create second Axes. Note the 0.0 height

		ax2 = fig.add_axes((0.1,0.15,0.8,0.0))
		ax2.yaxis.set_visible(False) # hide the yaxis

		ax2.set_xlim(ax1.get_xlim())
		ax2.set_xticks(newtick)
		ax2.set_xticklabels(newloc)

		fname = name+ key+ '.jpg'
		if not (Path(__file__).parent/'result'/'does'/br/'graph'/'season'/name/fname).exists():
			fig.savefig(Path(__file__).parent / 'result'/ 'does'/br/'graph'/'season'/name/fname)
			print (fname)
				
		fig.clf()


plot2xaxis(dt11, 'winter', newtick11, newloc11)

#Next we want to find the probability of Does exceed 2SAPD during its season and different time








