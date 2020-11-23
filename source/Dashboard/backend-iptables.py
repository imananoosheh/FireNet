import subprocess as sb
import logging


#OBJECT_ADDED_SUCCESSFULLY = 0
#ENTRY_IS_ALREADY_ADDED = 1
#ERROR_WHILE_ADDING_ENTRY = 2
#SET_CREATED_SUCCESSFULLY = 3
#ERROR_WHILE_CREATING_SET = 4
#POLICY_WAS_ADDED_SUCCESSFULLY = 5
#ERROR_WHILE_ADDING_POLICY = 6
#OBJECT_DELETED_SUCCESSFULLY = 7
#ERROR_WHILE_DELETING_OBJECT = 8
#IPSET_DESTROYED_SUCCESSFULLY = 9
#ERROR_WHILE_DESTROYING_IPSET =10



def getAllSets():
	sets_list = []
	out = sb.Popen(['sudo', 'ipset', 'list'], shell = False, stdout = sb.PIPE)
	res, err = out.communicate()
	if res:
		num_of_sets = int(len(res.split('Name: ')) - 1)
		for i in range(1, num_of_sets + 1):
			sets_dict = {}
			name = res.split("Name: ")[i].split('\n')[0]
			sets_dict['set_name'] = name
			
			number_of_entires = int(res.split('Number of entries: ')[i].split('\n')[0])
			addresses_list = []
			for j in range(number_of_entires):
				addresses_list.append(res.split('Number of entries: ')[i].split('\n')[2+j])

			sets_dict['addresses'] = addresses_list
			sets_list.append(sets_dict)

	return sets_list


def ipsetLogging(logger):
	fhl = logging.FileHandler('ipset.log')
	formatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')
	logger.setLevel(logging.DEBUG)

	ch = logging.StreamHandler()
	logger.addHandler(ch)
	ch.setFormatter(formatter)
	ch.setLevel(logging.DEBUG)

	logger.addHandler(fhl)
	fhl.setFormatter(formatter)
	fhl.setLevel(logging.DEBUG)





#it deletes a single entry from a special ipset
def deleteIpsetEntry(set_name, entry_value):
	out = sb.Popen(['sudo', 'ipset', 'del', set_name, entry_value], shell = False, stderr = sb.PIPE)
	res, err = out.communicate()
	if not err:
		logger.debug('Entry %s was deleted from set %s successfully' % (entry_value, set_name))
		#sb.Popen(['/etc/ipset_save.sh'], shell = False)
		sb.call('sudo ipset save > /etc/Firewall/ipsetSave.conf', shell = True)
	else:
		logger.debug('%s' %err)




#it destroys an ipset
def destroyIpset(set_name):
	out = sb.Popen(['sudo', 'ipset', 'destroy', set_name], shell = False, stderr = sb.PIPE)
	res, err = out.communicate()
	if err:
		logger.debug("%s" %err)
	else:
		logger.debug('IPset %s was destroyed completely' %set_name)
		sb.call('sudo ipset save > /usr/local/etc/ipsetSave.conf', shell = True)
		#sb.Popen(['/etc/ipset_save.sh'], shell = False)




#it edits a single entry
def editIpsetEntry(old_set_name, new_set_name, new_value, old_value, new_type="hash:net", old_type="hash:net"):
	if old_set_name == new_set_name  and new_type == old_type:
		deleteIpsetEntry(old_set_name, old_value)
		addIpsetEntry(new_set_name, new_value)
		logger.debug("Entry in set %s was replaced with %s in set %s" %(old_set_name, new_value, new_set_name))	
		sb.call('sudo ipset save > /usr/local/etc/ipsetSave.conf', shell = True)
		
	else:
		if new_type == "iprange" or new_type == "fqdn":
			createIpset(new_set_name, "hash:ip")
		if new_type == "hash:net":
			createIpset(new_set_name, "hash:net")
		if new_type == "mac":
			createIpset(new_set_name, "hash:mac")
		addIpsetEntry(new_set_name, new_value)
	
	logger.debug("Entry with value of {%s} in set (%s) was replaced with {%s} in set (%s)" %(old_value, old_set_name, new_value, new_set_name))	
	sb.call('sudo ipset save > /usr/local/etc/ipsetSave.conf', shell = True)
	return True




