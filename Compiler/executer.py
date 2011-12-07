# coding: utf-8

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"

control_table = dict()
input_params = None
input = None
local_params = dict()
sp = None
ip = None
all_code = None

def get_variable(name, index):
	res_val = None
	if name == "input":
		try:
			res_val = input.next()
		except Exception:
			pass
	elif not local_params.has_key(name):
		raise Exception("Undefined variable: " + name)
	else:
		if local_params.has_key(index):
			index = local_params[index][0]
		res_val = local_params[name][index]
	return res_val

def read_input():
	for var in input_params:
		yield var

def create_local_variable(res, res_ind, res_val):
	if not local_params.has_key(res):
		local_params[res] = list()
		local_params[res].append(res_val)
		return

	if local_params.has_key(res_ind):
		res_ind = local_params[res_ind][0]

	if res_ind == len(local_params[res]):
		local_params[res].append(res_val)
	elif res_ind < len(local_params[res]):
		local_params[res][res_ind] = res_val
	else:
		raise Exception("Index out of range: %s, %s"% (res, res_ind))

def get_value(arg, ind):
	res = None
	try:
		res = int(arg)
	except Exception:
		res = get_variable(arg, ind)
	return res

def LET(arg1, ind1, arg2, ind2, res, res_ind):
	res_val = get_value(arg2, ind2)

	if arg1 != res:
		raise Exception("Illegal operation params: %s, %s" % arg1)

	create_local_variable(res, res_ind, res_val)

def SUMM(arg1, ind1, arg2, ind2, res, res_ind):
	add1 = get_value(arg1, ind1)
	add2 = get_value(arg2, ind2)

	create_local_variable(res, res_ind, add1 + add2)

def MORE(arg1, ind1, arg2, ind2, res, res_ind):
	cmp1 = get_value(arg1, ind1)
	cmp2 = get_value(arg2, ind2)
	res_val = 0
	if cmp1 > cmp2:
		res_val = 1
	create_local_variable(res, res_ind, res_val)


def JUMP(arg1, ind1, arg2, ind2, res, res_ind):
	cmp1 = get_value(arg1, ind1)

	if cmp1 == 0:
		return

	global ip, sp
	for i in range(0, len(all_code)):
		if all_code[i][0] == res:
			sp = res
			ip = i
			break


def PUT(arg1, ind1, arg2, ind2, res, res_ind):
	try:
		print get_value(arg1, ind1)
	except:
		print arg1

def END(arg1, ind1, arg2, ind2, res, res_ind):
	pass


def create_control_table():
	global control_table
	control_table[":="] = LET
	control_table["+"] = SUMM
	control_table[">"] = MORE
	control_table["JUMP"] = JUMP
	control_table["PUT"] = PUT
	control_table["END"] = END



def execute(code, input_p):
	global all_code, input_params, input
	global ip, sp
	input_params = input_p
	input = read_input()
	all_code = code
	create_control_table()

	ip = 0
	while ip < len(code):
		ip += 1
		if ip-1 == 0:
			sp = code[ip-1][0]
		command = code[ip-1][1]
		control_table[command](code[ip-1][2], code[ip-1][3], code[ip-1][4], code[ip-1][5], code[ip-1][6], code[ip-1][7])
	pass