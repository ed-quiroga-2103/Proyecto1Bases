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

def ConsultEmployee(IdEmpleado):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM ConsultEmployee(" + str(IdEmpleado) + ");"

      print( connection.query(query))

      connection.close()

def ConsultStore(IdStore):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      query = "SELECT * FROM ConsultStore(" + str(IdStore) + ");"

      print( connection.query(query))

      connection.close()

def InsertEmployee(Name,  MiddleName, LastName, IdentityDoc, IdAddress, Status, IdJob, IdStore, HireDate):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertEmployee"
      cuerpo = str(Name) , str(MiddleName),  str(LastName) , str(IdentityDoc),IdAddress, Status,IdJob,IdStore,str(HireDate)
      final = encabezado + str(cuerpo) + ";"
      
      print( connection.query(str(final)))

      connection.close()


def InsertPromo(newIdStore, newIdItem , newInitialDateTime , newFinalDateTime , newPorcentage ):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertPromo"
      cuerpo = newIdStore , newIdItem, str(newInitialDateTime), str(newFinalDateTime),newPorcentage
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()


def InsertStore(Code , IdAddress , Status , IdAdmin ):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT InsertStore"
      cuerpo = Code , IdAddress, Status, IdAdmin
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()  

def ModifyEmployee(Id, Status):
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyEmpoyee"
      cuerpo = Id, Status
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()
      
def ModifyEmployeePerson(Id , newName ,  newMiddleName , newLastName , newIdentityDoc , newIdAddress ) :
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyEmployeePerson"
      cuerpo = Id, str(newName), str(newMiddleName), str(newLastName), str(newIdentityDoc),newIdAddress
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

      connection.close()

def ModifyStore(newid , newcode , newidaddress , newstatus , newidadmin )  :
      connection = pg.DB(dbname='sk8database', host='127.0.0.1', port = 5432, user='root', passwd='root')
      
      encabezado = "SELECT ModifyStore"
      cuerpo = newid, newcode, newidaddress, newstatus, newidadmin
      final = encabezado + str(cuerpo) + ";"
      
      print(str(final))
      print( connection.query(str(final)))

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


def fragEmployeeStore(idStore):
      
      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      cursor.execute("SELECT IdPerson FROM Employee;")

      cursor.close()


def reportePuntos():

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      cursor.execute("CALL ReportePuntos();")

      cursor.close()


def reportePuntos():

      connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

      cursor = connection.cursor()

      cursor.execute("CALL ReporteCompras();")

      cursor.close()
      

def consultaGarantia(fecha)

      connection = mysql.connector.connect(host='localhost',
                                          database=db + str(idStore),
                                          user='root',
                                          password='root')

            cursor = connection.cursor()

            cursor.execute("SELECT GarantiaProducto("+str(fecha)+");")

            data = cursor.fetchall()

            if data = 0:
                  print("La garantia se vencio")
            else:
                  print("La garantia sigue vigente")

            cursor.close()



def consultaPromocion(fecha)

      connection = mysql.connector.connect(host='localhost',
                                          database=db + str(idStore),
                                          user='root',
                                          password='root')

            cursor = connection.cursor()

            cursor.execute("SELECT PromocionFechaHora("+str(fecha)+");")
            
            data = cursor.fetchall()

            if data = 0:
                  print("La promocion se vencio")
            else:
                  print("La promocion sigue vigente")


            cursor.close()


def consultaPromocion(id)

      connection = mysql.connector.connect(host='localhost',
                                          database=db + str(idStore),
                                          user='root',
                                          password='root')

            cursor = connection.cursor()

            cursor.execute("SELECT PromocionFechaHora("+str(id)+");")

            data = cursor.fetchall()
            
            print(data)

            cursor.close()
     