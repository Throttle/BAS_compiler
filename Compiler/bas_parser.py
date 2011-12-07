# coding: utf-8
import logging
import re


__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"

# symbol Current Token:
#sp=0
# current chain
#chain=""
# level identetion
level = 0

# numbers
re_digit = "^[0-9]*$"
# identificators
re_letter = "^[A-Z]*$"
re_label = "^[A-Z]*:$"
# unary operations
re_unop = "^[-!]$"
# binary operations
re_binop = "+-*\/%=>"
# character
re_character = "^[\s\w\d:_]*$"

KEYWORDS = dict()

all_tokens = None
current_token = None
token_index = None

def get_next_token():
	global token_index
	global current_token
	token_index += 1
	if token_index < len(all_tokens):
		current_token = all_tokens[token_index]
	else:
		current_token = None


def init_keywords():
	global KEYWORDS

	KEYWORDS['LET'] = 'LET'
	KEYWORDS['GET'] = 'GET'
	KEYWORDS['JUMP'] = 'JUMP'
	KEYWORDS['IF'] = 'IF'
	KEYWORDS['PUT'] = 'PUT'
	KEYWORDS['LINE'] = 'LINE'
	KEYWORDS['END'] = 'END'


def print_error(waiting, after):
	print_in_log("Current Token: " + str(current_token) + ", error: waiting \'" + waiting + "\' after \'" + after + "\'!")


def print_in_log(message):
	msg = "-> " + message + " current token: " + str(current_token)
	logging.info(msg.replace("\n", ""))


def printer(func):
	def wrapper(*args, **kwargs):
		global level
		msg = "--" * level + "> " + func.__name__ + " ( current token: " + str(current_token) +")"

		logging.info(msg.replace("\n", ""))
		result = func(*args, **kwargs)

		level -= 1
		return result
	return wrapper


def level_increment(func):
	def wrapper(*args, **kwargs):
		global level
		level += 1
		result = func(*args, **kwargs)
		return result
	return wrapper


def runParser(tokens):
	"""
	Run the parser

	@return:
	"""
	global token_index
	global all_tokens
	# Primary initialization
	token_index = -1
	all_tokens = tokens[:]
	init_keywords()
	get_next_token()

	logging.info("^"*80)
	logging.info("Analyzing chain: " + str(tokens))


	# Let's get it on
	tree = Program()
	if tree:
		logging.info("-> CHAIN IS CORRECT!!!\nNo Errors occured!")
		return tree # Все прошло нормально
	else:
		logging.info("-> CHAIN IS WRONG!!!\nInternal Errors occured!")

	return None # Есть ошибки


@level_increment
@printer
def Program():
	key = 'Program'
	result = None
	tree_full = dict()
	tree_full[key] = list()

	subtree = CC()
	if current_token != KEYWORDS["END"]:
		subtree = II()
		if not subtree:
			print_error("CC or II", "Program")
			result = False

	tree_full[key].append(subtree)

	subtree = KEY("END")
	if subtree:
		tree_full[key].append(subtree)
		if current_token is None:
			result = tree_full
		else:
			print_error("string end", "END")
	else:
		print_error("END", "CC or II")
		result = False
	print tree_full
	return result

@level_increment
@printer
def CC():
	key = 'CC'
	current_tree = dict()
	current_tree[key] = list()

	result = list()

	subtree = comment()
	if subtree:
		current_tree[key].append(subtree)
		subtree = CC()
		if not subtree is None:
			current_tree[key].append(subtree)
			result = current_tree
		else:
			print_error("CC", "comment")
			result = None

	return result

@level_increment
@printer
def II():
	key = 'II'
	current_tree = dict()
	current_tree[key] = list()
	result = list()

	subtree = instr()
	if subtree:
		current_tree[key].append(subtree)
		subtree = II()
		if not subtree is None:
			current_tree[key].append(subtree)
			result = current_tree
		else:
			print_error("II", "instr")
			result = None

	return result

@level_increment
@printer
def comment():
	key = 'comment'
	current_tree = dict()
	current_tree[key] = list()

	result = None
	subtree = semicolon()
	if subtree:
		current_tree[key].append(subtree)
		subtree = string_()
		if subtree:
			current_tree[key].append(subtree)
			result = current_tree
		else:
			print_error("string", "semicolumn")
			result = None

	return result

