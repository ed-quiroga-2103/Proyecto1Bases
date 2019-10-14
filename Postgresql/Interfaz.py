import mysql.connector
from mysql.connector import Error
import pg

from datetime import date

db = "Test"

def main():
      getItemStore(1)

def getItemStore(IdStore):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getItemStore(" + str(IdStore) + ");"

      data = connection.query(query)

      connection.close()
      
      try:
            test = data[0][0]

            return data

      except:

            return -1

def fragItemStore(idStore):

      items = getItemStore(idStore)

      if items == -1:
            return

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      cursor.execute("SELECT IdItem FROM ItemStore;")

      currentItems = cursor.fetchall()


      for newItem in items:
            exists = False
            for item in currentItems:
                  if newItem[0] == item[0]:
                        exists = True

                        query = "UPDATE ItemStore SET Quantity = "
                        query += str(newItem[1]) + " "
                        query += "WHERE IdItem = " + str(newItem[0]) + ";"

                        cursor.execute(query)
                  
                        connection.commit()
                        break
            if not exists:
                  exists = False
                  
                  cursor.execute("INSERT INTO ItemStore VALUES (%s,%s);", newItem)
                  connection.commit()
            
def getEmployeeStore(IdStore):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getEmployeeStore(" + str(IdStore) + ");"

      data = connection.query(query)

      connection.close()
      
      try:
            test = data[0][0]

            return data

      except:

            return -1

def fragEmployeeStore(idStore):
      

      newEmployees = getEmployeeStore(idStore)

      if newEmployees == -1:
            return

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      cursor.execute("SELECT IdPerson FROM Employee;")

      currentEmployee = cursor.fetchall()


      for newEmployee in newEmployees:
            exists = False
            for employee in currentEmployee:
                  if newEmployee[0] == employee[0]:
                        exists = True

                        query = "UPDATE EmployeeJob SET IdJob = "
                        query += str(newEmployee[0]) + " "
                        query += "WHERE IdItem = " + str(newEmployee[1]) + ";"

                        cursor.execute(query)
                  
                        connection.commit()
                        break

            if not exists:
                  exists = False

                  empData = (newEmployee[1], 1)

                  cursor.execute("INSERT INTO Employee VALUES (%s,%s);", empData)
                  connection.commit()
                  cursor.execute("INSERT INTO EmployeeJob VALUES (%s,%s,%s);", newEmployee)
                  connection.commit()
            
def getPromoStore(IdStore):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getPromoStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()

def fragItems(idStore):
      fragCategory(idStore)
      fragBrand(idStore)

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query("SELECT * FROM Item;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      for line in data:
            query = "INSERT INTO Item VALUES "
            
           
            query += str( line ) + ";"
            
            
            cursor.execute(query)

      connection.commit()

      connection.close()

def fragPerson(idStore):

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query("SELECT * FROM Person;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      for line in data:
            query = "INSERT INTO Person (IdPerson, FirstName, MiddleName, LastName, IdentityDoc, IdAddress) VALUES "
            
            if str(line[2]) == "None":
                  query += "(" + str(line[0]) + ", '" + str(line[1]) + "', NULL, '" + str(line[3]) + "', '"
                  query += str(line[4]) + "', " + str(line[5]) + ");"
            else:
                  query += str( (line[0], line[1], line[2], line[3], line[4], line[5]) ) + ";"
            
            
            cursor.execute(query)

      connection.commit()

      connection.close()

def fragJob(idStore):

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query("SELECT * FROM Job;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                    database=db + str(idStore),
                                    user='root',
                                    password='root')
      cursor = connection.cursor()
      
      for line in data:

            query  = "INSERT INTO Job (IdJob, Job, Salary) VALUES "
            query += str( (line[0], line[1], line[2]) ) + ";"

            cursor.execute(query)

            connection.commit()

      connection.close()

def fragCountry(idStore):

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query("SELECT * FROM Country;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                    database=db + str(idStore),
                                    user='root',
                                    password='root')
      cursor = connection.cursor()

      for line in data:

            query  = "INSERT INTO Country (IdCountry, Name) VALUES "
            query += str( (line[0], line[1]) ) + ";"

            cursor.execute(query)

      connection.commit()

      connection.close()

def fragState(idStore):

      connection = pg.DB(host='localhost',
                  user='root',
                  passwd='root',
                  dbname='testpsql')

      data = connection.query("SELECT * FROM State;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                              database=db + str(idStore),
                              user='root',
                              password='root')
      cursor = connection.cursor()

      for line in data:

            query  = "INSERT INTO State (IdState, IdCountry, Name) VALUES "
            query += str( line ) + ";"
            
            cursor.execute(query)

      connection.commit()

      connection.close()

def fragCity(idStore):

      connection = pg.DB(host='localhost',
                  user='root',
                  passwd='root',
                  dbname='testpsql')

      data = connection.query("SELECT * FROM City;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                              database=db + str(idStore),
                              user='root',
                              password='root')
      cursor = connection.cursor()

      for line in data:

            query  = "INSERT INTO City VALUES "
            query += str( line ) + ";"
            
            cursor.execute(query)

      connection.commit()

      connection.close()

def fragAddress(idStore):

      fragCountry(idStore)
      fragState(idStore)
      fragCity(idStore)

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query("SELECT * FROM Address;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                    database=db + str(idStore),
                                    user='root',
                                    password='root')

      cursor = connection.cursor()

      for line in data:

            query  = "INSERT INTO Address VALUES "
            query += str( line ) + ";"
            
            cursor.execute(query)

      connection.commit()

      connection.close()

def fragCategory(idStore):

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query("SELECT * FROM Category;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                    database=db + str(idStore),
                                    user='root',
                                    password='root')

      cursor = connection.cursor()

      for line in data:

            query  = "INSERT INTO Category VALUES "
            query += str( line ) + ";"
            
            cursor.execute(query)

      connection.commit()

      connection.close()

def fragBrand(idStore):

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query("SELECT * FROM Brand;")

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                    database=db + str(idStore),
                                    user='root',
                                    password='root')

      cursor = connection.cursor()

      for line in data:

            query  = "INSERT INTO Brand VALUES "
            query += str( line ) + ";"
            
            cursor.execute(query)

      connection.commit()

      connection.close()

def initStore(idStore):

      connection = mysql.connector.connect(host='localhost',
                                    user='root',
                                    password='root')

      cursor = connection.cursor()

      cursor.execute("CREATE DATABASE Test"+str(idStore)+";")

      file = open("MySQL/StoreScript.sql")

      query = "USE Test"+str(idStore) + ";\n" + "\n".join(file.readlines())

      file.close()

      cursor.execute(query)

      connection.close()



      fragAddress(idStore)
      fragBrand(idStore)
      fragCategory(idStore)
      fragItems(idStore)
      fragPerson(idStore)
      fragJob(idStore)

      return 1

