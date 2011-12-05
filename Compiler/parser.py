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
	if Program():
		logging.info("-> CHAIN IS CORRECT!!!\nNo Errors occured!")
		return True # Все прошло нормально
	else:
		logging.info("-> CHAIN IS WRONG!!!\nInternal Errors occured!")

	return False # Есть ошибки


@level_increment
@printer
def Program():
	result = False
	if CC():
		pass

	if current_token != KEYWORDS["END"]:
		if II():
			pass
		else:
			print_error("CC or II", "Program")
			result = False

	if KEY("END"):
		if current_token is None:
			return True
		else:
			print_error("string end", "END")
	else:
		print_error("END", "CC or II")
		result = False
	return result

@level_increment
@printer
def CC():
	result = True
	if comment():
		if CC():
			result = True
		else:
			print_error("CC", "comment")
			result = False

	return result

@level_increment
@printer
def II():
	result = True
	if instr():
		if II():
			result = True
		else:
			print_error("II", "instr")
			result = False

	return result

@level_increment
@printer
def comment():
	result = False
	if semicolon():
		if string_():
			return True
		else:
			print_error("string", "semicolumn")
			result = False

	return result

@level_increment
@printer
def string_():
	if current_token is None:
		return False
	if re.match(re_character, current_token):
		get_next_token()
		return True
	return False

@level_increment
@printer
def ident():
	if current_token is None:
		return False
	if re.match(re_letter, current_token):
		get_next_token()
		return True
	return False

@level_increment
@printer
def label():
	if current_token is None:
		return False
	if re.match(re_label, current_token):
		get_next_token()
		return True
	return False

@level_increment
@printer
def posint():
	if current_token is None:
		return False
	if re.match(re_digit, current_token):
		get_next_token()
		return True
	return False

@level_increment
@printer
def semicolon():
	if current_token is None:
		return False

	if current_token == ";":
		get_next_token()
		return True
	return False

@level_increment
@printer
def quote():
	if current_token is None:
		return False

	if current_token == "\'":
		get_next_token()
		return True
	return False

@level_increment
@printer
def colon():
	if current_token is None:
		return False

	if current_token == ":":
		get_next_token()
		return True
	return False

@level_increment
@printer
def unop():
	if current_token is None:
		return False

	if re.match(re_unop, current_token):
		get_next_token()
		return True
	return False

@level_increment
@printer
def binop():
	if current_token is None:
		return False

	if current_token in re_binop:
		get_next_token()
		return True
	return False

@level_increment
@printer
def assignment():
	if current_token is None:
		return False

	if current_token == ":=":
		get_next_token()
		return True
	return False

@level_increment
@printer
def lparent():
	if current_token is None:
		return False

	if current_token == "(":
		get_next_token()
		return True
	return False

@level_increment
@printer
def rparent():
	if current_token is None:
		return False

	if current_token == ")":
		get_next_token()
		return True
	return False

@level_increment
@printer
def instr():
	result = False
	if KEY('LET'):
		if term():
			if assignment():
				if R3():
					result = True
				else:
					print_error("R3", "assignment")
			else:
				print_error("assignment", "term")
		else:
			print_error("term", "LET")
	elif KEY('JUMP'):
		if ident():
			if KEY('IF'):
				if expr():
					result = True
				else:
					print_error("expr", "IF")
			else:
				print_error("IF", "ident")
		else:
			print_error("ident", "JUMP")
	elif KEY('GET'):
		if term():
			result = True
		else:
			print_error("term", "GET")
	elif KEY('PUT'):
		if term():
			result = True
		elif quote():
			if string_():
				if quote():
					result = True
				else:
					print_error("quote", "string")
			else:
				print_error("string", "quote")
		else:
			print_error("term", "GET")
	elif KEY('LINE'):
		result = True

	elif label():
		result = True

	return result

@level_increment
@printer
def term():
	result = False
	if ident():
		if R1():
			result = True
		else:
			print_error("R1", "ident")
	return result

@level_increment
@printer
def expr():
	result = False
	if term():
		if R2():
			result = True
		else:
			print_error("R2", "term")
	elif unop():
		if term():
			result = True
		else:
			print_error("term", "unop")
	return result

@level_increment
@printer
def R1():
	result = True
	if lparent():
		if ident():
			if rparent():
				result = True
			else:
				print_error(")", "ident")
		else:
			print_error("ident", "(")
	return result

@level_increment
@printer
def R2():
	result = True
	if binop():
		if term():
			result = True
		else:
			print_error("term", "binop")
			result = False
	return result

@level_increment
@printer
def R3():
	result = False
	if expr():
		result = True
	elif posint():
		result = True

	return result

@level_increment
@printer
def KEY(key):
	if current_token is None:
		return False

	if current_token == KEYWORDS[key]:
		get_next_token()
		return True
	return False


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