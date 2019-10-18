import mysql.connector
from mysql.connector import Error
import pg
import csv

from datetime import date
from WarehouseFunctions import *

db = "Test"

def getLastReceipt(idStore):

    query = 'SELECT IdReceipt FROM Receipt ORDER BY IdReceipt DESC LIMIT 1;'

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()


    id = 0
    
    cursor.execute(query)
    
    records = cursor.fetchall()
    try:
        id = records[0][0] + 1
    except:
        id = 1

    return id

def purchase(itemIds, QuantItem, IdSeller, IdCustomer, idStore, IdPayment):
    totalPrice = 0
    ind = 0

    today = date.today()
    sellingDate = today.strftime("%Y-%m-%d")


    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT LAST_INSERT_ID() FROM Receipt;")
    records = cursor.fetchall()
    
    IdReceipt = getLastReceipt(idStore)



    while(ind != len(itemIds)):

        cursor.execute("SELECT Quantity FROM ItemStore WHERE IdItem = "+ str(itemIds[ind]))

        records = cursor.fetchall()

        stock = records[0][0]

        if QuantItem[ind] > stock:
            if input("Solamente hay "+str(stock)+" articulos con el ID: "+str(itemIds[ind])+".\nDesea comprarlos todos?") == "y":
                QuantItem[ind] = stock
            else:
                ind+=1
                continue
        elif stock == 0:
            print("El articulo con el ID: " + str(itemIds[ind]) + " no se encuentra en existencia")
            continue
        
        updateItemStock(itemIds[ind], stock - QuantItem[ind], idStore)

        totalPrice += getItemPrice(itemIds[ind], idStore)*QuantItem[ind]

        ind+=1

    queryData = ()
    query = ""
    

    
    query = "INSERT INTO Receipt (IdEmployee, IdCustomer, Price, SellingDate, idPayment) VALUES (%s,%s,%s,%s, %s);"
    queryData = (IdSeller, IdCustomer, totalPrice, sellingDate, IdPayment)

    updateCustomerPoints(IdCustomer, int(totalPrice*0.10), idStore)


    cursor.execute(query, queryData)

    connection.commit()


    ind = 0 

    while(ind != len(itemIds)):
        subQuery = "INSERT INTO ItemReceipt (IdItem, IdReceipt, Quantity) VALUES  (%s,%s,%s);"

        data = (itemIds[ind], IdReceipt, QuantItem[ind])
    
        cursor.execute(subQuery, data)

        ind+=1

    connection.commit()


    return query

def getItemPrice(itemId, idStore):

    query = "SELECT Price FROM Item WHERE IdItem = "+str(itemId)+";"

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute(query)

    records = cursor.fetchall()


    return records[0][0]

def updateItemStock(itemId, quantity, idStore):


    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "UPDATE ItemStore SET Quantity = " + str(quantity) + " WHERE IdItem = " + str(itemId) + ";"

    try:

        cursor.execute(query)
        connection.commit()

    except:

        print(query)


    return

def getItemsWithCeroStock(idStore):


    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("""SELECT ItemStore.IdItem FROM ItemStore 
    INNER JOIN Item ON Item.IdItem = ItemStore.IdItem 
    WHERE Item.Status = 1 AND ItemStore.Quantity < 5;""")

    records = cursor.fetchall()

    itemIds = []

    for line in records:

        itemIds.append(line[0])

    
    return itemIds

def updateCustomerPoints(IdCustomer, points, idStore):

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "UPDATE Customer SET Points = Points +  " + str(points) + " WHERE IdPerson = " + str(IdCustomer) + ";"

    cursor.execute(query)

    connection.commit()

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='datawarehouse')

    connection.query(query)

    connection.close()

def modifyCustomerPoints(IdCustomer, points, idStore):
    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "UPDATE Customer SET Points = " + str(points) + " WHERE IdPerson = " + str(IdCustomer) + ";"

    cursor.execute(query)

    connection.commit()

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='datawarehouse')

    connection.query(query)

    connection.close()

def sendPromos(idStore):
    
    #LA FRAGMENTACION TAMBIEN TIENE QUE HACERSE CON LAS PROMOCIONES
    data = getPromos(idStore)

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

    for line in data:
        query = "INSERT INTO Promo VALUES "
        query += str( (line[0], idStore, line[1], line[2].strftime("%Y-%m-%d %H:%M:%S"), line[3].strftime("%Y-%m-%d %H:%M:%S"), line[4]) )
        query += ";"
        connection.query(query)


    connection.close()

def createPromo(IdItem, initialDateTime, finalDateTime, percentage, idStore):

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "INSERT INTO Promo (IdItem, InitialDateTime, FinalDateTime, Percentage) VALUES"
    query +=  str((IdItem, initialDateTime, finalDateTime, percentage)) + ";"


    cursor.execute(query)

    connection.commit()

    connection.close()

