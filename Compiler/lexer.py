# coding: utf-8

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"



def get_tokens(code):
	"""
	Get tokens of the code
	@param code: code lines
	@type code: list of string
	@return: list of tokens
	"""

	tokens = list()
	input = False
	input_values = list()
	for code_line in code:
		# prepare the code line
		# assume that at least one blank or tab separates each token
		code_line = code_line.replace('\t', ' ').replace('\n', '').replace('  ', ' ').strip()
		if code_line == '':
			continue
		line_tokens = code_line.split(' ')

		if not input:
			tokens.extend(line_tokens)
		else:
			input_values.append(line_tokens[0])
		if 'END' in line_tokens:
			input = True

	return tokens, input_values

if __name__ == "__main__":
	code_file = open('./../Input/example1.txt', 'r')
	code_lines = code_file.readlines()
	code_file.close()
	t, inp = get_tokens(code_lines)
	print t
	print inp