#Writer: Suppachai Laobundit 
from block import genMdBlock, genColBlock, genTimeBlock, genMdTimeBlock 
from convertUnit import deFrontZero, MdToDay, timeToMins, effTilT
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def Antipsor(lamda):  #Antipsoriasis

    if lamda < 296.0:
        return 0.6504*10**(-0.6304*(296.-lamda))
    
    elif lamda < 300.0:
        return 1.0000*10**(-0.0467*(300.-lamda))
    
    elif lamda < 304.0:
        return 1.0000*10**(-0.1067*(lamda-300.))
    
    elif lamda < 313.0:
        return 0.3743*10**(-0.1571*(lamda-304.))
    
    elif lamda < 330.0:
        return 0.0144*10**(0.08233*(313.-lamda))
    
    elif lamda < 400.0: #Note it does not go beyond 400
        return 0.00057*10**(0.00937*(330.-lamda))

def insideInteg(list_file):
    
    #input list of lines from our txt file
    #output float Ambient Antipsoriatic Irradiance [ Wm-2]

    xlines, ylines = [], [] # print (file[20:-20])
    for str_line in list_file[:-1]: #only care from 280 to 399
        if str_line.strip(): # only pass if line is not blank
            list_line = str_line.split() # make sample list, strip '\n' in trialling
            xlines.append(float(list_line[0])) # x is our uv lamda 
            ylines.append(float(list_line[1])/1000) # y is its Irradiance,
                                                   # I suspect that data is in unit milli-W/m^2 
    antipsor_array = []
    for ele in xlines:
        antipsor_array.append(Antipsor(ele)) #antipsor lists
    
    antipsor_array = np.array(antipsor_array)
    xlines, ylines = np.array(xlines), np.array(ylines)
    product_array = ylines*antipsor_array #d1 irradiance * antipsor
    
    area_sum = np.sum(product_array) - 0.5*(product_array[0] + product_array[-1])
#     plt.plot(xlines, product_array) #If I want to plot

    return area_sum 


def AAIARawF(dName='dat_full', br='raw'):

	#Variables
	filesInPath = [child for child in (Path(__file__).parent / dName).iterdir()] #list very important file path in dat_full 
	md_tms = genMdTimeBlock()[245:-147] #this is what we want limit by boundary 0206_0559, 1228_1759
	
	a = np.empty(len(md_tms))
	a.fill(np.nan)
	AAIA = pd.DataFrame(a, index=md_tms,columns=['firstResult'])
	
	#chack
	(Path(__file__).parent/'result'/'AAI'/br).mkdir(parents=True, exist_ok=True) #create directory if not exist yet
	if not (Path(__file__).parent/'result'/'AAI'/'allAAIPan.html').exists():
		print ('We have made this')
		return False

	count = 0 #for index dataFolder

	for md_tm in AAIA.index: #loop around index

		print ('moty', md_tm)  #for tracking and debug

		pas = True

		while pas:

			print ('coby', filesInPath[count].name) #for tracking and debug

			
			if MdToDay(filesInPath[count].name[4:8]) > MdToDay(md_tm[:4]):
	 
				AAIA.loc[md_tm] = np.nan #float
				pas = False
				continue


			elif MdToDay(filesInPath[count].name[4:8]) == MdToDay(md_tm[:4]):

				if timeToMins(filesInPath[count].name[9:13]) > timeToMins(md_tm[5:9]):

					AAIA.loc[md_tm] = np.nan #float
					pas = False

				elif timeToMins(filesInPath[count].name[9:13]) == timeToMins(md_tm[5:9]):
						
					with open(filesInPath[count], 'r') as f:
						AAIA.loc[md_tm] = np.around(insideInteg(list(f)), decimals=3)
						
					pas = False
					print (filesInPath[count].name)
					count += 1

				else:
					count +=1

				continue


			else:
				count += 1

	if not (Path(__file__).parent/'result'/'AAI'/br/'allAAIA.html').exists():
		AAIA.to_html(Path(__file__).parent/'result'/'AAI'/br/'allAAIA.html') #export all df to html

	if not (Path(__file__).parent / 'result'/'AAI'/br/'AAIA.h5').exists():
		AAIA.to_hdf(Path(__file__).parent / 'result'/'AAI'/br/'AAIA.h5', key='AAIA', mode='w')


