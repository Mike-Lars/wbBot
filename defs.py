if __name__ == '__main__':
	print("Please run 'wbBot.py' instead")
	quit()
else:
	# Define function for program quit and exit message
	def finished():
		print('\n~ Happy landings ~\n')
		quit()

	# Define function to handle invalid input
	def invalid():
		print('Invalid entry')