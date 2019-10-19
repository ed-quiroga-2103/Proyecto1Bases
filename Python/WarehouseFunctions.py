import mysql.connector
from mysql.connector import Error
import pg
import StoreFunctions
import random
from datetime import date

db = "Store"

def getItemStore(IdStore):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getItemStore(" + str(IdStore) + ");"

      data = connection.query(query)

      connection.close()
      
      try:
            test = data[0][0]

            return data

      except:

            return -1

def getAllCustomers():
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = connection.query("SELECT * FROM Customer;")
      return data

def fragCustomers(idStore):

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      data = getAllCustomers()

      for customer in data:
            query = "INSERT INTO Customer VALUES "
            query += str(customer) + ";"

            cursor.execute(query)

      connection.commit()

      connection.close()

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
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
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
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM getPromoStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()

def fragItems(idStore):
      fragCategory(idStore)
      fragBrand(idStore)

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

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
                        dbname='datawarehouse')

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
                        dbname='datawarehouse')

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
                        dbname='datawarehouse')

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
                  dbname='datawarehouse')

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
                  dbname='datawarehouse')

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
                        dbname='datawarehouse')

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
                        dbname='datawarehouse')

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
                        dbname='datawarehouse')

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

      cursor.execute("CREATE DATABASE Store"+str(idStore)+";")

      file = open("MySQL/StoreScript.sql")

      query = "USE Store"+str(idStore) + ";\n" + "\n".join(file.readlines())

      file.close()

      cursor.execute(query)

      connection.close()



      fragAddress(idStore)
      fragItems(idStore)
      fragPerson(idStore)
      fragJob(idStore)
      fragEmployeeStore(idStore)
      fragItemStore(idStore)
      fragCustomers(idStore)

      return 1

def getItemsWarehouse():

      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = connection.query("SELECT IdItem FROM ItemWarehouse WHERE Quantity = 0;")

      ids = []

      connection.close()

      for line in data:
            ids.append(line[0])

      return ids

def generateWarehouseRequest():

      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = getItemsWarehouse()

      if data == []:
            return

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
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')



      for i in idList:

            query = "UPDATE ItemWarehouse SET Quantity = 25 WHERE IdItem = " + str(i) + ";"

            connection.query(query)

      connection.close()
            
def getStockFromWarehouse(idItem):

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')


    data = connection.query("SELECT Quantity FROM ItemWarehouse WHERE IdItem = " + str(idItem) + ";")

    connection.close()

    return data[0][0]

def getItemsForRestock():

      query = "SELECT IdRequest, IdItem, Quantity FROM StoreRequestItem WHERE Status = 0 ORDER BY IdRequest;"

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

      return connection.query(query)

def updateWarehouseStock(idItem, newStock):

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

      query = "UPDATE ItemWarehouse SET Quantity = " + str(newStock)
      query += "WHERE IdItem = " + str(idItem) + ";" 

      connection.query(query)

      connection.close()

def restockStores():

      items = getItemsForRestock()

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

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
            
            elif stock == -1:
                  #The item is discontinued
                  continue
            
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
                        dbname='datawarehouse')

      data = connection.query(query)

      return data[0][0]

def getItemStock(idItem, idStore):

      query = "SELECT ItemStore.Quantity FROM ItemStore INNER JOIN Item ON Item.IdItem =  ItemStore.IdItem "
      query += "WHERE Item.Status = 1 AND ItemStore.IdStore = " + str(idStore) + " "
      query += "AND ItemStore.IdItem = " + str(idItem) + ";"

      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

      data = connection.query(query)

      try:
            return data[0][0]
      
      except:
            return -1

def ConsultEmployee(IdEmpleado):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM ConsultEmployee(" + str(IdEmpleado) + ");"

      print( connection.query(query))

      connection.close()

def ConsultStore(IdStore):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM ConsultStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()