def createIpset(set_name, set_type="hash:net"):
	out = sb.Popen(['sudo', 'ipset', '-N', set_name, set_type, 'comment'], shell = False, stderr = sb.PIPE)
	res,err = out.communicate()
	if err:
		logger.debug('%s' %err)
	else:
		logger.debug('IPset named %s of type %s was created successfully' % (set_name, set_type))
		sb.call('sudo ipset save > /etc/Firewall/ipsetSave.conf', shell = True)
		#sb.Popen(['/etc/ipset_save.sh'], shell = False)




def addIpsetEntry(set_name, entry_value ,comment=""):
	out = sb.Popen(['sudo', 'ipset', '-A', set_name, entry_value, '--exist'], shell = False, stderr = sb.PIPE)
	out.wait()
	err = out.communicate()
	if err[1]:
		logger.debug('%s' %err[1])
		return 1
	else:
		logger.debug('Entry %s was added successfully in set %s' %(entry_value, set_name))
		#sb.Popen(['/etc/ipset_save.sh'], shell = False)
		return 0


		

def addRule(policy_name, address_set, interface, port, protocol, action, is_input):
	
	if is_input:
		proc = sb.Popen(['sudo', 'iptables', '-A', 'INPUT', '-m', 'set', '--match-set', address_set, 'src', '-p', protocol, '--sport', 
			port, '-m', 'comment', '--comment', policy_name, '-j',  action], shell = False, stderr = sb.PIPE)
		proc.wait()
		err = proc.communicate()
		if err[1]:
			logger.debug('%s' %err[1])
			return 6


	else:
		proc = sb.Popen(['sudo', 'iptables', '-A', 'OUTPUT', '-m', 'set', '--match-set', address_set, 'dst', '-p', protocol, '--dport', 
			port, '-m', 'comment', '--comment', policy_name, '-j', action ], shell = False, stderr = sb.PIPE)
		proc.wait()
		err = proc.communicate()
		if err[1]:
			logger.debug('%s' %err[1])
			return 6





def getAllRules(is_input):
	rules_list = []

	if is_input:
		proc = sb.Popen(['sudo', 'iptables', '-nvL', 'INPUT'], shell=False, stdout=sb.PIPE, stderr = sb.PIPE)
		
	else:
		proc = sb.Popen(['sudo', 'iptables', '-nvL', 'OUTPUT'], shell=False, stdout=sb.PIPE, stderr = sb.PIPE)

	proc.wait()
	output = proc.communicate()[0]

	splitted_output = output.split('\n')[2: len(output.split('\n')) - 1]
	for val in splitted_output:
		rule_dic = {}
		space_list = val.split(' ')
		space_list = filter(None, space_list)
		rule_dic['target'] = space_list[2]
		rule_dic['protocol'] = space_list[3]
		rule_dic['source_interface'] = space_list[5]
		rule_dic['set_name'] = space_list[10]
		rule_dic['policy_name'] = space_list[13]
		rules_list.append(rule_dic)

	return rules_list


def deleteRule(is_input, index):
	if is_input:
		proc = sb.Popen(['sudo', 'iptables', '-D', 'INPUT', str(index)], shell=False, stdout=sb.PIPE, stderr = sb.PIPE)
	else:
		proc = sb.Popen(['sudo', 'iptables', '-D', 'OUTPUT', str(index)], shell=False, stdout=sb.PIPE, stderr = sb.PIPE)

	

def main():
	print(getAllSets())


if __name__ == '__main__':
	main()