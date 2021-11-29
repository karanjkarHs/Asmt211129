from sys import path
from pathlib import Path
path.append(str(Path(__file__).resolve().parent.parent))
from module.atmDetailsCrud import main as ingAtmCrud
from flask_restful import Resource, reqparse
from flask_jwt import  jwt_required
from shared.log import logger
from flask import request
import json
from module.ingAtmDataLoad import main as dataLoader

class ListAllAtm(Resource):
    @jwt_required()
    def get(self):
        try:
            logger.info("[IngAtmService.get] get request")
            result = ingAtmCrud('getAllAtm', None, None)
            print(result)
            return result, 200 if result else 404

        except Exception as error:   
            logger.error(f"[IngAtmService.get] Error encountered {error}") 
            return

class AddUpdateAtm(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("atmJson",type=str,required=True,help="Input Json cannot be None")
    parser.add_argument("action",type=str,required=True,help="action str cannot be None")

    @jwt_required()
    def post(self):
        try:
            logger.info("[IngAtmService.post] post request")
            # Get the json from user as a list of atms    
            request_data = AddUpdateAtm.parser.parse_args()
            request_data = request.get_json()
            atmJson = str(request_data['atmJson']).replace("'",'"')
            action = str(request_data['action'])
            
            atmJson = json.loads(atmJson)
            # For each atm process it
            for item in atmJson:
                street = item.get("address")["street"]
                housenumber = item.get("address")["housenumber"]
                postalcode = item.get("address")["postalcode"]
                city = item.get("address")["city"]
                geoLocation = item.get("address")["geoLocation"]
                distance = item.get("distance")
                functionality = item.get("functionality")
                type = item.get("type")     
                openingHours = item.get("openingHours")

                if action == "insert":
                    # Check if the record already exist. If exist the continue with next
                    result = ingAtmCrud('findAtmUsingDtls', None, [functionality, type, distance, street, housenumber, postalcode, city, geoLocation["lat"], geoLocation["lng"]])
                    if result:
                        continue
                    # Insert atm general details     
                    result = ingAtmCrud('insertAtmDetails', None, [functionality, type, distance, street, housenumber, postalcode, city, geoLocation["lat"], geoLocation["lng"]]) 
                    atmId = result

                    # Insert atm operational hours
                    for days in openingHours:
                        dayOfWeek = days.get("dayOfWeek")
                        for hours in days.get("hours"):
                            hourFrom = hours.get("hourFrom")
                            hourTo = hours.get("hourTo")
                            ingAtmCrud('insertAtmSchedule', atmId, [dayOfWeek, hourFrom, hourTo])  

                elif action == "update":    
                    atmId = item.get("atmId")       
                    # Update the atm details record with the given atm id
                    result = ingAtmCrud('updateAtmDtls', atmId, [functionality, type, distance, street, housenumber, postalcode, city, geoLocation["lat"], geoLocation["lng"]])                  

            return result, 200 if result else 404            
        
        except Exception as error:   
            logger.error(f"[IngAtmService.post] Error encountered {error}") 
            return 404

class RemoveAtm(Resource):
    @jwt_required()
    def delete(self, atmId):
        try:
            logger.info("[IngAtmService.delete] delete request")
            result = ingAtmCrud('delAtmRecord',atmId,None)
            return result, 200 if result else 404     

        except Exception as error:   
            logger.error(f"[IngAtmService.delete] Error encountered {error}") 
            return 

class LoadAtmData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("url",type=str,required=True,help="url cannot be None")   
    
    @jwt_required()
    def post(self):
        try:
            logger.info("[IngAtmService.LoadAtmData] post request")
            request_data = LoadAtmData.parser.parse_args()
            request_data = request.get_json()
            url = str(request_data['url']).replace("'",'"')     
            result = dataLoader(url)
            return result, 200 if result else 404     

        except Exception as error:   
            logger.error(f"[IngAtmService.LoadAtmData] Error encountered {error}") 
            return     
