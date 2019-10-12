import mysql.connector
from mysql.connector import Error
import pg

from datetime import date


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
    try:
        IdReceipt = records[0][0] + 2
    except:
        IdReceipt = 1

    while(ind != len(itemIds)):

        cursor.execute("SELECT Quantity FROM ItemStore WHERE IdItem = "+ str(itemIds[ind]))

        records = cursor.fetchall()

        stock = records[0][0]

        if QuantItem[ind] > stock:
            if input("There are only "+str(stock)+" items with the ID: "+str(itemIds[ind])+".\nWould you like to buy that number of items?") != "y":
                QuantItem[ind] = stock
            else:
                ind+=1
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

    updateCustomerPoinst(IdCustomer, int(totalPrice*0.10))


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



def updateCustomerPoinst(IdCustomer, points):

    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    query = "UPDATE Customer SET Points = " + str(points) + " WHERE IdPerson = " + str(IdCustomer) + ";"

    cursor.execute(query)

    connection.commit()

def updatePromoPSQL(IdStore, IdItem, initialDateTime, finalDateTime, percentage):
    
    #LA FRAGMENTACION TAMBIEN TIENE QUE HACERSE CON LAS PROMOCIONES

    initialDate = initialDateTime.split(" ")[0]
    finalDate = finalDateTime.split(" ")[0]

    connection = pg.DB(host='localhost',
                       user='root',
                       passwd='root',
                       dbname='testpsql')

    query = "INSERT INTO Promo (IdStore, IdItem, InitialDate, FinalDate, Porcentaje) VALUES"
    query +=  str((IdStore, IdItem, initialDate, finalDate, percentage))

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

