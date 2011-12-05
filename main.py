# coding: utf-8
import logging
import os
import shutil
import time

__author__ = "Alexander Soulimov (alexander.soulimov@gmail.com)"
__copyright__ = "Copyright (c) 2011 A.Soulimov"
__license__ = "Python"

def set_logging(file_level, console_level, log_path, clean_old=True):
	"""
	Set logging parameters
	@return: None
	"""
	# set up logging to file - see previous section for more details

	if clean_old:
		try:
			shutil.rmtree(log_path)
		except WindowsError:
			pass
		#dirpath=os.path.abspath(__file__) + log_path
		os.mkdir(log_path)

	log_format = '%(message)s'

	# generate log name
	log_name = time.strftime('%m_%d_%Y_%H_%M_%S', time.gmtime()) + "_rk_2.log"

	logging.basicConfig(level=logging.DEBUG,
						format=log_format,
						datefmt='%m/%d/%Y %H:%M:%S',
						filename=log_path + log_name,
						filemode='w')
	# define a Handler which writes INFO messages or higher to the sys.stderr
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	# set a format which is simpler for console use
	formatter = logging.Formatter(log_format, '%m/%d/%Y %H:%M:%S')
	# tell the handler to use this format
	console.setFormatter(formatter)
	# add the handler to the root logger
	logging.getLogger('').addHandler(console)

def main():
	set_logging(logging.DEBUG, logging.DEBUG, "./log/")


if __name__ == "__main__":
	main()