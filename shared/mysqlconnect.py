###################################################################
#Script Name	: mysqlconnect                                                                                             
#Description	: Handles conection to mysql database and performs read and write operation.                                                                                                                                                                          
#Author       	: Harshad S Karanjkar                                                
#Date         	: December 2020
#Last Modified  :
#Modified By    :                                             
###################################################################
#get home directory path
from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
#mysql-connector-python
import mysql.connector
from mysql.connector import Error, errorcode
from config import (
    database_hostname,
    database_user,
    database_password,
    database_port,
    database_name
)
from shared.log import logger


class ConnectionDB(object):
    def __init__(self):
        try:
            """ connect to the database """
            self.conn = mysql.connector.connect(
                host=database_hostname,
                database=database_name,
                user=database_user,
                password=database_password,
                port=database_port
            )
            logger.info(f'[mysqlconnect] Mysql connection Successful') 
            self.cursor = self.conn.cursor(buffered=True) 

        except mysql.connector.Error as error:
            logger.error(f'[mysqlconnect] Mysql connection failed: {error}')
            self.connectSuccess = False
            exit()                    

    """ fetch multiple row """
    @logger.catch
    def fetch_query(self, query, params=[]):
        try:         
            self.cursor.execute(query,params)
            result = self.cursor.fetchall()           
            logger.info(f'[mysqlconnect] Mysql query result fetched for {query} - {params} with result: {result}')             
            return result

        except mysql.connector.Error as error:
            logger.error(f'[mysqlconnect] Mysql error while fetch  for {query} - {params}: {error}')
            self.conn.close()
            exit()  

    """ fetch single row """
    @logger.catch
    def fetch_query_one(self, query, params=[]):
        try:
            self.cursor.execute(query,params)
            result = self.cursor.fetchone()
            logger.info(f'[mysqlconnect] Mysql query result fetched for {query} - {params} with result: {result}')           
            return result

        except mysql.connector.Error as error:
            logger.error(f'[mysqlconnect] Mysql error while fetch for {query} - {params}: {error}')
            self.conn.close()
            exit()  

    """ insert/update data """
    @logger.catch
    def exec_query(self, query, params=[]):
        try:
            self.cursor.execute(query,params)
            logger.info(f'[mysqlconnect] Mysql insert/update completed for {query} - {params}') 
            return self.cursor.rowcount

        except mysql.connector.Error as error:
            logger.error(f'[mysqlconnect] Mysql error while insert/update for {query} - {params}: {error}')
            self.conn.rollback()
            logger.info('[mysqlconnect] Mysql rollback changes')
            self.close_db_connection()
            logger.info('[mysqlconnect] Mysql connection closed')
            exit() 

    """ close connection"""
    @logger.catch
    def close_db_connection(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
            logger.info('[mysqlconnect] Mysql connection closed')
