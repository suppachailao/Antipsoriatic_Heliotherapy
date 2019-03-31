#Old coding
from block import genMdBlock, genColBlock, genTimeBlock, genMdTimeBlock 
from convertUnit import deFrontZero, MdToDay, timeToMins
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def AAIAtxtF(outputName='AAIA.txt',dName='dat_full'):

	# Objective is to calculate AAI at times specified
	# input name of dataFolder in my case its location is in the same cwd
	# output open and write first integration to txt file 
	# Only choose the block, if it doesn't exist, Antipsor=nan 
	# if error is index out of range in dataFolder, still we accomplish the result

	#Variables
	filesInPath = [child for child in (Path(__file__).parent / dName).iterdir()] #child is path object

	#chack
	(Path(__file__).parent/'result'/'AAI').mkdir(parents=True, exist_ok=True) #create directory if not exist yet
	outputTxt = Path(__file__).parent / 'result'/'AAI'/outputName #our path to txt

	if outputTxt.exists():
		print ('We aleardy created txt file')
		return False

	#variable
	md_tms = genMdTimeBlock()[245:-147] #this is what we want limit by boundary 0206_0559, 1228_1759
	count = 0 #for index dataFolder

	#loop in md_tms # it just checking data and time before cal and write down ans
	for md_tm in md_tms:

		print ('moty', md_tm)  #for tracking and debug

		pas = True

		while pas:

			print ('coby', filesInPath[count].name) #for tracking and debug

			with open(outputTxt, 'a') as tfile: #open and write a txt file

					if MdToDay(filesInPath[count].name[4:8]) > MdToDay(md_tm[:4]):
	
						tfile.write("{},{}\n".format(md_tm, np.nan)) #write nan 
						pas = False
						continue


					elif MdToDay(filesInPath[count].name[4:8]) == MdToDay(md_tm[:4]):

						if timeToMins(filesInPath[count].name[9:13]) > timeToMins(md_tm[5:9]):
							tfile.write("{},{}\n".format(md_tm, np.nan))
							pas = False

						elif timeToMins(filesInPath[count].name[9:13]) == timeToMins(md_tm[5:9]):
							with open(filesInPath[count], 'r') as f:
								tfile.write("{},{:4f}\n".format(md_tm, insideInteg(list(f))))
							pas = False
							print (filesInPath[count].name)
							count += 1

						else:
							count +=1

						continue


					else:
						count += 1
	#
	return 'True'

def staDoes(br):

	#Find the mean, std, etc of does for our interval, 30 mins, 

	#Initialize
	does = pd.read_hdf(Path(__file__).parent / 'result'/ 'does'/br/'does.h5') #read from br
	myIndexs = pd.MultiIndex(levels=[[]]*2, labels=[[]]*2, names=['Month', 'Statistics']) #create mutiIndex

	#variables
	month = ['Feb', 'March', 'Apirl', 'May', 'June', 'July', 
			'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] #1-index name
	stats = ['Mean', 'Std'] #2-index name
	endMon = ['0228', '0331','0430', '0531', '0630', '0731',
			'0831', '0930', '1031', '1130', '1229'] #for calling does

	statDoes = pd.DataFrame(index=myIndexs, columns=does.columns) #create empty pandas 

	#for loop assign
	for im in range(0, len(month)): #int itera

		if im == 0:   iniMon = '0201' #string index
		else:         iniMon = endMon[im][:2] + '01' #string index

		print (iniMon, endMon[im]) #check index

		statDoes.loc[(month[im], stats[0]), :] = does.loc[iniMon :endMon[im], :].mean(axis=0).round(3) #mean-assign
		statDoes.loc[(month[im], stats[1]), :] = does.loc[iniMon :endMon[im], :].std(axis=0).round(3) #std-assign

	#create a file
	if not (Path(__file__).parent/'result'/'does'/br/'statDoes.p').exists():
	 	statDoes.to_pickle(Path(__file__).parent/'result'/'does'/br/'statDoes.p') #to_hdf reported warning, so I use pickle instead
	
	if not (Path(__file__).parent/'result'/'does'/br/'html'/'statDoes.html').exists():
	 	statDoes.to_html(Path(__file__).parent/'result'/'does'/br/'html'/'statDoes.html') #export all df to html

summer4_91 = does.loc['0401':'0731', '0900-0930':'0930-1000']
summer4_101 = does.loc['0401':'0731', '1000-1030':'1030-1100']
summer4_111 =  does.loc['0401':'0731', '1100-1130':'1130-1200']
summer4_121 = does.loc['0401':'0731', '1200-1230':'1230-1300']
summer4_131 = does.loc['0401':'0731', '1300-1330':'1330-1400']
summer4_141 = does.loc['0401':'0731', '1400-1430':'1430-1500']