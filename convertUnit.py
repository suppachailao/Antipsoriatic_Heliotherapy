#Convert Unit Function
from numpy import pi, sin
def deFrontZero(sn):

	#string sn
	#output string with no front zero
	if sn[0] == "0":
		return sn[1]
	else:
		return sn

def MdToDay(md, mdBlock={"2":29, "3":31, "4":30, "5":31, "6":30,
		   "7":31, "8":31, "9":30, "10":31, "11":30, "12":31}):

	#input md format string "0201"
	#output dayi in 366

	summ = 0
	if md[:2] == "02": return int(deFrontZero(md[2:4]))
	
	else:
		summ = sum([mdBlock[str(key)] for key in range (2, int(deFrontZero(md[:2]))) ]) #sum days of all previous months
		summ += int(deFrontZero(md[2:4])) #add remaining day
		
	return summ

def timeToMins(stri):

	#change time string to int number
	summ = 0
	summ += int(deFrontZero(stri[:2])) *60
	summ += int(deFrontZero(stri[2:4]))

	return summ

def effTilT(tstr):

	#determine the angle of the sun from hour 
	#input: str time, 0909
	#output: float radiant, 0.23

	#Theory 
	#Sun set at 0600 with 0 rad 
	#Sun came down 1800 with pi rad
	#1 hour rand = pi / 12 rand
	#1 mins rand a= pi / 12*60 rand
	#Output: () * 1hr-rad
	#Tilt-Radiant = sin(angle)*Radiant

	#variable 
	stT = timeToMins('0600') #integer starting time mins
	tgT = timeToMins(tstr) #integer target time mins
	difT = tgT - stT #integer diff time mins
	angle = difT *(pi /(12 *60) ) #float angle radiant 
	eff = sin(angle) #float solar effective no unit

	return eff



# print (effTilT('0900'))
Item = []
init = 8
end = 7
# for each in range(8, 10):
# 	before = '0'+str(init) +'01'
# 	after = '0' + str(each)+'01'
# 	Item.append(MdToDay(after)-MdToDay(before))

# print (Item)

# Item.append(MdToDay('1201')-MdToDay('1101'))

# print (Item)

# Item.append(Item[-1] + (MdToDay('1228')-MdToDay('1201')))
# print (Item)

# Item.append(Item[-1] + (MdToDay('0228')-MdToDay('0206')))

# print (Item)

