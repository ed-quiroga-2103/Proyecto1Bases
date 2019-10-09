import random

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
    file = open("Python/Queries/CityQuery.sql","w+")

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

    file = open("Python/Queries/AddressQuery.sql", "w+")
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


    file = open("Python/Queries/PersonaQuery.sql", "w+")
    file.write(queries)
    file.close()

def generateIdList(num, max):

    idList = []

    for i in range(num):
        
        id = random.choice(range(max))+1

        while id in idList:
            id = random.choice(range(max))+1

        idList.append(id)
    
    return idList

def generateEmployee(IdPerson,IdStore):

    return (IdPerson, 1)

def generateStore():
    #Pending
    pass