def getPromos(idStore):

    today = date.today()
    currentDate = today.strftime("%Y-%m-%d")

    

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Promo WHERE DATE(InitialDateTime) = '"+currentDate+"';")

    data = cursor.fetchall()

    connection.close()

    return data

def getReceipts(idStore):

    today = date.today()
    currentDate = today.strftime("%Y-%m-%d")

    

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Receipt WHERE SellingDate = '"+currentDate+"';")

    data = cursor.fetchall()

    connection.close()

    return data

def sendReceipts(idStore):

    receipts = getReceipts(idStore)

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='datawarehouse')

    for receipt in receipts:
        
        query = (receipt[0], receipt[1],
                receipt [2], idStore, receipt[3], receipt[5],receipt[4].strftime("%Y-%m-%d"))
        

        connection.query('INSERT INTO Receipt VALUES ' + str(query) + ";" )

    connection.close()

    sendItemReceipt(idStore)

def getItemReceipt(idStore):
    
    today = date.today()
    currentDate = today.strftime("%Y-%m-%d")


    query = "SELECT IR.* FROM ItemReceipt IR INNER JOIN Receipt R ON IR.IdReceipt = R.IdReceipt WHERE R.SellingDate = '"

    query += currentDate + "';"

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()
    cursor.execute(query)

    data = cursor.fetchall()

    return data

def sendItemReceipt(idStore):

    data = getItemReceipt(idStore)

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='datawarehouse')

    for line in data:
        
        query = (line[0], line[1],
                line[2])
        

        connection.query('INSERT INTO ItemReceipt (IdItem, IdReceipt, Quantity) VALUES ' + str(query) + ";" )

    connection.close()

def getStock(idStore):

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM ItemStore;")

    data = cursor.fetchall()

    connection.close()

    return data

def updateStock(idStore):

    stock = getStock(idStore)

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='datawarehouse')

    for item in stock:
        
        query = "UPDATE ItemStore SET Quantity = " 
        query += str(item[1]) 
        query += " WHERE IdItem = "
        query += str(item[0])
        query += " AND IdStore = " + str(idStore) + ";"

        print(query)

        connection.query(query)

    connection.close()

def updateWarehouse(idStore):

    sendReceipts(idStore)

    updateStock(idStore)

    sendPromos(idStore)

    generateStoreRequest(idStore)

def getCustomerPoints(IdCustomer, idStore):

    query = "SELECT Points FROM Customer WHERE IdPerson = " + str(IdCustomer) + ";"

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute(query)
    records = cursor.fetchall()
    
    points = 0
    try:
        points = records[0][0]
    except:
        points = -1

    return points

def buyWithPoints(itemIds, QuantItem, IdSeller, IdCustomer, idStore, IdPayment):
    totalPrice = 0
    ind = 0

    points = getCustomerPoints(IdCustomer, idStore)

    if points == -1:
        print("El cliente no esta registrado")

        return

    today = date.today()
    sellingDate = today.strftime("%Y-%m-%d")


    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT LAST_INSERT_ID() FROM Receipt;")
    records = cursor.fetchall()
    
    IdReceipt = getLastReceipt(idStore)



    while(ind != len(itemIds)):

        cursor.execute("SELECT Quantity FROM ItemStore WHERE IdItem = "+ str(itemIds[ind]))

        records = cursor.fetchall()

        stock = records[0][0]

        if QuantItem[ind] > stock:
            if input("Solamente hay "+str(stock)+" articulos con el ID: "+str(itemIds[ind])+".\nDesea comprarlos todos?") == "y":
                QuantItem[ind] = stock
            else:
                ind+=1
                continue
        elif stock == 0:
            print("El articulo con el ID: " + str(itemIds[ind]) + " no se encuentra en existencia")
            continue
        
        updateItemStock(itemIds[ind], stock - QuantItem[ind], idStore)

        totalPrice += getItemPrice(itemIds[ind], idStore)*QuantItem[ind]

        ind+=1

    queryData = ()
    query = ""
    
    if totalPrice >= points:
        modifyCustomerPoints(IdCustomer, 0, idStore)
        totalPrice -= points
    else:
        points -= totalPrice
        totalPrice = 0
        modifyCustomerPoints(IdCustomer, points, idStore)


    query = "INSERT INTO Receipt (IdEmployee, IdCustomer, Price, SellingDate, idPayment) VALUES (%s,%s,%s,%s, %s);"
    queryData = (IdSeller, IdCustomer, totalPrice, sellingDate, IdPayment)

    cursor.execute(query, queryData)

    connection.commit()


    ind = 0 

    while(ind != len(itemIds)):
        subQuery = "INSERT INTO ItemReceipt (IdItem, IdReceipt, Quantity) VALUES  (%s,%s,%s);"

        data = (itemIds[ind], IdReceipt, QuantItem[ind])

        cursor.execute(subQuery, data)

        ind+=1

    connection.commit()


    return query

