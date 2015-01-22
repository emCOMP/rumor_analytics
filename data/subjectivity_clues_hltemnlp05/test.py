def get_subjective(filename):
	
	subjective = set()
	with open(filename,'rb') as f:
		csv_reader = csv.reader(f)
		headers = True
		for row in csv_reader:
			if headers:
				headers = False
			else:
				#If it's a strongly subjective word.
				if row[0] == 'strongsubj':
					subjective.add(row[2])

	return subjective