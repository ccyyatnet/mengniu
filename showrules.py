def load_rules(addr):
	file_rules = open(addr,'r')
	rules = []
	for i in range(3):
		rules.append(file_rules.readline().split())
	#show rules
	print 'RULES:'
	for i in range(3):
		print '*** %d ***' % i 
		for rule in rules[i]:
			print rule
	file_rules.close()
	return rules

def fetch_keywords(addr):
	file_keywords = open(addr,'r')
	keywords = file_keywords.readline().split('|')
	#for i in keywords:	
	#	print i
	file_keywords.close()
	return keywords

if __name__ == '__main__':
	load_rules('../mengniu/rules.dat')