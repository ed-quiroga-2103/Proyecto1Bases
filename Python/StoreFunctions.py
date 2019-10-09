import mysql.connector
from mysql.connector import Error

from datetime import date


def purchase(itemIds, QuantItem, IdSeller, IdCustomer):
    totalPrice = 0
    ind = 0

    today = date.today()
    sellingDate = today.strftime("%Y-%m-%d")


    while(ind != len(itemIds)):
        totalPrice += getItemPrice(itemIds[ind])*QuantItem[ind]
        ind+=1

    queryData = () 
    query = ""

    if IdCustomer != -1:
        query = "INSERT INTO Receipt (IdEmployee, IdCustomer, Price, SellingDate) VALUES "
        queryData = (IdSeller, IdCustomer, totalPrice, sellingDate)

        query = query + str(queryData) + ";"

    else:
        query = "INSERT INTO Receipt (IdEmployee, IdCustomer, Price, SellingDate) VALUES "
        queryData = "(" + str(IdSeller) + ", NULL" + ", " + str(totalPrice) + "," + sellingDate + ")"

        query = query + str(queryData) + ";"



    connection = mysql.connector.connect(host='localhost',
                                         database='Test1',
                                         user='root',
                                         password='root')

    cursor = connection.cursor()

    cursor.execute(query)

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


