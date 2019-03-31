# Get Blocks of md, col, time, mdtime 

def genMdBlock(mdBlock = {"2":28, "3":31, "4":30, "5":31, "6":30,
		   "7":31, "8":31, "9":30, "10":31, "11":30, "12":31}):

	#input: dict-type {str:int,...,str:int}
	#output: list [mdday, mdday,....,mdday]

	dates = []

	for i in mdBlock.keys(): #month

		for j in range(1, mdBlock[i]+1): 

			if int(i) < 10 and j <10:
				dates.append("0"+ i +"0" +str(j))

			elif int(i) < 10 and j >= 10:
				dates.append("0"+ i +str(j))

			elif int(i) >=10 and j <10:
				dates.append(i +"0" +str(j))

			else:
				dates.append(i +str(j)) 

	return dates

def genColBlock(h1 = 9, h2 = 17, min1 = '00-', min2 = '30-'):

	#input: start-hour, end-hour, min1, min2
	#output: list 

	col_label = []

	for h in range(h1, h2):
		if h < 10: 
			col_label.extend(['0'+str(h)]* 2)
		else:
			col_label.extend([str(h) ]*2)

	diff = h2 - h1 

	for indx in range(0, diff*2, 2): #min1
		col_label[indx] += min1

	for indx in range(1, diff*2 +1, 2): #min2
		col_label[indx] += min2

	for i in range(0, len(col_label)-1): #copy and parse
		col_label[i] += col_label[i+1][:-1] 

	col_label[-1] += str(h2) + '00' #last

	return col_label

# print (genColBLock(hour))

def genTimeBlock(h1=9, h2=17, start="0859", mins=['09', '19', '29', '39', '49', '59']):

	#variable
	#mins is interval 

	timeBlock = [start] #first point from input

	for h in range(h1, h2):

		if h < 10: 
			timeBlock.extend(['0'+str(h)]* 6) #extend 

		else:
			timeBlock.extend([str(h)]*6)
		#finish hour block

	diff = h2 -h1

	for i in range(0, diff): #loop range(0, h2-h1)

		for j in range(1, len(mins)+1): #range(1, 7)

			timeBlock[i*6 +j] += mins[j-1] #add min one by one

	return timeBlock

def genMdTimeBlock():
	
	#output md_tms list, have check that length is good  
	

	md_tms = []  #res
	Md = genMdBlock()  #use
	Tm = genTimeBlock()  #use

	for md in Md:

		for tm in Tm:

			md_tms.append(md +'_' +tm) 

	return md_tms


# print (genMdBlock()[5:-3]) #Thanks
# print (genColBlock()[:])  #Thanks
# print (genTimeBlock()[:]) #Thanks
# print (genMdTimeBlock()[245:-147]) #limit by the boundary of dat_ful


