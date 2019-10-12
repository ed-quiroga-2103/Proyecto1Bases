import random
from datetime import date

def linesToList(path):
    file = open(path,"r")
    nameList = []

    for line in file:
        line = line.rstrip()      
        if line:                  
            nameList.append(line)

    file.close()

    return nameList

def generateStateScript():
    file = open("StateQuery.sql", "w+")

    lines = linesToList("Python/DataPools/States.txt")

    queries = ""
    
    print(len(lines))

    file.write("INSERT INTO State VALUES\n")
    
    for i in range(len(lines)-1):

        query = (1, i+1, lines[i])
        queries += str(query) + "," + "\n"

    query = str((1, len(lines), lines[-1])) + ";"

    file.write(queries)

    file.write(query)

    file.close()
    
def generateCityScript():
    file = open("Queries/CityQuery.sql","w+")

    lines = linesToList("Python/DataPools/Cities.txt")

    num = int(len(lines)/50)

    cont = 0
    stateId = 1
    cityId = 1
    
    query = ""

    file.write("INSERT INTO City VALUES\n")

    while(stateId != 51):
        
        while(cont != num):
            
            query += str((cityId,stateId,lines[cityId-1])) + ",\n"

            cityId += 1
            cont += 1

        cont = 0
        stateId += 1

    file.write(query)

    file.close()

def generateAddressScript():
    #350 cities
    cont = 0   
    idCont = 1
    queries = ""

    for i in range(1,351):
        while(cont != 3):
            calleNum = random.choice(range(1,51))
            address = "Calle " + str(calleNum) 
            query = (idCont, i, address)
            cont +=1
            idCont +=1

            queries += str(query) + ",\n"

        cont = 0

    file = open("Queries/AddressQuery.sql", "w+")
    file.write(queries)
    file.close()
    

    
def generatePersona(IdPersona, IdAddress):
    #Persona(IdPersona, Nombre, Apellido, IdentDoc, IdAddress)

    name = random.choice(linesToList("Python/DataPools/FirstNames.txt"))
    hasMiddleName = random.choice(range(10)) >= 5
    lastName = random.choice(linesToList("Python/DataPools/LastNames.txt"))
    identDoc = ""
    identNum = IdPersona
    for i in range(6):
        identDoc += str(identNum%10)
        identNum = identNum//10
    
    identDoc = name[0] + lastName[0] + identDoc[::-1]

    query = ""

    

    if hasMiddleName:
        middleName = random.choice(linesToList("Python/DataPools/FirstNames.txt"))
        query = (IdPersona, name, middleName, lastName, identDoc, IdAddress)
        return str(query)
    else:
        IdPersona = str(IdPersona)
        IdAddress = str(IdAddress)
        query = "("+IdPersona+", '"+name+"'"+", NULL"+", '"+lastName+"', '"+identDoc+"', "+IdAddress+")"
    return query

def generatePersonaScript():
    #1050 addresses

    queries = "INSERT INTO Persona VALUES\n"

    for i in range(2000):
        IdAddress = random.choice(range(1050)) + 1

        queries += generatePersona(i+1, IdAddress) + ",\n"


    file = open("Queries/PersonaQuery.sql", "w+")
    file.write(queries)
    file.close()

def generateIdList(num, max, excluded):

    idList = []

    for i in range(num):
        
        id = random.choice(range(max))+1

        while id in idList and id in excluded:
            id = random.choice(range(max))+1

        idList.append(id)
    
    return idList

def generateEmployee(IdPerson):

    return (IdPerson, 1)

def generateEmployeeScript(num, IdList, IdStore):

    queries = ""

    for i in range(num):
        queries += str(generateEmployee(IdList[i])) + ", \n"
    
    file = open("Queries/Employee"+str(IdStore)+".sql", "w+")
    file.write(queries)
    file.close()


def generateJobEmployee(IdPerson, IdStore, hireDate, IdJob = -1):
    if IdJob == -1:
        IdJob = random.choice(range(2,5))
    return (IdJob+1, IdPerson, IdStore, hireDate)

def generateJobEmployeeScript(IdList, IdAdmin, IdStore):
    today = date.today()
    hireDate = today.strftime("%Y-%m-%d")

    queries = "INSERT INTO JobEmployee VALUES\n"+ str((1, IdAdmin, IdStore, hireDate)) + ",\n"

    IdList.remove(IdAdmin)

    for i in range(len(IdList)):
        idEmployee = IdList[i]

        query = generateJobEmployee(idEmployee, IdStore, hireDate)

        queries += str(query) + ",\n"
    
    file = open("Queries/JobEmployees"+str(IdStore)+".sql", "w+")
    file.write(queries)
    file.close()

    return



def generateStore(IdStore, excluded):
    #2000 IdPersona
    #1050 addresses

    #Store Data
    #HAY QUE CONSIDERAR QUE LOS ID DE LOS EMPLEADOS NO SE REPITAN ENTRE TIENDAS
    #Se puede utilizar una lista de exclusion de ids
    idList = generateIdList(10,2000, excluded)
    code = IdStore
    IdAddress = random.choice(range(1050))+1
    status = 1
    IdAdmin = random.choice(idList)

    
    query = (IdStore, code, IdAddress, status, IdAdmin) 
    #Employee Generation
    generateEmployeeScript(10,idList,IdStore)

    #JobEmployee Generation
    generateJobEmployeeScript(idList, IdAdmin, IdStore)

    file = open("Queries/Store"+str(IdStore)+"Query.sql", "w+")
    file.write("INSERT INTO Store VALUES \n" + str(query) + ";")
    file.close()

    file = open("ExcludedIds.txt", "a+")
    file.write(str(idList)+"\n")
    file.close()

def getRandElements(elements, num):

    randElements = []

    for i in range(num):
        ele = random.choice(elements)

        while ele in randElements:
            ele = random.choice(elements)

        randElements.append(ele)

    return randElements

def generateBrands():
    
    brands = linesToList("Python/DataPools/Brands.txt")

    randBrands = getRandElements(brands, 25)

    queries = "INSERT INTO Brand VALUES"

    for i in range(25):

        queries += str( (i+1, randBrands[i]) ) + ",\n"

    file = open("Queries/BrandQuery.sql", "w+")
    file.write(queries)
    file.close()

def generateItem(IdItem, IdBrand):

    categories = [1,2,3,4,5,6,7,8,9]
    categoryDescription = ["Shirt", "Pants", "Shoes", "Skateboard", "Trucks", "Wheels", "Bearings", "Board", "Hat"]
    prices = [25,40,80,120,40,45,25,60,25]
    descriptions = ["Nice ", "Cool ", "Amazing ", "The best ", "Fire "]

    ind = random.choice(range(9))

    category = categories[ind]
    price = prices[ind]
    description = descriptions[ind%5] + categoryDescription[ind]
    
    today = date.today()
    entryDate = today.strftime("%Y-%m-%d")

    status = 1

    return (IdItem, IdItem, IdBrand, description, category, price, status, entryDate)

def generateItems():

    queries = "INSERT INTO Items VALUES\n"

    contItem = 1
    contBrand = 1

    contLim = 0

    while contBrand != 26:

        while contLim != 10:

            query = str(generateItem(contItem, contBrand))

            queries += query + ",\n"

            contItem += 1
            contLim += 1

        contLim = 0
        contBrand += 1


    file = open("Queries/ItemQuery3.sql", "w+")
    file.write(queries)
    file.close()

def generateCustomer():
    queries = "INSERT INTO Customer"
    for i in range(2000):
        query = (i+1, 1, 0)
        queries += str(query) + ",\n"

    file = open("Queries/CustomerQuery.sql")