def AAIBRawF(hdf='AAIA.h5', br='raw'):

	#input AAItxt
	#output 2d AAI Pandas 

	#variables-1
	mds = genMdBlock()[5:-3] #0226 - 1228
	col_labs = genTimeBlock() #0859 - 1659
	ncol = len(col_labs) #len
	dot = 0 #for multiply

	#variable-2 (Important NOTE below)
	#AAIA is only one column df
	#AAIB is multiple column df 

	AAIA = pd.read_hdf(Path(__file__).parent / 'result'/'AAI'/br/hdf)

	a = np.empty(shape =(len(mds), len(col_labs))) #create empty 2d array
	a.fill(np.nan) #fill all ele to nan
	AAIB = pd.DataFrame(a, index =mds, columns=col_labs) #create df from nan array

	#loop
	for ind in AAIB.index: 

		AAIB.loc[ind, :] = AAIA.iloc[dot*ncol: (dot+1)*ncol, 0].values #assign slice of AAIA with same day to row ele of AAIB 

		if dot % 100 == 0: # check
			print (AAIA.iloc[dot*ncol],  AAIA.iloc[(dot+1)*ncol])
		dot += 1 #increment 

	(Path(__file__).parent/'result'/'AAI'/br/'html').mkdir(parents=True, exist_ok=True)
	(Path(__file__).parent/'result'/'AAI'/br/'excel').mkdir(parents=True, exist_ok=True)


	if not (Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5').exists():
		AAI.to_hdf(Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5', key='AAIB', mode='w')

	if not (Path(__file__).parent/'result'/'AAI'/br/'html'/'allAAIB.html').exists():
		AAI.to_html(Path(__file__).parent/'result'/'AAI'/br/'html'/'allAAIB.html') #export all df to html

	if not (Path(__file__).parent/'result'/'AAI'/'excel'/br/'allAAIB.xlsx').exists():
			AAIB.to_excel(Path(__file__).parent/'result'/'AAI'/br/'excel'/'allAAIB.xlsx')

	lasts = ['0228', '0331','0430', '0531', '0630', '0731' ,
			'0831', '0930', '1031', '1130', '1228']

	#Save each month 
	for md in lasts: #loop

		if md == '0228': a = '0206'
		else: a = md[:2] + '01' 	#0m01
	
		name = md[:2] + 'AAIB.html' 	#name for files
		if not (Path(__file__).parent/'result'/'AAI'/br/'html'/name).exists(): #check if destinatation has been not created		
			AAIB.loc[a:md].to_html(Path(__file__).parent/'result'/'AAI'/br/'html'/name)

		nameB = md[:2] + 'AAIB.xlsx'
		if not (Path(__file__).parent/'result'/'AAI'/'noSmooth'/'excel'/nameB).exists():
			AAIB.loc[a:md].to_excel(Path(__file__).parent/'result'/'AAI'/br/'excel'/nameB)



def AAIBClean(br='clean'):

	#variables
	AAIB = pd.read_hdf(Path(__file__).parent / 'result'/'AAI'/'raw'/'AAIB.h5') #read from raw

	for ico in range(0, len(AAIB.columns)): #loop column length

		#variables
		print ('co')
		nanIndx = (np.argwhere(np.isnan(AAIB.iloc[:, ico].values)).flatten()) #array of nan indx in column

		for inan in nanIndx: #index of our Nan in coloum ico\
			#initialize values	
			print ('nono')
			p, q = 0, 0 
			pL, qL = [], [] 
			pas = True 
			c, d = 1, 1

			while pas:

				if p != 3: #if p less than 3, when p == 3, it will not execute
					if np.isnan(AAIB.iloc[inan-c, ico]) == False: #if before is not nan
						pL.append(AAIB.iloc[inan-c, ico])
						p += 1
					c += 1 

				if q != 3:
					if np.isnan(AAIB.iloc[inan+d, ico]) == False: #if after is not nan
						qL.append(AAIB.iloc[inan+d, ico])
						# print (AAIB.iloc[inan+d, ico])
						q += 1
					d += 1

				elif p == 3 and q == 3:
					pas = False

			AAIB.iloc[inan, ico] = np.round(np.mean(pL+qL), decimals=3)
			
	(Path(__file__).parent/'result'/'AAI'/br/'html').mkdir(parents=True, exist_ok=True)
	(Path(__file__).parent/'result'/'AAI'/br/'excel').mkdir(parents=True, exist_ok=True)


	if not (Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5').exists(): #if not exist
		AAIB.to_hdf(Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5', key='AAIB', mode='w')

	if not (Path(__file__).parent/'result'/'AAI'/br/'html'/'allAAIB.html').exists():
		AAIB.to_html(Path(__file__).parent/'result'/'AAI'/br/'html'/'allAAIB.html') #export all df to html

	if not (Path(__file__).parent/'result'/'AAI'/'excel'/br/'allAAIB.xlsx').exists():
		AAIB.to_excel(Path(__file__).parent/'result'/'AAI'/br/'excel'/'allAAIB.xlsx')

	lasts = ['0228', '0331','0430', '0531', '0630', '0731' ,
			'0831', '0930', '1031', '1130', '1228']

	#Save each month 
	print ('Done')


def AAIBSmooth(br='smooth'):
	#function for smooting clean data
	mds = genMdBlock()[5:-3] #0226 - 1228
	col_labs = genTimeBlock() #0859 - 1659
	a = np.empty(shape =(len(mds), len(col_labs))) #create empty 2d array
	

	

	AAIBs = pd.DataFrame(a, index=mds, columns=col_labs)
	ndex = len(aaibc.index)
	
	for icol in range(0, len(aaibc.columns)):

		print ('cp')
		for indx in range(0, 3): #0, 1, 2

			AAIBs.iloc[indx, icol] = np.round(np.mean(aaibc.iloc[indx:indx+4,icol].values), decimals=3)

		for indx in range(ndex-3, ndex):
			AAIBs.iloc[indx, icol] =  np.round(np.mean(aaibc.iloc[indx-3:ndex,icol].values), decimals=3)

		for indx in range(3, ndex-3):

			AAIBs.iloc[indx, icol] = np.round(np.mean(aaibc.iloc[indx-3:indx+4, icol].values), decimals=3)


	(Path(__file__).parent/'result'/'AAI'/br/'html').mkdir(parents=True, exist_ok=True)
	(Path(__file__).parent/'result'/'AAI'/br/'excel').mkdir(parents=True, exist_ok=True)

	if not (Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5').exists(): #if not exist
		AAIBs.to_hdf(Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5', key='AAIB', mode='w')

	if not (Path(__file__).parent/'result'/'AAI'/br/'html'/'allAAIB.html').exists():
		AAIBs.to_html(Path(__file__).parent/'result'/'AAI'/br/'html'/'allAAIB.html') #export all df to html

	if not (Path(__file__).parent/'result'/'AAI'/'excel'/br/'allAAIB.xlsx').exists():
		AAIBs.to_excel(Path(__file__).parent/'result'/'AAI'/br/'excel'/'allAAIB.xlsx')

	print ('Done')

def AAIBtilT(br='tilt'):

	AAIB = pd.read_hdf(Path(__file__).parent / 'result'/'AAI'/'smooth'/'AAIB.h5') #pd.Df smooth data

	(Path(__file__).parent/'result'/'AAI'/br).mkdir(parents=True, exist_ok=True) #create directory 

	cols = AAIB.columns #pd

	ncol = len(cols) # int

	for icol in range(0, ncol): 

		AAIB.iloc[:, icol] = np.round(AAIB.iloc[:, icol] *(effTilT(cols[icol])), decimals=3) #

	if not (Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5').exists(): #if not exist
		AAIB.to_hdf(Path(__file__).parent / 'result'/'AAI'/br/'AAIB.h5', key='AAIB', mode='w')

	if not (Path(__file__).parent/'result'/'AAI'/br/'allAAIB.html').exists():
		AAIB.to_html(Path(__file__).parent/'result'/'AAI'/br/'allAAIB.html') #export all df to html

	print ('Done')




def AAIBplotDayF(br):
	#Should change this to have input
	#variable
	mwd = ['Feb', 'March', 'Apirl', 'May', 'June', 'July', 
			'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	mns = [ '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'] #list of string
	dns = [ '07', '14', '21', '28' ] #list of days

	#data 
	AAIB = pd.read_hdf(Path(__file__).parent / 'result'/ 'AAI'/br/'AAIB.h5') #read from br
	#directory checked / created
	(Path(__file__).parent/'result'/'AAI'/br/'graph').mkdir(parents=True, exist_ok=True)

	#loop, plot
	for i in range(len(mns)):
		(Path(__file__).parent/'result'/'AAI'/br/'graph'/mwd[i]).mkdir(parents=True, exist_ok=True)

		for di in dns:
			

			tg = mns[i] +di #target for df.loc
			print (tg)
			fname = 'AAI of ' + mwd[i] +' '+ di +'06.jpg'

			ylines = AAIB.loc[tg].values
			xlines = np.linspace(9, 17, len(ylines))

			plt.plot(xlines, ylines, label=tg)
			plt.axhline(0.0624, label='threshold AAI = 0.0624 Wm-2',linestyle='--', color='r')
		 	
			plt.title('AAI of ' + mwd[i] +' '+ di +' 06')
			plt.xlabel('Time [Hour]'); plt.ylabel('Ambient Antipsoriatic Irradiance [ Wm-2]')

			plt.legend(bbox_to_anchor=(0.625, .7, 1., .102), loc=3, fontsize='small')

			if not (Path(__file__).parent/'result'/'AAI'/br/'graph'/mwd[i]/fname).exists():
				plt.savefig(Path(__file__).parent / 'result'/ 'AAI' /br/'graph'/mwd[i]/fname )

			plt.clf()


def AAIBplotTime(br):

	#data 
	AAIB = pd.read_hdf(Path(__file__).parent / 'result'/ 'AAI'/br/'AAIB.h5') #read from br

	#variables
	sample = ['0959']
	time=['0959', '1159', '1359', '1559']
	xlines = np.arange(MdToDay('0206')+31, MdToDay('1228')+31)

	#intialize
	(Path(__file__).parent/'result'/'AAI'/br/'graph'/'time').mkdir(parents=True, exist_ok=True)

	for each in time:

		print (each)
		fname = 'AAI of ' + each +'.jpg'
		aaiT = AAIB.loc[:, each].values #np array
		plt.plot(xlines, aaiT)

		plt.title('AAI during '+ each)
		plt.xlabel('Date [Day]'); plt.ylabel('Ambient Antipsoriatic Irradiance [ Wm-2]')

		if not (Path(__file__).parent/'result'/'AAI'/br/'graph'/'time'/fname).exists():
			plt.savefig(Path(__file__).parent / 'result'/ 'AAI' /br/'graph'/'time'/fname)

		plt.clf()

	print ('done')












# AAIARawF()
# AAIBRawF()
# AAIBClean()
# AAIBplotDayF('tilt')
# AAIBSmooth()
# AAIBplotTime('tilt')
# AAIBtilT()


# aaia = pd.read_hdf(Path(__file__).parent / 'result'/'AAI'/'noSmooth'/'AAIA.h5')
