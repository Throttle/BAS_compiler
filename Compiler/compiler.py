# coding: utf-8
import logging

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"
from main import set_logging
from lexer import get_tokens
from bas_parser import runParser

local_variables = dict()
input_parameters = list()

input = None
primary_code = list()

def get_variable_index(var):
	if not len(var):
		return 0
	else:
		return var[0]

temp_inc = 0
def get_new_temp():
	global temp_inc
	temp_inc += 1
	return 't' + str(temp_inc)

current_label = 'PROGRAM'
def code(op, arg1, arg2, res, ind1=0, ind2=0, res_ind=0):
	primary_code.append((current_label, op, arg1, ind1, arg2, ind2, res, res_ind))
	for line in primary_code:
		print line


def get_classification(tree):
	"""

	@param tree:
	@return:
	"""
	global current_label
	# если уже в листе
	if type(tree) != dict:
		print "TERMINAL: " + str(tree)
		return tree
	else:
		print tree
		attr = tree.keys()[0]
		print tree[attr]
		results = list()
		if attr == "label":
			current_label = tree[attr].replace(':','')
		elif attr=="KEY":
			if tree['KEY'] == "END":
				code('END', '', '', '')
		if type(tree[attr]) is list:
			for subtree in tree[attr]:
				results.append(get_classification(subtree))
			if attr == "instr":
				if results[0] == "LET":
					code(results[2], results[1][0], results[3][0], results[1][0], get_variable_index(results[1][1]))
				elif results[0] == "GET":
					code(":=", results[1][0], 'input', results[1][0], results[1][1][1], 'next', results[1][1][1])
				elif results[0] == "JUMP":
					code("JUMP", results[3][0], '', results[1], get_variable_index(results[3][1]))
				elif results[0] == "PUT":
					if type(results[1]) is list:
						code("PUT", results[1][0], '', '', results[1][1][1])
					else:
						code("PUT", results[2], '', '')
				elif results[0] == "LINE":
					code("PUT", "\n", '', '')
			elif attr == "R3":
				if len(results) == 1:
					results = results[0]
			elif attr == "expr":
				if not len(results[1]):
					results = results[0]
				else:
					temp = get_new_temp()
					code(results[1][0], results[0][0], results[1][1][0], temp, get_variable_index(results[0][1]), get_variable_index(results[1][1][1]))
					results = [temp, []]


			return results
		else:
			return tree[attr]

def GET(term, index=0):
	in_val = None
	try:
		in_val =input.next()
	except Exception:
		pass

	if not local_variables.has_key(term):
		local_variables[term] = list()
		local_variables[term].append(in_val)
	else:
		try:
			local_variables[term][index] = in_val
		except IndexError:
			local_variables[term].append(in_val)





def runCompiler(tree):
	from executer import execute
	get_classification(tree)
	print "Start executing..."

	execute(primary_code, input_parameters)



if __name__ == "__main__":
	global input_parameters
	global input
	set_logging(logging.DEBUG, logging.DEBUG, "./../log/")
	code_file = open('./../Input/example1.txt', 'r')
	code_lines = code_file.readlines()
	code_file.close()
	chain_lines, input_variables = get_tokens(code_lines)
	input_parameters = map(lambda x: int(x), input_variables)
	#chain_lines = [";", "asdasdasdasdqwe asd", "END"]
	tree = runParser(chain_lines)
	runCompiler(tree)