def InsertEmployeePerson(Name,  MiddleName, LastName, IdentityDoc, IdAddress, Status, IdJob, IdStore, HireDate):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertEmployee"
      cuerpo = str(Name) , str(MiddleName),  str(LastName) , str(IdentityDoc),IdAddress, Status,IdJob,IdStore,str(HireDate)
      final = encabezado + str(cuerpo) + ";"
      
      print( connection.query(str(final)))

      connection.close()
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = connection.query("SELECT IdPerson FROM Person ORDER BY IdPerson DESC LIMIT 1;")

      connection = mysql.connector.connect(host='localhost',
                                          database= db + str(IdStore),
                                          user='root',
                                          password='root')
      cursor = connection.cursor()

      

      query = "INSERT INTO Person VALUES "
      query += str((data[0][0], Name, MiddleName, LastName, IdentityDoc, IdAddress)) + ";"

      print(query)

      cursor.execute(query)

      connection.commit()
      connection.close()

def InsertPromo(newIdStore, newIdItem , newInitialDateTime , newFinalDateTime , newPorcentage ):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertPromo"
      cuerpo = newIdStore , newIdItem, str(newInitialDateTime), str(newFinalDateTime),newPorcentage
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()

def InsertStore(Code , IdAddress , Status , IdAdmin ):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertStore"
      cuerpo = Code , IdAddress, Status, IdAdmin
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()  

def ModifyEmployee(Id, Status):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyEmpoyee"
      cuerpo = Id, Status
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()
      
def ModifyEmployeePerson(Id , newName ,  newMiddleName , newLastName , newIdentityDoc , newIdAddress ) :
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyEmployeePerson"
      cuerpo = Id, str(newName), str(newMiddleName), str(newLastName), str(newIdentityDoc),newIdAddress
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()

def ModifyStore(newid , newcode , newidaddress , newstatus , newidadmin )  :
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyStore"
      cuerpo = newid, newcode, newidaddress, newstatus, newidadmin
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()

def ModifyItemStatus(id, status):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "SELECT * FROM ModifyStatusItem(" + str(id) + "," + str(status) + ");"

      connection.query(query)

# ----------------------------- Store Creation process ----------------------------------

def CreateStore():
      idStore = getNextStore()
      initStore(idStore)
      newEmployees = getNewEmployees()
      idAdmin = assignEmployees(idStore,newEmployees)
      
      idAddress = random.choice(range(1050)) + 1 
      InsertStore(idStore, idAddress, 1, idAdmin)

      updateWarehouseEmployees(idStore)

      updateStoreEmployeeTable(idStore, newEmployees)
      updateWarehouseEmployeeTable(newEmployees)
      fragCustomers(idStore)

def getNewEmployees():
      query = "SELECT P.IdPerson FROM Person P WHERE P.IdPerson NOT IN (SELECT EJ.IdPerson FROM EmployeeJob EJ);"

      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = connection.query(query)

      newEmployees = []

      connection.close()

      for i in range(10):
            
            choice = random.choice(data)

            while choice[0] in newEmployees:
                  
                  choice = random.choice(data)

            newEmployees.append(choice[0])

      return newEmployees

def assignEmployees(idStore, newEmployees):
      idAdmin = random.choice(newEmployees)

      newEmployees.remove(idAdmin)

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      for employee in newEmployees:

            idJob = random.choice(range(1,5))+1
            today = date.today()
            hireDate = today.strftime("%Y-%m-%d")

            query = "INSERT INTO EmployeeJob VALUES "
            query += str( (idJob, employee, hireDate) ) + ";"

            cursor.execute(query)
      connection.commit()

      connection.close()

      assignAdmin(idStore, idAdmin, hireDate)

      return idAdmin

def assignAdmin(idStore,idAdmin, hireDate):

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      query = "INSERT INTO EmployeeJob VALUES " 
      query += str( (1, idAdmin, hireDate) ) + ";"
      cursor.execute(query)
      connection.commit()

      connection.close()
      
