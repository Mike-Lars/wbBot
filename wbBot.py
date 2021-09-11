import sqlite3

# Establish db connection and make cursor
conn = sqlite3.connect('wbBot.sqlite')
cur = conn.cursor()

# Create aircraft table if one doesn't already exist
cur.execute('''
CREATE TABLE IF NOT EXISTS Aircraft(
	make TEXT, 
	model TEXT,
	tail_number TEXT,
	empty_weight INTEGER,
	arm INTEGER,
	moment INTEGER,
	useful_load INTEGER
)
''')

# # Insert statements
# cur.execute('''
# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "R", "N512CT", 1701.00, 40.336, 68611.53, 756);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "R", "N815CT", 1709.00, 41.3024, 70585.8, 748);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N512ND", 1725.3953, 41.3452, 71336.8, 832.6047);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N566ND", 1725.875, 41.3139, 71302.56, 832.125);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N6318D", 1675.3, 40.3512, 67600.35, 882.7);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N712DS", 1685.694, 40.9612, 69047.99, 872.306);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N5113J", 1714.1, 41.8105, 71667.31, 873.9);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N551ND", 1724.2, 41.2777, 71170.97, 833.8);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N6318L", 1703.1, 41.6, 70848.96, 854.9);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N5138Q", 1714.155, 41.8095, 71667.9, 843.845);

# INSERT INTO Aircraft (make, model, tail_number, empty_weight, arm, moment, useful_load)
# VALUES ("C172", "S", "N5138G", 1714.14, 41.81, 61668.19, 843.86);
# ''')

# Define function for program quit and exit message
def exit():
	print('\n~ Happy landings ~\n')
	quit()

# Define function to handle invalid input
def invalid():
	print('Invalid entry')

print("\n~ WB Bot at your service. Type 'done' at any time to finish ~\n")

# Ask user for aircraft
while True:
	aircraft = input('Aircraft tail number: ')
	if aircraft == 'done':
		exit()
	aircraft = aircraft.upper()
	# Grab aircraft's empty weight, arm and moment from db
	try:
		cur.execute('''SELECT empty_weight FROM Aircraft WHERE tail_number=?''', (aircraft,))
		emptyWeight = cur.fetchone()[0]
		cur.execute('''SELECT arm FROM Aircraft WHERE tail_number=?''', (aircraft,))
		arm = cur.fetchone()[0]
		cur.execute('''SELECT moment FROM Aircraft WHERE tail_number=?''', (aircraft,))
		moment = cur.fetchone()[0]
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
zero_moment = moment + (frontPaxWeight * 37) + (rearPaxWeight * 73) + (baggageWeight * 95)
zero_cg = round(zero_moment / zero_weight, 2)

takeoff_weight = round(zero_weight + fuelWeight, 2)
takeoff_moment = round(zero_moment + (fuelWeight * 48), 2)
takeoff_cg = round(takeoff_moment / takeoff_weight, 2)

landing_weight = round(takeoff_weight - burnWeight, 2)
landing_moment = round(takeoff_moment - (burnWeight * 48), 2)
landing_cg = round(landing_moment / landing_weight, 2)

print('\n\n~ Weight and Balance Calculations ~')

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