def isAdmin(idEmployee):

    query = "SELECT E.IdPerson FROM Employee E "
    query += "INNER JOIN EmployeeJob EJ ON EJ.IdPerson = E.IdPerson "
    query += "WHERE EJ.IdJob = 1 AND E.Status = 1;"

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

    data = connection.query(query)

    connection.close()

    try:
        for line in data:

            if line[0] == idEmployee:
                return True

    except:
        return False

    

    return False

def getAdminStore(idAdmin):

    query = "SELECT S.IdStore FROM Store S "
    query += "INNER JOIN EmployeeJob EJ ON EJ.IdStore = S.IdStore "
    query += "WHERE EJ.IdPerson = " + str(idAdmin) + ";"

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

    data = connection.query(query)

    connection.close()

    idStore = data[0][0]

    return idStore

def getNonAdminsForStore(idStore, prevAdmin):

    query = "SELECT E.* FROM Employee E "
    query += "INNER JOIN EmployeeJob EJ ON EJ.IdPerson = E.IdPerson "
    query += "WHERE EJ.IdJob != 1 AND EJ.IdStore = " + str(idStore) 
    query += " AND E.IdPerson != " + str(prevAdmin) + "AND E.Status = 1;"

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

    data = connection.query(query)


    connection.close()
    
    try:
        nextAdmin = data[0][0]
        return nextAdmin

    except:
        return -1

def deactivateEmployee(idEmployee):

    if isAdmin(idEmployee):

        return deactivateAdmin(idEmployee)

    else:

        query = "UPDATE Employee SET Status = 0 WHERE IdPerson = " + str(idEmployee) + ";"

        connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

        connection.query(query)

def deactivateAdmin(idEmployee):

    idStore = getAdminStore(idEmployee)

    newAdmin = getNonAdminsForStore(idStore, idEmployee)

    if newAdmin == -1:
        deactivateStore(idStore)

    else:
        connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

        

        query = "UPDATE Employee SET Status = 0 WHERE IdPerson = " +str(idEmployee) + ";"

        connection.query(query)

        query = "UPDATE Store SET IdAdmin = " + str(newAdmin) + " "

        query += "WHERE IdStore = " + str(idStore) + ";"

        connection.query(query)

        query = "UPDATE EmployeeJob SET IdJob = 1 WHERE IdPerson = " + str(newAdmin) + ";"

        connection.query(query)
        
        print(query)

        connection.close()

def deactivateStore(idStore):

    query = "UPDATE Store SET Status = 0 WHERE IdStore = " + str(idStore) + ";"

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

    connection.query(query)

    connection.close()

    deactivateStoreEmployees(idStore)

def deactivateStoreEmployees(idStore):

    query = "UPDATE Employee SET Status = 0 FROM Employee E "
    query += "INNER JOIN EmployeeJob EJ ON EJ.IdPerson = E.IdPerson WHERE EJ.IdStore = " + str(idStore) + ";"

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

    connection.query(query)

    connection.close()

