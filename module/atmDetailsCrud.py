from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
from shared.log import logger
from shared.mysqlconnect import ConnectionDB
import collections
import json

class CrudAtmDetails(ConnectionDB):
    def __init__(self):
        ConnectionDB.__init__(self)

    def getlastInsertId(self):
        try:
            query = "select last_insert_id()"
            result = self.fetch_query_one(query)
            return result[0]
        except Exception as error:   
            logger.info(f"[IngDataLoader.getlastInsertId] Error encountered {error}") 
            return

    def insertAtmDetails(self, functionality, type, distance, street, house_no, pin_code, city, lat, lng):
        try:
            insert_query = "insert into atm_details(functionality,type,distance,street,house_no,pin_code,city,lat,lng) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            params = [functionality,type,distance,street,house_no,pin_code,city,lat,lng]
            self.exec_query(insert_query,params)
            return self.getlastInsertId()
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.insertAtmDetails] Error encountered {error}") 
            
    def insertAtmSchedule(self,atm_id,dayOfWeek,hourFrom,hourTo):
        try:
            insert_query = "insert into atm_openinghours(atm_id,dayOfWeek,hourFrom,hourTo) values(%s,%s,%s,%s);"
            params = [atm_id,dayOfWeek,hourFrom,hourTo]
            self.exec_query(insert_query,params)
            return self.getlastInsertId()
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.insertAtmSchedule] Error encountered {error}") 
            return        

    def updateAtmDetails(self, functionality, type, distance, street, house_no, pin_code, city, lat, lng, atmId):
        try:
            update_query = "update atm_details set functionality=%s,type=%s,distance=%s,street=%s,house_no=%s,pin_code=%s,city=%s,lat=%s,lng=%s where id=%s;"
            params = [functionality,type,distance,street,house_no,pin_code,city,lat,lng,atmId]
            self.exec_query(update_query,params)
            return 1
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.updateAtmDetails] Error encountered {error}") 

    def updateAtmSchedule(self,schedule_id,hourFrom,hourTo):
        try:
            update_query = "update atm_openinghours set hourFrom=%s,hourTo=%s where id=%s;)"
            params = [hourFrom,hourTo,schedule_id]
            self.exec_query(update_query,params)
            return 1
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.updateAtmSchedule] Error encountered {error}") 
            return            

    def deleteAtmDetails(self, atmId):
        try:
            delete_query = "delete from atm_details where id =%s;"
            params = [atmId]
            self.exec_query(delete_query,params)
            return 1
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.deleteAtmDetails] Error encountered {error}") 
            return

    def deleteAtmSchedule(self,atm_id,schedule_id=None,dayOfWeek=None):
        try:
            if atm_id is not None:
                delete_query = "delete from atm_openinghours where atm_id=%s;)" 
                params = [atm_id]   
            elif dayOfWeek is None:
                delete_query = "delete from atm_openinghours where id=%s;)"
                params = [schedule_id]
            else:   
                delete_query = "delete from atm_openinghours where id=%s and dayOfWeek=%s;)"
                params = [schedule_id,dayOfWeek]
            self.exec_query(delete_query,params)
            return 1
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.deleteAtmSchedule] Error encountered {error}") 
            return           

    def deleteAtmUsingId(self,atmId):
        try:
            self.deleteAtmSchedule(atmId)    
            self.deleteAtmDetails(atmId)
            return 1
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.deleteAtmUsingId] Error encountered {error}")    

    def selectAtmDetailsWithScheduleUsingId(self, atm_id):
        try:
            query = "select ad.id,ad.functionality,ad.type,ad.distance,ad.street,ad.house_no,ad.pin_code,ad.city,ad.lat,ad.lng,ao.dayOfWeek,ao.hourFrom,ao.hourTo from atm_details ad, atm_openinghours ao where ad.id=ao.atm_id and ad.id= %s;"
            param = [atm_id]
            result = self.fetch_query(query,param)
            return result
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.getAtmDetailsWithScheduleUsingId] Error encountered {error}")             

    def selectAllAtmDetailsWithSchedule(self):
        try:
            query = "select ad.id,ad.functionality,ad.type,ad.distance,ad.street,ad.house_no,ad.pin_code,ad.city,ad.lat,ad.lng,ao.id,ao.dayOfWeek,ao.hourFrom,ao.hourTo from atm_details ad, atm_openinghours ao where ad.id=ao.atm_id limit;"
            result = self.fetch_query(query)
            return result
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.getAllAtmDetailsWithSchedule] Error encountered {error}") 

    def selectAllAtmDetails(self):
        try:
            query = "select ad.id,ad.functionality,ad.type,ad.distance,ad.street,ad.house_no,ad.pin_code,ad.city,ad.lat,ad.lng from atm_details ad;"
            result = self.fetch_query(query)
            return result
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.getAllAtmDetailsWithSchedule] Error encountered {error}") 

    def selectAtmDetailsUsingId(self, atm_id):
        try:
            query = "select ad.id,ad.functionality,ad.type,ad.distance,ad.street,ad.house_no,ad.pin_code,ad.city,ad.lat,ad.lng from atm_details ad where ad.id=%s;"
            params = [atm_id]
            result = self.fetch_query(query,params)
            return result
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.getAtmDetailsUsingId] Error encountered {error}")               

    def getAtmScheduleUsingAtmId(self,atm_id):
        try:
            query = "select id,dayOfWeek,hourFrom,hourTo from atm_openinghours where atm_id=%s order by dayOfWeek;"
            params = [atm_id]
            result = self.fetch_query(query,params)
            return result
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.getAtmSchedule] Error encountered {error}") 
            return   

    def findAtmUsingDtls(self,city,street,house_no,pin_code,lat,lng):
        try:
            query = "select id from atm_details where city=%s and street=%s and house_no=%s and pin_code=%s and lat=%s and lng=%s;"
            params = [city,street,house_no,pin_code,lat,lng]
            result = self.fetch_query_one(query,params)
            if result:
                result = result[0]

            return result
        except Exception as error:   
            logger.error(f"[CrudAtmDetails.getAllAtmDetailsWithSchedule] Error encountered {error}") 


    @logger.catch
    def createDictFromResult(self, atmList):
        try:
            atmJsonlist = []
            for atmDetails in atmList:
                atmDetailJson = collections.OrderedDict()
                atmId, functionality, type, distance, street, house_no, pin_code, city, lat, lng = atmDetails
                atmAddress = {"street": street, "housenumber": house_no, "postalcode": pin_code, "city": city, "geoLocation": { "lat": lat, "lng": lng }}
                atmDetailJson["atmId"] = atmId
                atmDetailJson["address"] = atmAddress
                atmDetailJson["distance"] = distance
                atmDetailJson["functionality"] = functionality
                atmDetailJson["type"] = type  
                atmJsonlist.append(atmDetailJson)

                preDayOfWeek = 0
                daysList = []
                timingsList = []
                resultSchedule = self.getAtmScheduleUsingAtmId(atmId)
                for atmSchedule in resultSchedule:
                    atmScheduleJson = collections.OrderedDict()
                    atmScheduleId, dayOfWeek, hourFrom, hourTo = atmSchedule
                    if dayOfWeek != preDayOfWeek:
                        atmScheduleJson["dayOfWeek"] = dayOfWeek
                    
                    if (dayOfWeek != preDayOfWeek and preDayOfWeek == 0) or dayOfWeek == preDayOfWeek:
                        atmtime = {"atmScheduleId": atmScheduleId, "hourFrom": hourFrom, "hourTo": hourTo} 
                        timingsList.append(atmtime)     
                        atmScheduleJson["hours"] = timingsList
                    else:
                        atmScheduleJson["hours"] = {"atmScheduleId": atmScheduleId, "hourFrom": hourFrom, "hourTo": hourTo}   

                    daysList.append(atmScheduleJson)
                    
                    preDayOfWeek = dayOfWeek       

                atmDetailJson["openingHours"] = daysList

            return atmJsonlist    

        except Exception as error:   
            logger.error(f"[CrudAtmDetails.createDictFromResult] Error encountered {error}") 
            return 

    @logger.catch
    def getAtmList(self):
        try:
            atmList = self.selectAllAtmDetails()
            result = self.createDictFromResult(atmList)
            return json.dumps(result)

        except Exception as error:   
            logger.error(f"[CrudAtmDetails.getAtmList] Error encountered {error}") 
            return 
                                  

