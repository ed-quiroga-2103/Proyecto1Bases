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
                        query += "WHERE IdPerson = " + str(newEmployee[1]) + ";"

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
      fragItems(idStore)
      fragPerson(idStore)
      fragJob(idStore)
      fragEmployeeStore(idStore)
      fragItemStore(idStore)

      return 1

def getItemsWarehouse():

      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = connection.query("SELECT IdItem FROM ItemWarehouse WHERE Quantity = 0;")

      ids = []

      connection.close()

      for line in data:
            ids.append(line[0])

      return ids

def generateWarehouseRequest():

      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = getItemsWarehouse()


      idRequest = connection.query("SELECT IdRequest FROM WarehouseRequest ORDER BY IdRequest DESC;")

      try:

        idRequest = idRequest[0][0] + 1 

      except:

        idRequest = 1

      today = date.today()
      requestDate = today.strftime("%Y-%m-%d")


      connection.query("INSERT INTO WarehouseRequest VALUES " + str( (idRequest, requestDate) ) + ";")


      for i in data:

            query = "INSERT INTO WarehouseRequestItem VALUES "

            query += str( (idRequest, i, 1) ) + ";"

            connection.query(query)

      connection.close()

      restockWarehouse(data)

def restockWarehouse(idList):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')



      for i in idList:

            query = "UPDATE ItemWarehouse SET Quantity = 25 WHERE IdItem = " + str(i) + ";"

            connection.query(query)

      connection.close()
            
def getStockFromWarehouse(idItem):

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')


    data = connection.query("SELECT Quantity FROM ItemWarehouse WHERE IdItem = " + str(idItem) + ";")

    connection.close()

    return data[0][0]

def getItemsForRestock():

      query = "SELECT IdRequest, IdItem, Quantity FROM StoreRequestItem WHERE Status = 0 ORDER BY IdRequest;"

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      return connection.query(query)

def updateWarehouseStock(idItem, newStock):

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      query = "UPDATE ItemWarehouse SET Quantity = " + str(newStock)
      query += "WHERE IdItem = " + str(idItem) + ";" 

      connection.query(query)

      connection.close()

def restockStores():

      items = getItemsForRestock()

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      for item in items:

            idStore = getStoreFromRequest(item[0])
            
            stock = getStockFromWarehouse(item[1])

            needed = item[2]

            newValue = 0

            if stock > needed:
                  newValue = needed + getItemStock(item[1], idStore)
                  stock -= needed

                  updateWarehouseStock(item[1], stock)
                  query = "UPDATE StoreRequestItem SET Status = 1 WHERE IdItem = " + str(item[1]) 
                  query += " AND IdRequest = " + str(item[0]) + ";" 
                  connection.query(query)

            else:
                  newValue = stock + getItemStock(item[1], idStore)
                  updateWarehouseStock(item[1], 0)

                  needed -= stock

                  query = "UPDATE StoreRequestItem SET Quantity = " + str(needed)
                  query += " WHERE IdItem = " + str(item[1]) + " AND IdRequest = " + str(item[0]) + ";"

                  connection.query(query)

            query = "UPDATE ItemStore SET Quantity = " + str(newValue)

            query += " WHERE IdStore = " + str(idStore)
            query += " AND IdItem = " + str(item[1]) + ";"
            connection.query(query)


def getStoreFromRequest(idRequest):

      query = "SELECT IdStore FROM StoreRequest WHERE IdRequest = " + str(idRequest) + ";"
      
      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query(query)

      return data[0][0]

def getItemStock(idItem, idStore):

      query = "SELECT Quantity FROM ItemStore WHERE IdStore = " + str(idStore) + " "
      query += "AND IdItem = " + str(idItem) + ";"

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

      data = connection.query(query)

      return data[0][0]


def ConsultEmployee(IdEmpleado):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM ConsultEmployee(" + str(IdEmpleado) + ");"

      print( connection.query(query))

      connection.close()

def ConsultStore(IdStore):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM ConsultStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()

def InsertEmployee(Name,  MiddleName, LastName, IdentityDoc, IdAddress, Status, IdJob, IdStore, HireDate):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertEmployee"
      cuerpo = str(Name) , str(MiddleName),  str(LastName) , str(IdentityDoc),IdAddress, Status,IdJob,IdStore,str(HireDate)
      final = encabezado + str(cuerpo) + ";"
      
      print( connection.query(str(final)))

      connection.close()

      connection = mysql.connector.connect(host='localhost',
                                          database= db + str(IdStore),
                                          user='root',
                                          password='root')
      cursor = connection.cursor()

      cursor.execute("SELECT IdPerson FROM Person ORDER BY IdPerson DESC LIMIT 1;")
      data = cursor.fetchall()

      query = "INSERT INTO Person VALUES "
      query += str((data[0][0] +1, Name, MiddleName, LastName, IdentityDoc, IdAddress)) + ";"

      print(query)

      cursor.execute(query)

      connection.commit()
      connection.close()

def InsertPromo(newIdStore, newIdItem , newInitialDateTime , newFinalDateTime , newPorcentage ):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertPromo"
      cuerpo = newIdStore , newIdItem, str(newInitialDateTime), str(newFinalDateTime),newPorcentage
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()

def InsertStore(Code , IdAddress , Status , IdAdmin ):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertStore"
      cuerpo = Code , IdAddress, Status, IdAdmin
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()  

def ModifyEmployee(Id, Status):
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyEmpoyee"
      cuerpo = Id, Status
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()
      
def ModifyEmployeePerson(Id , newName ,  newMiddleName , newLastName , newIdentityDoc , newIdAddress ) :
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyEmployeePerson"
      cuerpo = Id, str(newName), str(newMiddleName), str(newLastName), str(newIdentityDoc),newIdAddress
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()

def ModifyStore(newid , newcode , newidaddress , newstatus , newidadmin )  :
      connection = pg.DB(dbname='testpsql', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyStore"
      cuerpo = newid, newcode, newidaddress, newstatus, newidadmin
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()
