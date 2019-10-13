import mysql.connector
from mysql.connector import Error
import pg

from datetime import date

def main():
      getItemStore(1)

def getItemStore(IdStore):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getItemStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()
      
def getEmployeeStore(IdStore):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getEmployeeStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()
      
def getPromoStore(IdStore):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getPromoStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()

