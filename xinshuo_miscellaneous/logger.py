# -*- coding: utf-8 -*-

# Author: Xinshuo Weng
# Email: xinshuo.weng@gmail.com

from __future__ import print_function


# logging
def print_log(print_str, log, same_line=False, display=True):
	'''
	print a string to a log file

	parameters:
		print_str:          a string to print
		log:                a opened file to save the log
		same_line:          True if we want to print the string without a new next line
		display:            False if we want to disable to print the string onto the terminal
	'''
	if display:
		if same_line: print('{}'.format(print_str), end='')
		else: print('{}'.format(print_str))

	if same_line:
		log.write('{}'.format(print_str))
	else:
		log.write('{}\n'.format(print_str))
	log.flush()
