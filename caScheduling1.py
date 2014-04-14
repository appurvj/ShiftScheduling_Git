#!/usr/local/bin/python
import pymprog as math
import pprint

dispGASlots = False
dispGASlotCount = False
dispOffSch = False

## Problem Config  ##
gaList = ['Appurv', 'Ashley', 'Bianca', 'Kristy', 'Rob', 'Jason',
'Davona', 'Rocky', 'Taylor', 'Praveen','Alex', 'Laurel', 'Harshita', 
'Thomas','Chris', 'Tyler', 'Angela']
reqSlotsPerGA = [18,9,9,9,9,9,9,9,9,9,9,9,4,4,4,4,4]
officeList = ['RiverKnoll', 'Colony']
daysList = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
slotsList = ['9am - 10am', '10am - 11am', '11am - 12pm', '12pm - 1pm', '1pm - 2pm', '2pm - 3pm', '3pm - 4pm', '4pm - 5pm']



##  Mathematical Model  ##
p = math.model('Shift Assignment') # Starting the model
#math.verbose(True)


##  Sets  ##
GAs = range(len(gaList)) # Set of student staff
SLOTS = range(len(slotsList)) # Set of shift slots per day (1/2 hour each)
OFFICES = range(len(officeList)) # Set of offices
DAYS = range(len(daysList)) # Set of days when office is open


##  Params  ##
alpha = [[[1 for k in DAYS] for j in SLOTS] for i in GAs]
kappa = [0 for k in GAs]
maxSlots = 5  # Max consecutive slots allowed in an assignment
minSlots = 2  # Min consecutive slots required in an assignment


## Variables  ##
x = p.var(math.iprod(GAs,SLOTS,OFFICES,DAYS), 'X',bool)

##  Objective Function  ##
p.max(sum(x[(g,s,o,d)] for g in GAs for s in SLOTS for o in OFFICES for d in DAYS))


##  Constraints  ##
p.st( # For a given slot, GA must be available and can only be in one office
[sum(x[(g,s,o,d)] for o in OFFICES) <= alpha[g][s][d] for g in GAs for s in SLOTS for d in DAYS],
'singleAssignment')

p.st( # Each GA should be allotted the total slots required to be allotted
[sum(x[(g,s,o,d)] for s in SLOTS for o in OFFICES for d in DAYS) == reqSlotsPerGA[g] for g in GAs],
'HoursRequirements')

p.st( # Every office should be covered by at least two GAs for every slot
[sum(x[(g,s,o,d)] for g in GAs) >= 1 for s in SLOTS for o in OFFICES for d in DAYS],
'CoverOffice')

p.solve(float)
print "\nSIMPLEX DONE:", p.status()
p.solve(int)
print '\nOptimal Soln:', p.vobj()
if dispGASlots or dispGASlotCount:
	print ' \n\nDisplaying GA slot assignment/count..'
	for g in GAs:
		count = 0 
		if dispGASlots:
			print ' '
			print gaList[g] ,':'
		for d in DAYS:
			for (s,o) in math.iprod(SLOTS, OFFICES):
				if x[g,s,o,d].primal >= 1 :
					count += 1
					if dispGASlots:
						print daysList[d], slotsList[s], officeList[o]
		if dispGASlotCount:
			print gaList[g] ,':', count, 'slots'

if dispOffSch:
	print ' \n\nChecking slot fulillment..'
	for o in OFFICES:
		print '\n', officeList[o]
		for s in SLOTS:
			printList = [slotsList[s],'  ']
			for d in DAYS:
				subList = [daysList[d]]
				for g in GAs:
					if x[g,s,o,d].primal >= 1: subList.append(gaList[g])
				subList.append('  ')
				printList.append(subList)
			print printList