def getNextStore():

      query = "SELECT IdStore FROM Store ORDER BY IdStore DESC LIMIT 1;"

      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = connection.query(query)

      idStore = data[0][0]

      return idStore + 1

def updateWarehouseEmployees(idStore):
      connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')      
      data = getStoreEmployees(idStore)

      for employee in data:
            
            query = "INSERT INTO EmployeeJob VALUES "
            query += str( (employee[0], employee[1], idStore, employee[2].strftime("%Y-%m-%d")) ) + ";"

            connection.query(query)

def getStoreEmployees(idStore):

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      cursor.execute("SELECT * FROM EmployeeJob;")

      data = cursor.fetchall()

      connection.close()

      return data

def updateStoreEmployeeTable(idStore, idList):
      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      for id in idList:

            query = "INSERT INTO Employee VALUES "
            query += str( (id, 1) ) + ";"

            cursor.execute(query)

      connection.commit()

def updateWarehouseEmployeeTable(idList):
      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      for id in idList:

            query = "INSERT INTO Employee VALUES "
            query += str( (id, 1) ) + ";"

            connectionpsql.query(query)

def getIdStoreList():
      query = "SELECT IdStore FROM Store;"

      idList = []
      
      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      data = connectionpsql.query(query)

      for line in data:
            idList.append(line[0])

      return idList

# -------------------------------------------------------------------------------------------

def InsertItem(idBrand, description, idCategory, price, stores):
      idItem = code = getNextItem()

      today = date.today()
      entryDate = today.strftime("%Y-%m-%d")

      query = "INSERT INTO Item VALUES "
      query += str( (idItem,code,idBrand,description,idCategory,price,1,entryDate) ) + ";"

      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      connectionpsql.query(query)

      connectionpsql.close()

      storeIds = getIdStoreList()

      for id in storeIds:
            try:
                  insertItemStore(query, id)
            except:
                  continue
      for id in stores:
            try:
                  insertWithCeroStock(idItem, id)
                  insertWithCeroStockToStore(idItem, id)
            except:
                  continue

      insertWithCeroStockToWarehouse(idItem)

def insertItemStore(query, idStore):

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      cursor.execute(query)
      connection.commit()
      connection.close()

def insertWithCeroStock(idItem, idStore):
      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "INSERT INTO ItemStore VALUES "
      query += str( (idStore,idItem,0) ) + ";"

      connectionpsql.query(query)

def insertWithCeroStockToWarehouse(idItem):
      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "INSERT INTO ItemWarehouse VALUES "
      query += str( (idItem,0) ) + ";"

      connectionpsql.query(query)

      connectionpsql.close()

def insertWithCeroStockToStore(idItem,idStore):
      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      query = "INSERT INTO ItemStore VALUES "
      query += str( (idItem, 0) ) + ";"
      cursor.execute(query)
      print(query)
      connection.commit()

def getNextItem():

      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "SELECT IdItem FROM Item ORDER BY IdItem DESC LIMIT 1;"

      data = connectionpsql.query(query)

      try:
            return data[0][0] + 1
      except:
            return 1

def deactivateItem(idItem):

      query = "UPDATE Item SET Status = 0 WHERE IdItem = " + str(idItem) + ";"

      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      connectionpsql.query(query)

      connectionpsql.close()

      storeList = getIdStoreList()

      for i in storeList:
            try:
                  connection = mysql.connector.connect(host='localhost',
                                                database=db + str(i),
                                                user='root',
                                                password='root')

                  cursor = connection.cursor()

                  cursor.execute(query)

                  connection.commit()
                  connection.close()

            except:
                  continue            

def activateItem(idItem):

      query = "UPDATE Item SET Status = 1 WHERE IdItem = " + str(idItem) + ";"

      connectionpsql = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      connectionpsql.query(query)

      connectionpsql.close()

      storeList = getIdStoreList()

      for i in storeList:
            try:
                  connection = mysql.connector.connect(host='localhost',
                                                database=db + str(i),
                                                user='root',
                                                password='root')

                  cursor = connection.cursor()

                  cursor.execute(query)

                  connection.commit()
                  connection.close()

            except:
                  continue            

