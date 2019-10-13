import mysql.connector
from mysql.connector import Error
import pg

from datetime import date


def getLastReceipt():

    query = 'SELECT IdReceipt FROM Receipt ORDER BY IdReceipt DESC LIMIT 1;'

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
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

def purchase(itemIds, QuantItem, IdSeller, IdCustomer):
    totalPrice = 0
    ind = 0

    today = date.today()
    sellingDate = today.strftime("%Y-%m-%d")


    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT LAST_INSERT_ID() FROM Receipt;")
    records = cursor.fetchall()
    
    IdReceipt = getLastReceipt()



    while(ind != len(itemIds)):

        cursor.execute("SELECT Quantity FROM ItemStore WHERE IdItem = "+ str(itemIds[ind]))

        records = cursor.fetchall()

        stock = records[0][0]

        if QuantItem[ind] > stock:
            if input("There are only "+str(stock)+" items with the ID: "+str(itemIds[ind])+".\nWould you like to buy that number of items?") == "y":
                QuantItem[ind] = stock
            else:
                ind+=1
                continue
        elif stock == 0:
            input("This item is not in stock")
            continue
        #NO ESTA FUNCIONANDO BIEN
        #LA CONDICION DE LA PREGUNTA ESTA MAL
        #NO AUMENTA EL SUBINDICE SI SE DECIDE NO COMPRAR
        updateItemStock(itemIds[ind], stock - QuantItem[ind])

        totalPrice += getItemPrice(itemIds[ind])*QuantItem[ind]

        ind+=1

    queryData = ()
    query = ""
    

    
    query = "INSERT INTO Receipt (IdEmployee, IdCustomer, Price, SellingDate) VALUES (%s,%s,%s,%s);"
    queryData = (IdSeller, IdCustomer, totalPrice, sellingDate)

    updateCustomerPoints(IdCustomer, int(totalPrice*0.10))


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

def getItemPrice(itemId):

    query = "SELECT Price FROM Item WHERE IdItem = "+str(itemId)+";"

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute(query)

    records = cursor.fetchall()


    return records[0][0]

def updateItemStock(itemId, quantity):


    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
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

def getItemsWithCeroStock():


    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT IdItem FROM ItemStore WHERE Quantity < 5;")

    records = cursor.fetchall()

    itemIds = []

    for line in records:

        itemIds.append(line[0])

    
    return itemIds

def generateItemRequest(IdRequest):

    query = ""

    ids = getItemsWithCeroStock()

    for i in range(len(ids) - 1):
        query += str((IdRequest, ids[i])) + ",\n "

    query += str((IdRequest, ids[-1])) + ";"

    return query

def updateCustomerPoints(IdCustomer, points):

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "UPDATE Customer SET Points = Points +  " + str(points) + " WHERE IdPerson = " + str(IdCustomer) + ";"

    cursor.execute(query)

    connection.commit()

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='testpsql')

    connection.query(query)

    connection.close()

def modifyCustomerPoints(IdCustomer, points):
    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "UPDATE Customer SET Points = " + str(points) + " WHERE IdPerson = " + str(IdCustomer) + ";"

    cursor.execute(query)

    connection.commit()

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='testpsql')

    connection.query(query)

    connection.close()

def sendPromos(idStore):
    
    #LA FRAGMENTACION TAMBIEN TIENE QUE HACERSE CON LAS PROMOCIONES
    data = getPromos()

    connection = pg.DB(host='localhost',
                        user='root',
                        passwd='root',
                        dbname='testpsql')

    for line in data:
        query = "INSERT INTO Promo VALUES "
        query += str( (line[0], idStore, line[1], line[2].strftime("%Y-%m-%d %H:%M:%S"), line[3].strftime("%Y-%m-%d %H:%M:%S"), line[4]) )
        query += ";"
        connection.query(query)


    connection.close()

