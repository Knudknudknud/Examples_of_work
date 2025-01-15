"""
The terminal_logger is used to allow toggling of print statements, more specifically to sys.stderr.
Likewise the use of terminal_logger was used to make tests of Error prints easier to test for with unittest
without having to override sys.stdout and other convoluted methods.
"""
import logging

#Creates a handler that redirects log messages to the terminal "sys.stderr"
terminal_handler = logging.StreamHandler()
#Sets the format, to be user friendly.
terminal_handler.setFormatter(logging.Formatter('%(message)s'))

#create logger for terminal with above handler.
terminal_logger = logging.getLogger('terminal_logger')
terminal_logger.setLevel(logging.INFO)
terminal_logger.addHandler(terminal_handler)