# --------------------------------- New Functions ---------------------------------------------------

def ConsultGuarantee(idreceipt):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "SELECT SellingDate FROM Receipt WHERE IdReceipt = "+str(idreceipt)+" ;"

      data = connection.query(query)

      connection.close()

      test = data[0][0]

      today = date.today()
      requestDate = today

      if abs(requestDate.days - test).days > 30:
            return "La garantia se vencio..."
      else:
            return "La garantia sigue vigente..."

def InsertEmployee(idperson, idjob, idstore):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "SELECT * FROM Person WHERE IdPerson = " + str(idperson) + " ;"

      data = connection.query(query)

      today = date.today()
      requestDate = today.strftime("%Y-%m-%d")

      try:
            test = data[0][0]  
            InsertEmployee_aux(idperson)
            InsertEmployeeJob(idjob,idperson,idstore)
            InsertEmployeeMSQL(idperson, idstore)
            InsertEmployeeJobMSQL(idjob,idperson,idstore)
            return 1

      except:

            return "La persona no se encuentra en la base de datos..."

      connection.close()

def InsertEmployee_aux(idperson):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "INSERT INTO Employee VALUES ( " + str(idperson) + ", 1 );"

      data = connection.query(query)

      connection.close()


def InsertEmployeeJob(idjob, idperson, idstore):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      today = date.today()
      requestDate = today.strftime("%Y-%m-%d")

      query = "INSERT INTO EmployeeJob VALUES "
      query2 = idjob,idperson,idstore,requestDate
      query3 = query + str(query2) + ";" 

      data = connection.query(str(query3))      

      if idjob == 1:
            UpdateStoreAdmin(idstore,idperson)

      connection.close()

def UpdateStoreAdmin(idstore,idperson):
      connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

      query = "SELECT * FROM Store WHERE IdStore = " + str(idstore) + ";"

      data = connection.query(query)

      oldidadmin = data[0][4]

      query2 = "UPDATE Store SET IdAdmin = " + str(idperson) + "WHERE IdAdmin = " + str(oldidadmin) + ";"
      data2 = connection.query(query2)

      query3 = "UPDATE Employee SET Status = 0 WHERE IdPerson = " + str(oldidadmin) + ";"
      data3 = connection.query(query3)

      connection.close()
# ---------------------------------- MySQL -------------------------------------------------------------

def InsertEmployeeMSQL(idperson,idStore):

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      query = "INSERT INTO Employee VALUES ( " + str(idperson) + ", 1 );"
      
      try:

            cursor.execute(query)
            connection.commit()

      except:

            print(query)


      return

def InsertEmployeeJobMSQL (idjob, idperson, idStore):

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor() 

      today = date.today()
      requestDate = today.strftime("%Y-%m-%d")

      query = "INSERT INTO EmployeeJob VALUES "
      query2 = idjob,idperson,requestDate
      query3 = query + str(query2) + ";"

      try:

            cursor.execute(str(query3))
            connection.commit()

      except:

            print(query)


      return

def UpdateStore(idperson, idStore):
      connection = mysql.connector.connect(host='localhost',
                                          database=db + str(idStore),
                                          user='root',
                                          password='root')
      cursor = connection.cursor()

      try:

            query = "SELECT * FROM Store WHERE IdStore = " + str(idstore) + ";"
            cursor.execute(query)

            data = cursor.fetchall()
            oldidadmin = data[0][4]

            query2 = "UPDATE Store SET IdAdmin = " + str(idperson) + "WHERE IdAdmin = " + str(oldidadmin) + ";"
            cursor.execute(query2)

            query3 = "UPDATE Employee SET Status = 0 WHERE IdPerson = " + str(oldidadmin) + ";"
            cursor.execute(query3)

            connection.commit()

      except:
            print(query)
      return