@level_increment
@printer
def string_():
	if current_token is None:
		return None
	if re.match(re_character, current_token):
		current_tree = dict()
		current_tree['comment_string'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def ident():
	if current_token is None:
		return None
	if re.match(re_letter, current_token):
		current_tree = dict()
		current_tree['ident'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def label():
	if current_token is None:
		return None
	if re.match(re_label, current_token):
		current_tree = dict()
		current_tree['label'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def posint():
	if current_token is None:
		return None
	if re.match(re_digit, current_token):
		current_tree = dict()
		current_tree['posint'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def semicolon():
	current_tree = dict()
	current_tree['semicolumn'] = list()

	if current_token is None:
		return None

	if current_token == ";":
		get_next_token()
		current_tree['semicolumn'] = ";"
		return current_tree
	return None

@level_increment
@printer
def quote():
	if current_token is None:
		return None

	if current_token == "\'":
		current_tree = dict()
		current_tree['quote'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def colon():
	if current_token is None:
		return None

	if current_token == ":":
		current_tree = dict()
		current_tree['colon'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def unop():
	if current_token is None:
		return None

	if re.match(re_unop, current_token):
		current_tree = dict()
		current_tree['unop'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def binop():
	if current_token is None:
		return None

	if current_token in re_binop:
		current_tree = dict()
		current_tree['binop'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def assignment():
	if current_token is None:
		return None

	if current_token == ":=":
		current_tree = dict()
		current_tree['assignment'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def lparent():
	if current_token is None:
		return None

	if current_token == "(":
		current_tree = dict()
		current_tree['lparent'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def rparent():
	if current_token is None:
		return None

	if current_token == ")":
		current_tree = dict()
		current_tree['rparent'] = current_token
		get_next_token()
		return current_tree
	return None

@level_increment
@printer
def instr():
	current_tree = dict()
	current_tree['instr'] = list()

	result = None
	subtree = KEY('LET')
	if subtree:
		current_tree['instr'].append(subtree)
		subtree = term()
		if subtree:
			current_tree['instr'].append(subtree)
			subtree = assignment()
			if subtree:
				current_tree['instr'].append(subtree)
				subtree = R3()
				if subtree:
					current_tree['instr'].append(subtree)
					result = current_tree
				else:
					print_error("R3", "assignment")
			else:
				print_error("assignment", "term")
		else:
			print_error("term", "LET")
	else:
		subtree = KEY('JUMP')
		if subtree:
			current_tree['instr'].append(subtree)
			subtree = ident()
			if subtree:
				current_tree['instr'].append(subtree)
				subtree = KEY('IF')
				if subtree:
					current_tree['instr'].append(subtree)
					subtree = expr()
					if subtree:
						current_tree['instr'].append(subtree)
						result = current_tree
					else:
						print_error("expr", "IF")
				else:
					print_error("IF", "ident")
			else:
				print_error("ident", "JUMP")
		else:
			subtree = KEY('GET')
			if subtree:
				current_tree['instr'].append(subtree)
				subtree = term()
				if subtree:
					current_tree['instr'].append(subtree)
					result = current_tree
				else:
					print_error("term", "GET")
			else:
				subtree = KEY('PUT')
				if subtree:
					current_tree['instr'].append(subtree)
					subtree = term()
					if subtree:
						current_tree['instr'].append(subtree)
						result = current_tree
					else:
						subtree =  quote()
						if subtree:
							current_tree['instr'].append(subtree)
							subtree = string_()
							if subtree:
								current_tree['instr'].append(subtree)
								subtree = quote()
								if subtree:
									current_tree['instr'].append(subtree)
									result = current_tree
								else:
									print_error("quote", "string")
							else:
								print_error("string", "quote")
						else:
							print_error("term", "GET")
				else:
					subtree = KEY('LINE')
					if subtree:
						current_tree['instr'].append(subtree)
						result = current_tree
					else:
						subtree = label()
						if subtree:
							current_tree['instr'].append(subtree)
							result = current_tree

	return result

@level_increment
@printer
def term():
	current_tree = dict()
	current_tree['term'] = list()
	result = None
	subtree = ident()
	if subtree:
		current_tree['term'].append(subtree)
		subtree = R1()
		if not subtree is None:
			current_tree['term'].append(subtree)
			result = current_tree
		else:
			print_error("R1", "ident")
	return result

@level_increment
@printer
def expr():
	current_tree = dict()
	current_tree['expr'] = list()
	result = None

	subtree = term()
	if subtree:
		current_tree['expr'].append(subtree)
		subtree = R2()
		if not subtree is None:
			current_tree['expr'].append(subtree)
			result = current_tree
		else:
			print_error("R2", "term")
	else:
		subtree = unop()
		if subtree:
			current_tree['expr'].append(subtree)
			subtree = term()
			if subtree:
				current_tree['expr'].append(subtree)
				result = current_tree
			else:
				print_error("term", "unop")
	return result

@level_increment
@printer
def R1():
	current_tree = dict()
	current_tree['R1'] = list()
	result = list()

	subtree = lparent()

	if subtree:
		current_tree['R1'].append(subtree)
		subtree = ident()
		if subtree:
			current_tree['R1'].append(subtree)
			subtree = rparent()
			if subtree:
				current_tree['R1'].append(subtree)
				result = current_tree
			else:
				print_error(")", "ident")
				result = None
		else:
			print_error("ident", "(")
			result = None
	return result

@level_increment
@printer
def R2():
	current_tree = dict()
	current_tree['R2'] = list()

	result = list()

	subtree = binop()
	if subtree:
		current_tree['R2'].append(subtree)
		subtree = term()
		if subtree:
			current_tree['R2'].append(subtree)
			result = current_tree
		else:
			print_error("term", "binop")
			result = None
	return result

@level_increment
@printer
def R3():
	tree = dict()
	tree['R3'] = list()
	result = None
	subtree = expr()
	if subtree:
		tree['R3'].append(subtree)
		result = tree
	else:
		subtree = posint()
		if subtree:
			tree['R3'].append(subtree)
			result = tree
	return result

@level_increment
@printer
def KEY(key):
	if current_token is None:
		return None

	if current_token == KEYWORDS[key]:
		tree = dict()
		tree['KEY'] = current_token
		get_next_token()
		return tree
	return None


if __name__ == "__main__":
	from main import set_logging
	from lexer import get_tokens
	set_logging(logging.DEBUG, logging.DEBUG, "./../log/")
	code_file = open('./../Input/example1.txt', 'r')
	code_lines = code_file.readlines()
	code_file.close()
	chain_lines = get_tokens(code_lines)
	#chain_lines = [";", "asdasdasdasdqwe asd", "END"]
	runParser(chain_lines)