from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
from shared.log import logger
from shared.mysqlconnect import ConnectionDB
from shared.httpClient import httpClient
import json
#import requests

class IngDataLoader(ConnectionDB):
    def __init__(self):
        ConnectionDB.__init__(self)

    @logger.catch
    def retriveIngAtmDataFromUrl(self,url):
        """ Retrives the ING ATM details json from a given URL """    
        try:
            logger.info("Retriving the atm data from the url")
            # Fetching the json data from the get api provided
            result = httpClient('get',url,None,{'Content-Type': 'application/json'},60)      
            result = json.loads(result)
            # Bad json object needs correcton. Correcting at this end
            with open('atms.json','w',encoding = 'utf-8') as file:
                file.writelines(json.dumps(result["data"][5:]))
            logger.info("Completed retriving the atm data from the url")    
            return

        except Exception as error:   
            logger.info(f"[IngDataLoader.retriveIngAtmDataFromUrl] Error encountered {error}")  
            return  

    def insertAtmDetails(self, functionality, type, distance, street, house_no, pin_code, city, lat, lng):
        try:
            insert_query = "insert ignore into atm_details(functionality,type,distance,street,house_no,pin_code,city,lat,lng) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            params = [functionality,type,distance,street,house_no,pin_code,city,lat,lng]
            self.exec_query(insert_query,params)
            return self.getlastInsertId()
        except Exception as error:   
            logger.error(f"[IngDataLoader.insertAtmDetails] Error encountered {error}")         

    def insertAtmSchedule(self,atm_id,dayOfWeek,hourFrom,hourTo):
        try:
            insert_query = "insert ignore into atm_openinghours(atm_id,dayOfWeek,hourFrom,hourTo) values(%s,%s,%s,%s);"
            params = [atm_id,dayOfWeek,hourFrom,hourTo]
            self.exec_query(insert_query,params)
            return
        except Exception as error:   
            logger.error(f"[IngDataLoader.insertAtmSchedule] Error encountered {error}") 
            return

    def getlastInsertId(self):
        try:
            query = "select last_insert_id()"
            result = self.fetch_query_one(query)
            return result[0]
        except Exception as error:   
            logger.info(f"[IngDataLoader.getlastInsertId] Error encountered {error}") 
            return


    @logger.catch
    def loadDataIntoTables(self):
        """ Loads the data into database tables """
        try:
            logger.info("[IngDataLoader.loadDataIntoTables] Performing load of the atm details in db")
            # Get the details from the json
            with open('atms.json','r') as file:
                atmDetailsJson = json.load(file)
                # For each atm item in the list of atms, get the details
                logger.info("[IngDataLoader.loadDataIntoTables] Reading the atm details from the file and processing each atm")
                for item in json.loads(atmDetailsJson):
                    street = item.get("address")["street"]
                    housenumber = item.get("address")["housenumber"]
                    postalcode = item.get("address")["postalcode"]
                    city = item.get("address")["city"]
                    geoLocation = item.get("address")["geoLocation"]
                    distance = item.get("distance")
                    openingHours = item.get("openingHours")
                    functionality = item.get("functionality")
                    type = item.get("type")

                    # Cleanup data issues
                    street = street.replace("'", " ")
                    city = city.replace("'", " ")

                    # Insert into atm_details
                    atmId = self.insertAtmDetails(functionality, type, distance, street, housenumber, postalcode, city, geoLocation["lat"], geoLocation["lng"])
                    if atmId is None:
                        logger.info("[IngDataLoader.loadDataIntoTables] Last insert id not found")
                        logger.error("[IngDataLoader.loadDataIntoTables] Last insert id not found")
                        break

                    # Insert into atm_openinghours
                    for days in openingHours:
                        dayOfWeek = days.get("dayOfWeek")
                        for hours in days.get("hours"):
                            hourFrom = hours.get("hourFrom")
                            hourTo = hours.get("hourTo")
                            self.insertAtmSchedule(atmId,dayOfWeek,hourFrom,hourTo)

            logger.info("[IngDataLoader.loadDataIntoTables] Completed inserting the atm details in the tables")            

        except Exception as error:   
            logger.info(f"[IngDataLoader.loadDataIntoTables] Error encountered {error}")    

def main(url):
    try:
        obj = IngDataLoader()
        obj.retriveIngAtmDataFromUrl(url)
        obj.loadDataIntoTables()
        return 1

    except Exception as error:   
        logger.info(f"[IngDataLoader.main] Error encountered {error}") 
        return

    finally:
        obj.close_db_connection()     



if __name__ == '__main__':
    obj = IngDataLoader()
    #obj.retriveIngAtmDataFromUrl('https://www.ing.nl/api/locator/atms/')
    obj.loadDataIntoTables()
    obj.close_db_connection()