def main(operation, atmId, *args):
    try:
        obj = CrudAtmDetails()
        result = None
        if operation == 'getAllAtm':
            result = obj.getAtmList()
        elif operation == 'delAtmRecord':    
            result = obj.deleteAtmDetails(atmId)
        elif operation == 'insertAtmDetails':
            #logger.info(f"args->{args[0]} ")
            functionality, type, distance, street, house_no, pin_code, city, lat, lng = args[0]
            result = obj.insertAtmDetails(functionality, type, distance, street, house_no, pin_code, city, lat, lng)
        elif operation == 'insertAtmSchedule':
            dayOfWeek, hourFrom, hourTo = args[0]
            result = obj.insertAtmSchedule(atmId, dayOfWeek, hourFrom, hourTo)            
        elif operation == 'updateAtmDtls':  
            functionality, type, distance, street, house_no, pin_code, city, lat, lng = args[0] 
            result = obj.updateAtmDetails(functionality, type, distance, street, house_no, pin_code, city, lat, lng, atmId)
        elif operation == 'updateAtmSchedule': 
            schedule_id,hourFrom,hourTo = args[0] 
            result = obj.updateAtmSchedule(schedule_id,hourFrom,hourTo) 
        elif operation == 'findAtmUsingDtls':  
            functionality, type, distance, street, house_no, pin_code, city, lat, lng = args[0]  
            result = obj.findAtmUsingDtls(city,street,house_no,pin_code,lat,lng)
        return result    

    except Exception as error:   
            logger.error(f"[CrudAtmDetails.main] Error encountered {error}") 
            return 

    finally:
        obj.close_db_connection()         


if __name__ == '__main__':
    obj = CrudAtmDetails()
    result =obj.getAtmList()
    #result = obj.createDictFromResult([(1, 'Geldautomaat', 'GELDMAAT', 0, 'Kastelenstraat', '70', '1083 CD', 'Amsterdam', 52.326288, 4.883155)])
    print(json.dumps(result))