def employeeOfTheMonth(idStore):

    query = "SELECT IdEmployee, COUNT(IdEmployee) AS Sales FROM Receipt GROUP BY IdEmployee ORDER BY Sales DESC LIMIT 1;"



    connection = mysql.connector.connect(host='localhost',
                                         database= db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute(query)

    data = cursor.fetchall()

    employeeId = 0

    try:
        employeeId = data[0][0]

    except:

        print("No employee")
    
    connection.close()

    return getEmployeeData(employeeId, idStore)

def getEmployeeData(idEmployee, idStore):

    query = "SELECT * FROM Person WHERE IdPerson = " + str(idEmployee) + ";"

    connection = mysql.connector.connect(host='localhost',
                                         database= db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute(query)

    data = cursor.fetchall()
    try:
        return data[0]
    except:
        return "There are no sales registered"

def generateStoreRequest(idStore):

    items = getItemsWithCeroStock(idStore)

    today = date.today()
    requestDate = today.strftime("%Y-%m-%d")


    query = "INSERT INTO StoreRequest (IdStore, RequestDate) VALUES "
    query += str( (idStore, requestDate) ) + ";"

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='datawarehouse')

    connection.query(query)

    data = connection.query("SELECT IdRequest FROM StoreRequest ORDER BY IdRequest DESC;")

    try:

        idRequest = data[0][0]

    except:

        idRequest = 1

    query = "INSERT INTO StoreRequestItem VALUES "

    for item in items:
        
        amount = getRestock(idStore, item)

        connection.query(query + str((idRequest, item, amount)))

    connection.close()

def getRestock(idStore, idItem):

    connection = mysql.connector.connect(host='localhost',
                                         database= db + str(idStore),
                                         user='root',
                                         password='root')
    cursor = connection.cursor()

    cursor.execute("SELECT Quantity FROM ItemStore WHERE IdItem = " + str(idItem) + ";")

    data = cursor.fetchall()

    connection.close()

    return 5 - data[0][0]

def openStore(idStore):
    fragItemStore(idStore)
    fragEmployeeStore(idStore)

def buyWithPromo(itemIds, QuantItem, IdSeller, IdCustomer, idStore, idPromo, IdPayment):
    totalPrice = 0
    ind = 0

    today = date.today()
    sellingDate = today.strftime("%Y-%m-%d")

    promo = getPromoItemAndDiscount(idPromo, idStore)

    if promo == -1:
        print("The promo does not exist")
        return
    

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT LAST_INSERT_ID() FROM Receipt;")
    records = cursor.fetchall()
    
    IdReceipt = getLastReceipt(idStore)



    while(ind != len(itemIds)):

        cursor.execute("SELECT Quantity FROM ItemStore WHERE IdItem = "+ str(itemIds[ind]))

        records = cursor.fetchall()

        stock = records[0][0]

        if QuantItem[ind] > stock:
            if input("Solamente hay "+str(stock)+" articulos con el ID: "+str(itemIds[ind])+".\nDesea comprarlos todos?") == "y":
                QuantItem[ind] = stock
            else:
                ind+=1
                continue
        elif stock == 0:
            print("El articulo con el ID: " + str(itemIds[ind]) + " no se encuentra en existencia")
            continue
        
        updateItemStock(itemIds[ind], stock - QuantItem[ind], idStore)

        totalPrice += getItemPrice(itemIds[ind], idStore)*QuantItem[ind]

        if itemIds[ind] == promo[0]:
            totalPrice -= getItemPrice(itemIds[ind], idStore)*QuantItem[ind] * (promo[1]/100)

        ind+=1

    queryData = ()
    query = ""
    
    totalPrice = int(totalPrice)
    

    query = "INSERT INTO Receipt (IdEmployee, IdCustomer, Price, SellingDate, idPayment) VALUES (%s,%s,%s,%s, %s);"
    queryData = (IdSeller, IdCustomer, totalPrice, sellingDate, IdPayment)

    updateCustomerPoints(IdCustomer, int(totalPrice*0.10), idStore)


    cursor.execute(query, queryData)

    connection.commit()


    ind = 0 

    while(ind != len(itemIds)):
        subQuery = "INSERT INTO ItemReceipt (IdItem, IdReceipt, Quantity) VALUES  (%s,%s,%s);"

        data = (itemIds[ind], IdReceipt, QuantItem[ind])
    
        cursor.execute(subQuery, data)

        ind+=1

    connection.commit()


    return query

def getPromoItemAndDiscount(idPromo, idStore):

    connection = mysql.connector.connect(host='localhost',
                                         database=db + str(idStore),
                                         user='root',
                                         password='root')

    cursor = connection.cursor()


    query = "SELECT IdItem, Percentage FROM Promo WHERE IdPromo = "
    query += str(idPromo) + ";"


    cursor.execute(query)

    data = cursor.fetchall()

    connection.close()

    try:
        return data[0]

    except:
        
        return -1

def generateSalesReport(idStore):

    connection = mysql.connector.connect(host='localhost',
                                        database=db + str(idStore),
                                        user='root',
                                        password='root')

    cursor = connection.cursor()

    query = "CALL SalesReport();"
    
    try:
    
        cursor.execute(query)
    
        data = cursor.fetchall()
    
        myFile = open('ReporteDeCompras'+str(idStore)+'.csv', 'w+')
    
        with myFile:
    
            writer = csv.writer(myFile)
        
            writer.writerows(data)
        
        print("Writing complete")      
    
        connection.close()
    except:
        print("No se logro escribir el archivo...")
    return

def generatePointsReport(idStore):
    connection = mysql.connector.connect(host='localhost',
                                        database=db + str(idStore),
                                        user='root',
                                        password='root')
    cursor = connection.cursor()
    query = "CALL PointsReport();"
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        myFile = open('ReporteDePuntos'+str(idStore)+'.csv', 'w+')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(data)
        print("Writing complete")      
        connection.close()
    except:
        print("No se logro escribir el archivo...")
    return

def consultSales(idemployee):
    connection = pg.DB(dbname='datawarehouse', host='127.0.0.1', port = 5432, user='root', passwd='root')

    query = "SELECT ConsultSales( " + str(idemployee) + ");" 

    data = connection.query(query)

    print(data)

    connection.close()