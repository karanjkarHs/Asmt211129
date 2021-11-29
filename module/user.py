from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
from shared.log import logger
from shared.mysqlconnect import ConnectionDB
from werkzeug.security import safe_str_cmp

class User(ConnectionDB):
    def __init__(self):
        ConnectionDB.__init__(self)  

    def findByName(self, user):
        try:
            query = f"select id,username,password from user where username = '{user}'"
            result = self.fetch_query_one(query)
            self.close_db_connection()
            return result
        except Exception as error:   
            logger.error(f"[User] Error encountered {error}") 
            return 

    def findPassByName(self, user):
        try:
            query = f"select password from user where username = '{user}'"
            result = self.fetch_query_one(query)
            self.close_db_connection()
            return result[0]
        except Exception as error:   
            logger.error(f"[User] Error encountered {error}") 
            return 
            
user = User()

def authenticate(user, password):
    try:
        logger.info(f" Inside authenticate with user:{user}")
        obj = User()
        _, usr, passwd,  = obj.findByName(user)   
        if usr and safe_str_cmp(passwd, password):
            logger.info(f" authenticated user:{usr}")
            return usr
    except Exception as error:   
        logger.error(f"[User] Error encountered {error}") 
        return 

def identity(payload):
    try:
        logger.info(f" Inside identity with payload:{payload}")
        obj = User()
        user_id = payload['identity']
        id, _, _, = obj.findByName(user_id)
        return id
    except Exception as error:   
        logger.error(f"[User] Error encountered {error}") 
        return 

