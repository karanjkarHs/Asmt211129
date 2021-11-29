###################################################################
#Script Name	: log                                                                                             
#Description	: General logging for info, error and unhandled exceptions.                                                                                                                                                                          
#Author       	: Harshad S Karanjkar                                                
#Date         	: December 2020
#Last Modified  :
#Modified By    :                                             
###################################################################
#get home directory path
from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
from config import log_file_home_path

"""Custom logging."""
from sys import stdout
from loguru import logger as custom_logger

def create_logger(novelLogName):
	"""Create custom logger."""
	#global log_file_path
	if novelLogName:
		log_file_path = log_file_home_path + novelLogName + "-"
	else:	
		log_file_path = log_file_home_path
	custom_logger.remove()
	custom_logger.add(
		log_file_path + "info.log",
		colorize=True,
		level="INFO",
		format="{time:MM-DD-YYYY HH:mm:ss} | \
		{level} \
		{message}",
        rotation="12:00",
        retention="5 days"
        #backtrace=True,
        #diagnose=True
	)
	custom_logger.add(
		log_file_path + "error.log",
		colorize=True,
		level="ERROR",
		catch=True,
		format="{time:MM-DD-YYYY HH:mm:ss} | \
		{level} \
		{message}",
        rotation="12:00",
        retention="5 days"
        #backtrace=True,
        #diagnose=True
	)
	return custom_logger


logger = create_logger(novelLogName = None)