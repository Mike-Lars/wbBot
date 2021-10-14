import sqlite3

# Establish db connection and make cursor
conn = sqlite3.connect('wbBot.sqlite')
cur = conn.cursor()

# Define function for program quit and exit message
def finished():
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
[print('>', plane[0]) for plane in aircraftList]
print()

# Ask user for aircraft choice
while True:
	aircraft = input('Aircraft tail number: ')
	if aircraft == 'done':
		finished()
	aircraft = aircraft.upper()
	try:
		# Grab aircraft's metadata from db
		cur.execute('''SELECT Aircraft.empty_weight, Aircraft.empty_arm, Aircraft.empty_moment, Aircraft.frontpax_arm, Aircraft.rearpax_arm, Aircraft.fuel_arm, Aircraft.baggage_arm, Type.name, Location.name FROM Aircraft JOIN Type JOIN Location ON Location.id=Aircraft.location_id AND Type.id=Aircraft.type_id WHERE tail_number=?''', (aircraft,))
		mdata = cur.fetchone()
		emptyWeight = mdata[0]
		emptyArm = mdata[1]
		emptyMoment = mdata[2]
		frontpax_arm = mdata[3]
		rearpax_arm = mdata[4]
		fuel_arm = mdata[5]
		baggage_arm = mdata[6]
		type = mdata[7]
		location = mdata[8]
		break
	except:
		print('Aircraft not found in database')

# Ask user for FRONT PAX weight
while True:
	frontPaxWeight = input('FRONT PAX weight: ')
	if frontPaxWeight == 'done':
		finished()
	try:
		frontPaxWeight = int(frontPaxWeight)
		break
	except:
		invalid()

# Ask user for REAR PAX weight
while True:
	rearPaxWeight = input('REAR PAX weight: ')
	if rearPaxWeight == 'done':
		finished()
	try:
		rearPaxWeight = int(rearPaxWeight)
		break
	except:
		invalid()

# Ask user for FUEL in gallons
while True:
	fuelWeight = input('FUEL in gallons: ')
	if fuelWeight == 'done':
		finished()
	try:
		fuelWeight = int(fuelWeight) * 6
		break
	except:
		invalid()

# Ask user for BAGGAGE weight
while True:
	baggageWeight = input('BAGGAGE weight: ')
	if baggageWeight == 'done':
		finished()
	try:
		baggageWeight = int(baggageWeight)
		break
	except:
		invalid()

# Ask user for FUEL BURN in gallons
while True:
	burnWeight = input('FUEL BURN in gallons: ')
	if burnWeight == 'done':
		finished()
	try:
		burnWeight = int(burnWeight) * 6
		break
	except:
		invalid()

zero_weight = emptyWeight + frontPaxWeight + rearPaxWeight + baggageWeight
zero_moment = emptyMoment + (frontPaxWeight * frontpax_arm) + (rearPaxWeight * rearpax_arm) + (baggageWeight * baggage_arm)
zero_cg = zero_moment / zero_weight

takeoff_weight = zero_weight + fuelWeight
takeoff_moment = zero_moment + (fuelWeight * fuel_arm)
takeoff_cg = takeoff_moment / takeoff_weight

landing_weight = takeoff_weight - burnWeight
landing_moment = takeoff_moment - (burnWeight * fuel_arm)
landing_cg = landing_moment / landing_weight

print()
print(f'~ Weight and Balance Calculations for {aircraft}, {type} based in {location} ~')
print()
print(f'Zero fuel weight: {zero_weight:.2f}')
print(f'Zero fuel CG: {zero_cg:.2f}')
print(f'Zero fuel moment: {zero_moment:.2f}')
print()
print(f'Takeoff weight: {takeoff_weight:.2f}')
print(f'Takeoff CG: {takeoff_cg:.2f}')
print(f'Takeoff moment: {takeoff_moment:.2f}')
print()
print(f'Landing weight: {landing_weight:.2f}')
print(f'Landing CG: {landing_cg:.2f}')
print(f'Landing moment: {landing_moment:.2f}')
print()
print('~ Happy landings ~\n')
