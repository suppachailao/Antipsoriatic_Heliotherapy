import pandas as pd
import numpy as np
from block import genMdBlock, genColBlock, genTimeBlock, genMdTimeBlock 
from convertUnit import MdToDay
from pathlib import Path
from matplotlib import pyplot as plt


def doesF(br, inputName='AAIB.h5'):

	#Explaination
	
	#variable 1
	md_tms = genMdBlock()[5:-3] #list str ['0206', '0207', ..., 1228] index row for df
	col_labs = genColBlock() #list str ['0600-0630', '0630-0700', ... ] column labels for df
	T = 600 #int Time 

	#Initialize
	a = np.empty(shape =(len(md_tms), len(col_labs))) #create empty 2d array
	does = pd.DataFrame(a, index =md_tms, columns=col_labs) #create df from nan array
	aaiB = pd.read_hdf(Path(__file__).parent / 'result'/'AAI'/br/inputName) #pd.df AAIB
	

	# Loop
	for ix in range(0, len(does.index)):
		#initialize
		stt = 0 #int 
		end = 4 #int we can change this 

		for ic in range(0, len(does.columns)):

			try:

				L = aaiB.iloc[ix, stt:end].values #np array 
				does.iloc[ix, ic] = np.round(0.5 *T *(L[0] +2*L[1] +2*L[2] +L[3]) / 317.9, decimals=2)

			except IndexError:
				print (False)
				print (ix, ic)

			finally:
				stt += 3
				end += 3

	
	#SAVE

	(Path(__file__).parent/'result'/'does'/br).mkdir(parents=True, exist_ok=True)

	if not (Path(__file__).parent / 'result'/'does'/br/'does.h5').exists(): #if not exist
		does.to_hdf(Path(__file__).parent / 'result'/'does'/br/'does.h5', key='does', mode='w')


	(Path(__file__).parent/'result'/'does'/br/'html').mkdir(parents=True, exist_ok=True)
	(Path(__file__).parent/'result'/'does'/br/'excel').mkdir(parents=True, exist_ok=True)

	if not (Path(__file__).parent/'result'/'does'/br/'html'/'allDoes.html').exists():
		does.to_html(Path(__file__).parent/'result'/'does'/br/'html'/'allDoes.html') #export all df to html

	#variable
	lasts = ['0228', '0331','0430', '0531', '0630', '0731',
			'0831', '0930', '1031', '1130', '1229']

	for md in lasts: #loop

		#Initialize "a"
		if md == '0228': a = '0206'
		else: a = md[:2] + '01' 	
	
		name = md[:2] + 'R.html' 	#name for files
		if not (Path(__file__).parent/'result'/'does'/br/'html'/name).exists(): #check if destinatation has been not created		
			does.loc[a:md].to_html(Path(__file__).parent/'result'/'does'/br/'html'/name)

		nameB = md[:2] + 'R.xlsx'
		if not (Path(__file__).parent/'result'/'does'/br/'excel'/nameB).exists():
			does.loc[a:md].to_excel(Path(__file__).parent/'result'/'does'/br/'excel'/nameB)

def doesplotF(br):

	#variable
	mwd = ['Feb', 'March', 'Apirl', 'May', 'June', 'July', 
			'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	mns = [ '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] #list of string
	dns = [ '06', '16', '26' ] #list of days

	#data 
	does = pd.read_hdf(Path(__file__).parent / 'result'/ 'does' /br/'does.h5')
	#directory checked / created
	(Path(__file__).parent/'result'/'does'/br/'graph').mkdir(parents=True, exist_ok=True)

	#loop, plot
	for i in range(len(mns)):

		(Path(__file__).parent/'result'/'does'/br/'graph'/mwd[i]).mkdir(parents=True, exist_ok=True)

		for di in dns:
			

			tg = mns[i] +di #target for df.loc
			print (tg)
			fname = 'Does of ' + mwd[i] +' '+ di +'06.jpg'
			width = 0.45
			ylines = does.loc[tg].values
			xlines = np.linspace(9., 17., len(ylines), endpoint=False)
			# if i == 7:
			# 	print (ylines)

			plt.bar(xlines, ylines, width=width,align='edge')
		 	
			plt.title('Does of ' + mwd[i] +' '+ di +' 06')
			plt.xlabel('Time[Hour]'); plt.ylabel('Does [SAPD]')
			plt.axhline(1.0, label='1 SAPD',linestyle='--', color='r')
			plt.axhline(2.0, label='2 SAPD', linestyle='--',color='green')
			plt.legend()

			if not (Path(__file__).parent/'result'/'does'/br/'graph'/mwd[i]/fname).exists():
				plt.savefig(Path(__file__).parent / 'result'/ 'does'/br /'graph'/mwd[i]/fname )

			plt.clf()

def doesplotTime(br):

	#data 
	does = pd.read_hdf(Path(__file__).parent / 'result'/ 'does'/br/'does.h5') #read from br

	#variables
	time=['1030-1100', '1200-1230', '1500-1530']
	xlines = np.arange(MdToDay('0206')+31, MdToDay('1228')+31)

	#intialize
	(Path(__file__).parent/'result'/'does'/br/'graph'/'time').mkdir(parents=True, exist_ok=True)

	for each in time:

		print (each)
		fname = 'Does of ' + each +'.jpg'
		doesT = does.loc[:, each].values #np array
		plt.plot(xlines, doesT)

		plt.title('Does during '+ each)
		plt.xlabel('Date [Day]'); plt.ylabel(' Does[SAPD]')
		plt.axhline(1.0, label='1 SAPD',linestyle='--', color='r')
		plt.axhline(2.0, label='2 SAPD', linestyle='--',color='green')
		plt.legend()

		if not (Path(__file__).parent/'result'/'does'/br/'graph'/'time'/fname).exists():
			plt.savefig(Path(__file__).parent / 'result'/ 'does' /br/'graph'/'time'/fname)


		plt.clf()

	print ('done')


def 


# doesplotF('smooth')
# doesplotTime('smooth')


