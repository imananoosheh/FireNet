import subprocess as sb
import iptc
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
	out = sb.Popen(['sudo', 'ipset', 'list'], shell = False, stdout = sb.PIPE)
	res, err = out.communicate()
	if res:
		sets = res.split("\n")
		for i in range(0, len(sets)):
			sets[i] = sets[i][6:]
	if res:
		sets.remove('')
		return sets
	else:
		return []




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
def editIpsetEntry(old_set_name, new_set_name, new_type, old_type, new_value, old_value):
	if old_set_name == new_set_name  and new_type == old_type:
		delete_entry(old_set_name, old_value)
		add_entry(new_set_name, new_value)
		logger.debug("Entry in set %s was replaced with %s in set %s" %(old_set_name, new_value, new_set_name))	
		sb.call('sudo ipset save > /usr/local/etc/ipsetSave.conf', shell = True)
		return False
	else:
		if new_type == "iprange" or new_type == "fqdn":
			create_unranged_ipset(new_set_name, "hash:ip")
		if new_type == "subnet":
			create_unranged_ipset(new_set_name, "hash:net")
		if new_type == "mac":
			create_unranged_ipset(new_set_name, "hash:mac")
		add_entry(new_set_name, new_value)
	
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
	if comment:
		comment = "(" + set_name + ") " + comment
	else:
		comment =  "(" + set_name + ")"

	out = sb.Popen(['sudo', 'ipset', '-A', set_name, entry_value, '--exist', 'comment', comment ], shell = False, stderr = sb.PIPE)
	out.wait()
	err = out.communicate()
	if err[1]:
		logger.debug('%s' %err[1])
		return 1
	else:
		logger.debug('Entry %s was added successfully in set %s' %(entry_value, set_name))
		#sb.Popen(['/etc/ipset_save.sh'], shell = False)
		return 0


        

def addInputRule(policy_name, src_address_set, src_port, protocol, action, comment=""):
    
    out = sb.Popen(['sudo', 'iptables', '-A', 'INPUT', '-m', '--set', src_address_set, '-p', protocol, '--sport', src_port, '-m', 'comment', '--comment', comment ], 
        shell = False, stderr = sb.PIPE)
	out.wait()
	err = out.communicate()
