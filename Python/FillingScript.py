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


    

#generateStateScript()
generateCityScript()     
    