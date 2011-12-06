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

def get_classification(tree):
	"""

	@param tree:
	@return:
	"""
	# если уже в листе
	if type(tree) != dict:
		print "TERMINAL: " + str(tree)
		return tree
	else:
		print tree
		attr = tree.keys()[0]
		print tree[attr]
		results = list()
		if type(tree[attr]) is list:
			for subtree in tree[attr]:
				results.append(get_classification(subtree))
			if attr == "instr":
				if results[0] == "LET":
					if not local_variables.has_key(results[1][0]):
						local_variables[results[1][0]] = list()
						res_val = None
						try:
							res_val = int(results[3][0])
						except Exception:
							res_index = results[3][0][0][1]
							if not res_index:
								res_index = 0
							else:
								res_index = res_index[0]
							res_val = local_variables[results[3][0][0][0]][res_index]

						local_variables[results[1][0]].append(res_val)
				elif results[0] == "GET":
					if not local_variables.has_key(results[1][0]):
						local_variables[results[1][0]] = list()

						res_ind = int(local_variables[results[1][1][1]][0]) - 1
						local_variables[results[1][0]].append(input_parameters[res_ind])
				elif results[0] == "JUMP":
					pass
			elif attr == "R3":
				pass
			elif attr == "expr":
				pass


			return results
		else:
			return tree[attr]



def runCompiler(tree):
	get_classification(tree)

if __name__ == "__main__":
	global input_parameters
	set_logging(logging.DEBUG, logging.DEBUG, "./../log/")
	code_file = open('./../Input/example1.txt', 'r')
	code_lines = code_file.readlines()
	code_file.close()
	chain_lines, input_variables = get_tokens(code_lines)
	input_parameters = map(lambda x: int(x), input_variables)
	#chain_lines = [";", "asdasdasdasdqwe asd", "END"]
	tree = runParser(chain_lines)
	print tree
	runCompiler(tree)