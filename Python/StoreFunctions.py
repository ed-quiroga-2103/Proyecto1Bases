import mysql.connector
from mysql.connector import Error

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
        totalPrice += getItemPrice(itemIds[ind])*QuantItem[ind]

        ind+=1

    queryData = ()
    query = ""
    

    if IdCustomer != -1:
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


