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

def generatePersonaScript():
    file = open("PersonaScript.sql", "w+")
    

generateStateScript()
        
    