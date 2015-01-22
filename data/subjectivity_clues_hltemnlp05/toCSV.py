import re
from csv import writer

with open('subjclueslen1-HLTEMNLP05.tff','rb') as f:
	with open('subjclueslen1.csv','w') as out:
		
		output = writer(out)
		#Write headers.
		output.writerow(['type','len','word1','pos1','stemmed1','priorpolarity'])

		for line in f:
			line = re.sub(r'(type|len|word1|pos1|stemmed1|priorpolarity)=','',line)
			line = line.strip()
			row = line.split(' ')
			output.writerow(row)
print 'Processing complete.'
exit()