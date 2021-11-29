README

Brief Description

Data Model

Tables:- 
1. atm_details
2. atm_openinghours

Table atm_details has one to many relationship with atm_openinghours


Atm Data loading :
    • This will retrieve the data which is in the form of Json and load it into the tables.
    • Rest api is provided to perform this action.
    • Noted a invalid line in the json and is corrected vi a the code block. Remove in case of clean json at the url provided.
    • Any bulk import of the atm data can be done using this
    • In case if same json data is feed to the api, it wont result in adding duplicates. Only new records will be added.

Create/ Update / Delete / Read data:
    • Following operations are supported via rest apis
    • 1. User can retrieve all atm records
    • 2. User can add single or multiple atm records.  Duplicated will not be added and will not result in error and ignored.
    • 3. User can delete a record using record id.
    • 4. User can update single or multiple atm records, using record ids.



Rest Api’s

authentication:
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "username": "user1" ,
  "password": "password1"
}' \
 'http://192.168.1.141:5000/auth'








Load Data:
curl -i -X POST \
   -H "Authorization:JWT token_key" \
   -H "Content-Type:application/json" \
   -d \
'{
  "url":"https://www.ing.nl/api/locator/atms/"
}  ' \
 'http://192.168.1.141:5000/loadAtmData'


Get ATM list:
curl -i -X GET \
   -H "Authorization:JWT token_key" \
 'http://192.168.1.141:5000/listAllAtm'


Insert ATMs:
curl -i -X POST \
   -H "Authorization:JWT token_key" \
   -H "Content-Type:application/json" \
   -d \
'{
  "action":"insert","atmJson": [{"atmId":6857,"address":{"street":"newStreet345","housenumber":"24","postalcode":"5341 DG","city":"Oss","geoLocation":{"lat":"51.770457","lng":"5.524862"}},"distance":0,"openingHours":[{"dayOfWeek":2,"hours":[{"hourFrom":"13:00","hourTo":"21:31"}]},{"dayOfWeek":3,"hours":[{"hourFrom":"09:00","hourTo":"17:30"}]},{"dayOfWeek":4,"hours":[{"hourFrom":"09:00","hourTo":"17:30"}]},{"dayOfWeek":5,"hours":[{"hourFrom":"09:00","hourTo":"21:00"}]},{"dayOfWeek":6,"hours":[{"hourFrom":"09:00","hourTo":"17:30"}]},{"dayOfWeek":7,"hours":[{"hourFrom":"09:00","hourTo":"17:00"}]},{"dayOfWeek":1,"hours":[]}],"functionality":"xxxxxxxxxxxx","type":"xxxxxxxxxx"}]
}' \
 'http://192.168.1.141:5000/addUpdateAtm'



Update ATMs:
curl -i -X POST \
   -H "Authorization:JWT token_key" \
   -H "Content-Type:application/json" \
   -d \
'{
  "action":"update","atmJson": [{"atmId":6857,"address":{"street":"newStreet345","housenumber":"24","postalcode":"5341 DG","city":"Oss","geoLocation":{"lat":"51.770457","lng":"5.524862"}},"distance":0,"openingHours":[{"dayOfWeek":2,"hours":[{"hourFrom":"13:00","hourTo":"21:31"}]},{"dayOfWeek":3,"hours":[{"hourFrom":"09:00","hourTo":"17:30"}]},{"dayOfWeek":4,"hours":[{"hourFrom":"09:00","hourTo":"17:30"}]},{"dayOfWeek":5,"hours":[{"hourFrom":"09:00","hourTo":"21:00"}]},{"dayOfWeek":6,"hours":[{"hourFrom":"09:00","hourTo":"17:30"}]},{"dayOfWeek":7,"hours":[{"hourFrom":"09:00","hourTo":"17:00"}]},{"dayOfWeek":1,"hours":[]}],"functionality":"xxxxxxxxxxxx","type":"xxxxxxxxxx"}]
}' \
 'http://192.168.1.141:5000/addUpdateAtm'


Delete ATM:
curl -i -X DELETE \
   -H "Authorization:JWT token_key" \
 'http://192.168.1.141:5000/deleteAtm/6856'





INSTRUCTIONS


PREREQUSITES

USE LOCAL MYSQL DB INSTANCE (port-3306) OR use DOCKER as mentioned below 
yum install docker
docker pull mysql
docker image ls
docker container run -p 3307:3306 --name mysql -e MYSQL_ROOT_PASSWORD=root -d mysql
Python3+, flask, flask-restful, aiohttp, Flask-JWT, loguru, etc

Log into the DB and run below

mysql -uroot -proot -h127.0.0.1 -p3306
create database demo;

use demo;

create table atm_details(
id int not null auto_increment,
customer_code varchar(4) Default 'ING',
functionality varchar(256),
type varchar(64),
distance int,
street varchar(128),
house_no varchar(128),
pin_code varchar(128),
city varchar(128),
lat DOUBLE,
lng DOUBLE, 
primary key(id),
unique index(city,street,house_no,pin_code,lat,lng)
);

create table atm_openinghours(
id int not null auto_increment,
atm_id int,
dayOfWeek int,
hourFrom varchar(64),
hourTo varchar(64), 
primary key(id),
foreign key(atm_id) references atm_details(id) ON DELETE CASCADE ON UPDATE CASCADE,
unique index(atm_id,dayOfWeek,hourFrom,hourTo)
);

create table user(
id int not null auto_increment,
username varchar(64),
password varchar(64), 
primary key(id)
);
insert into user(username,password) values('user1','password1');


Download the directory in any path on the filesystem

Run app.py
python app.py >> app.log 2>&1 &