def createPromo(IdItem, initialDateTime, finalDateTime, percentage):

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "INSERT INTO Promo (IdItem, InitialDateTime, FinalDateTime, Percentage) VALUES"
    query +=  str((IdItem, initialDateTime, finalDateTime, percentage)) + ";"


    cursor.execute(query)

    connection.commit()

    connection.close()

def getPromos():

    today = date.today()
    currentDate = today.strftime("%Y-%m-%d")

    

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Promo WHERE DATE(InitialDateTime) = '"+currentDate+"';")

    data = cursor.fetchall()

    connection.close()

    return data

def getReceipts():

    today = date.today()
    currentDate = today.strftime("%Y-%m-%d")

    

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Receipt WHERE SellingDate = '"+currentDate+"';")

    data = cursor.fetchall()

    connection.close()

    return data

def sendReceipts(idStore):

    receipts = getReceipts()

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='testpsql')

    for receipt in receipts:
        
        query = (receipt[0], receipt[1],
                receipt [2], idStore, receipt[3], receipt[4].strftime("%Y-%m-%d"))
        

        connection.query('INSERT INTO Receipt VALUES ' + str(query) + ";" )

    connection.close()

    sendItemReceipt()

def getItemReceipt():
    
    today = date.today()
    currentDate = today.strftime("%Y-%m-%d")


    query = "SELECT IR.* FROM ItemReceipt IR INNER JOIN Receipt R ON IR.IdReceipt = R.IdReceipt WHERE R.SellingDate = '"

    query += currentDate + "';"

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()
    cursor.execute(query)

    data = cursor.fetchall()

    return data

def sendItemReceipt():

    data = getItemReceipt()

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='testpsql')

    for line in data:
        
        query = (line[0], line[1],
                line[2])
        

        connection.query('INSERT INTO ItemReceipt (IdItem, IdReceipt, Quantity) VALUES ' + str(query) + ";" )

    connection.close()

def getStock():

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM ItemStore;")

    data = cursor.fetchall()

    connection.close()

    return data

def updateStock(idStore):

    stock = getStock()

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='testpsql')

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

def getCustomerPoints(IdCustomer):

    query = "SELECT Points FROM Customer WHERE IdPerson = " + str(IdCustomer) + ";"

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
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

def buyWithPoints(itemIds, QuantItem, IdSeller, IdCustomer):
    totalPrice = 0
    ind = 0

    points = getCustomerPoints(IdCustomer)

    if points == -1:
        print("The customer is not registered")

        return

    today = date.today()
    sellingDate = today.strftime("%Y-%m-%d")


    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute("SELECT LAST_INSERT_ID() FROM Receipt;")
    records = cursor.fetchall()
    
    IdReceipt = getLastReceipt()



    while(ind != len(itemIds)):

        cursor.execute("SELECT Quantity FROM ItemStore WHERE IdItem = "+ str(itemIds[ind]))

        records = cursor.fetchall()

        stock = records[0][0]

        if QuantItem[ind] > stock:
            if input("There are only "+str(stock)+" items with the ID: "+str(itemIds[ind])+".\nWould you like to buy that number of items?") == "y":
                QuantItem[ind] = stock
            else:
                ind+=1
                continue
        elif stock == 0:
            input("This item is not in stock")
            continue
        #NO ESTA FUNCIONANDO BIEN
        #LA CONDICION DE LA PREGUNTA ESTA MAL
        #NO AUMENTA EL SUBINDICE SI SE DECIDE NO COMPRAR
        updateItemStock(itemIds[ind], stock - QuantItem[ind])

        totalPrice += getItemPrice(itemIds[ind])*QuantItem[ind]

        ind+=1

    queryData = ()
    query = ""
    
    if totalPrice >= points:
        modifyCustomerPoints(IdCustomer, 0)
        totalPrice -= points
    else:
        points -= totalPrice
        totalPrice = 0
        modifyCustomerPoints(IdCustomer, points)

    
    query = "INSERT INTO Receipt (IdEmployee, IdCustomer, Price, SellingDate) VALUES (%s,%s,%s,%s);"
    queryData = (IdSeller, IdCustomer, totalPrice, sellingDate)

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
