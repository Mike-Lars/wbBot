import sqlite3

# Establish db connection and make cursor
conn = sqlite3.connect('wbBot.sqlite')
cur = conn.cursor()

# Define function for program quit and exit message
def exit():
	print('\n~ Happy landings ~\n')
	quit()

# Define function to handle invalid input
def invalid():
	print('Invalid entry')

print("\n~ WB Bot at your service. Type 'done' at any time to finish ~\n")

# Print out a list of available aircraft in db
cur.execute('''SELECT tail_number FROM Aircraft ORDER BY tail_number ASC''')
aircraftList = cur.fetchall()
if len(aircraftList) < 1:
	print('No aircraft in database')
for plane in aircraftList:
	print('>', plane[0])
print()

# Ask user for aircraft choice
while True:
	aircraft = input('Aircraft tail number: ')
	if aircraft == 'done':
		exit()
	aircraft = aircraft.upper()
	try:
		# Grab aircraft's empty weight, empty arm, empty moment from db
		cur.execute('''SELECT empty_weight FROM Aircraft WHERE tail_number=?''', (aircraft,))
		emptyWeight = cur.fetchone()[0]
		cur.execute('''SELECT empty_arm FROM Aircraft WHERE tail_number=?''', (aircraft,))
		arm = cur.fetchone()[0]
		cur.execute('''SELECT empty_moment FROM Aircraft WHERE tail_number=?''', (aircraft,))
		moment = cur.fetchone()[0]

		# Grab aircraft arms for frontpax, rearpax, fuel, baggage from db
		cur.execute('''SELECT frontpax_arm FROM Aircraft WHERE tail_number=?''', (aircraft,))
		frontpax_arm = cur.fetchone()[0]
		cur.execute('''SELECT rearpax_arm FROM Aircraft WHERE tail_number=?''', (aircraft,))
		rearpax_arm = cur.fetchone()[0]
		cur.execute('''SELECT fuel_arm FROM Aircraft WHERE tail_number=?''', (aircraft,))
		fuel_arm = cur.fetchone()[0]
		cur.execute('''SELECT baggage_arm FROM Aircraft WHERE tail_number=?''', (aircraft,))
		baggage_arm = cur.fetchone()[0]

		# Grab aircraft type and location from db
		cur.execute('''SELECT Type.name FROM Type JOIN Aircraft ON Type.id=Aircraft.type_id WHERE Aircraft.tail_number=?''', (aircraft,))
		type = cur.fetchone()[0]
		cur.execute('''SELECT Location.name FROM Location JOIN Aircraft on Location.id=Aircraft.location_id WHERE Aircraft.tail_number=?''', (aircraft,))
		location = cur.fetchone()[0]
		break
	except:
		print('Aircraft not found in database')

# Ask user for FRONT PAX weight
while True:
	frontPaxWeight = input('FRONT PAX weight: ')
	if frontPaxWeight == 'done':
		exit()
	try:
		frontPaxWeight = int(frontPaxWeight)
		break
	except:
		invalid()

# Ask user for REAR PAX weight
while True:
	rearPaxWeight = input('REAR PAX weight: ')
	if rearPaxWeight == 'done':
		exit()
	try:
		rearPaxWeight = int(rearPaxWeight)
		break
	except:
		invalid()

# Ask user for FUEL in gallons
while True:
	fuelWeight = input('FUEL in gallons: ')
	if fuelWeight == 'done':
		exit()
	try:
		fuelWeight = int(fuelWeight) * 6
		break
	except:
		invalid()

# Ask user for BAGGAGE weight
while True:
	baggageWeight = input('BAGGAGE weight: ')
	if baggageWeight == 'done':
		exit()
	try:
		baggageWeight = int(baggageWeight)
		break
	except:
		invalid()

# Ask user for FUEL BURN in gallons
while True:
	burnWeight = input('FUEL BURN in gallons: ')
	if burnWeight == 'done':
		exit()
	try:
		burnWeight = int(burnWeight) * 6
		break
	except:
		invalid()

zero_weight = emptyWeight + frontPaxWeight + rearPaxWeight + baggageWeight
zero_moment = moment + (frontPaxWeight * frontpax_arm) + (rearPaxWeight * rearpax_arm) + (baggageWeight * baggage_arm)
zero_cg = round(zero_moment / zero_weight, 2)

takeoff_weight = round(zero_weight + fuelWeight, 2)
takeoff_moment = round(zero_moment + (fuelWeight * fuel_arm), 2)
takeoff_cg = round(takeoff_moment / takeoff_weight, 2)

landing_weight = round(takeoff_weight - burnWeight, 2)
landing_moment = round(takeoff_moment - (burnWeight * fuel_arm), 2)
landing_cg = round(landing_moment / landing_weight, 2)

print('\n\n~ Weight and Balance Calculations for ' + aircraft + ', ' + type + ' based in ' + location + ' ~')

print()
print('Zero fuel weight:', zero_weight)
print('Zero fuel CG:', zero_cg)
print('Zero fuel moment:', zero_moment)
print()

print('Takeoff weight:', takeoff_weight)
print('Takeoff CG:', takeoff_cg)
print('Takeoff moment:', takeoff_moment)
print()

print('Landing weight:', landing_weight)
print('Landing CG:', landing_cg)
print('Landing moment:', landing_moment)
print()

print('~ Happy landings ~\n')
