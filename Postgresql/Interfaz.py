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

status 0 