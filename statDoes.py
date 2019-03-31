import pandas as pd
import numpy as np
from block import genMdBlock, genColBlock, genTimeBlock, genMdTimeBlock 
from convertUnit import MdToDay
from pathlib import Path
from matplotlib import pyplot as plt

def statDoes(br):

	# Find the mean, std, etc of does for our interval, 30 mins, 


	# variables
	month = ['February', 'March', 'April', 'May', 'June', 'July', 
			 'August', 'September', 'October', 'November', 'December'] #index name
	stats = ['Mean', 'Std'] 
	endMon = ['0228', '0331','0430', '0531', '0630', '0731',
			'0831', '0930', '1031', '1130', '1229'] #for calling does


	does = pd.read_hdf(Path(__file__).parent / 'result'/ 'does'/br/'does.h5') #read from br
	multiCol = pd.MultiIndex.from_product([does.columns, stats])#multi-columns with 
	statDoes = pd.DataFrame(index=month, columns=multiCol) #Empty data frame



	for im in range(0, len(month)): #int itera

		#det range
		if im == 0:   iniMon = '0206' #string index
		else:         iniMon = endMon[im][:2] + '01' #string index


		statDoes.iloc[im, ::2] = does.loc[iniMon :endMon[im], :].mean(axis=0).round(3).values
		statDoes.iloc[im, 1::2] = does.loc[iniMon :endMon[im], :].std(axis=0).round(3).values

		print (statDoes.iloc[im, 0:2]) #check


	
	if not (Path(__file__).parent/'result'/'does'/br/'statDoes.p').exists():
		statDoes.to_pickle(Path(__file__).parent/'result'/'does'/br/'statDoes.p')
	if not (Path(__file__).parent/'result'/'does'/br/'html'/'statDoes.html').exists():
	 	statDoes.to_html(Path(__file__).parent/'result'/'does'/br/'html'/'statDoes.html') #export all df to html
	if not (Path(__file__).parent/'result'/'does'/br/'excel'/'statDoes.xlsx').exists():
		statDoes.to_excel(Path(__file__).parent/'result'/'does'/br/'excel'/'statDoes.xlsx')


	print ('Done')

def staPlot(br):
	

	(Path(__file__).parent/'result'/'does'/br/'graph'/'stat').mkdir(parents=True, exist_ok=True)
	statDoes = pd.read_pickle(Path(__file__).parent/'result'/'does'/br/'statDoes.p') #upload

	#variables
	width = 0.5 #float
	colors = plt.cm.BuPu(np.linspace(0.2, 0.5, 3))  #np.array
	xlines = np.linspace(9., 17., len(statDoes.columns.levels[0])) #xvalues
	month = statDoes.index


	for im in range(0, len(month)):

		meanlines = statDoes.iloc[im, ::2].values
		stdlines =  statDoes.iloc[im, 1::2].values
		minus = meanlines-stdlines

	
		plt.bar(xlines, minus , width=width ,bottom=0, align='edge',color=colors[0], label='lower')
		plt.bar(xlines, stdlines,width=width,bottom=minus, align='edge',color=colors[1], label='mean')
		plt.bar(xlines, stdlines, width=width ,bottom=meanlines, align='edge',color=colors[2], label='upper')

		xloc, xlabel = [i for i in range(9, 18)], [str(i) for i in range(9, 18)]
		plt.title('Mean +- 1std for' + month[im]); plt.xticks(xloc, xlabel)
		plt.xlabel('Time [Hour]'); plt.ylabel('Does[SAPD]')
		plt.axhline(1.0, label='MAD[minimum] = 1.0',linestyle='--', color='r')
		plt.legend(bbox_to_anchor=(0.75, .7, 1., .102), loc=3, fontsize='small')

		fname = month[im] + '.jpg'
		if not (Path(__file__).parent/'result'/'does'/br/'graph'/'stat'/fname).exists():
			plt.savefig(Path(__file__).parent / 'result'/'does'/br /'graph'/'stat'/fname )
			print (fname)

		# plt.show()

# staPlot('smooth')
statDoes('smooth')