CREATE TABLE IF NOT EXISTS Country (

    IdCountry PRIMARY KEY INT UNIQUE NOT NULL,
    Name TEXT NOT NULL

);

CREATE TABLE IF NOT EXISTS State (

    IdState PRIMARY KEY INT UNIQUE NOT NULL,
    IdCountry INT NOT NULL,
    Name TEXT NOT NULL,

    FOREIGN KEY (IdCountry) REFERENCES Country (IdCountry) 

);

CREATE TABLE IF NOT EXISTS City (

    IdCity PRIMARY KEY INT UNIQUE NOT NULL,
    IdState INT NOT NULL,
    Name TEXT NOT NULL,

    FOREIGN KEY (IdState) REFERENCES State (IdState)

);

CREATE TABLE IF NOT EXISTS Address (

    IdAddress PRIMARY KEY INT UNIQUE NOT NULL,
    IdCity INT NOT NULL,
    Detail TEXT NOT NULL,

    FOREIGN KEY (IdCity) REFERENCES City (IdCity)

);

CREATE TABLE IF NOT EXISTS Item (
    
    IdItem PRIMARY KEY INT UNIQUE NOT NULL,
    Code TEXT NOT NULL,
    Brand TEXT NOT NULL,
    Descript TEXT NOT NULL,
    Category TEXT NOT NULL,
    Price INT NOT NULL,
    Status INT NOT NULL,
    EntryDate DATE NOT NULL

);

CREATE TABLE IF NOT EXISTS Receipt (

    IdReceipt PRIMARY KEY INT UNIQUE NOT NULL,
    IdEmployee INT NOT NULL,
    Price INT NOT NULL,
    SellingDate DATE NOT NULL

);

CREATE TABLE IF NOT EXISTS ItemReceipt (

    IdItem INT NOT NULL,
    IdReceipt INT NOT NULL,
    Quantity INT NOT NULL,

    FOREIGN KEY (IdItem) REFERENCES Item (IdItem),
    FOREIGN KEY (IdReceipt) REFERENCES Item (IdReceipt)
);

CREATE TABLE IF NOT EXISTS Person (

    IdPerson PRIMARY KEY INT UNIQUE NOT NULL,
    FirstName TEXT NOT NULL,
    MiddleName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    IdentityDoc TEXT NOT NULL,
    IdAddress INT NOT NULL,

    FOREIGN KEY (IdAddress) REFERENCES Address (IdAddress)

);

CREATE TABLE IF NOT EXISTS Employee (
    
    IdPerson INT NOT NULL,
    Status INT NOT NULL,

    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)

);

CREATE TABLE IF NOT EXISTS Customer (

    IdPerson INT NOT NULL,
    Status INT NOT NULL,
    Points INT NOT NULL,

    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)

);

CREATE TABLE IF NOT EXISTS Job (

    IdJob PRIMARY KEY INT UNIQUE NOT NULL,
    Job TEXT NOT NULL,
    Salary INT NOT NULL

);

CREATE TABLE IF NOT EXISTS EmployeeJob (

    IdJob INT NOT NULL,
    IdPerson INT NOT NULL,
    HireDate DATE,

    FOREIGN KEY (IdJob) REFERENCES Job (IdJob),
    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)

);

CREATE TABLE IF NOT EXISTS Shipment (

    IdShipment PRIMARY KEY INT UNIQUE NOT NULL,
    IdWarehouse INT NOT NULL,
    RequestDate DATE NOT NULL,
    DeliveryDate DATE NOT NULL

);

CREATE TABLE IF NOT EXISTS ItemShipment (

    IdShipment INT NOT NULL,
    IdItem INT NOT NULL,

    FOREIGN KEY (IdShipment) REFERENCES Shipment (IdShipment),
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
);

CREATE TABLE IF NOT EXISTS Promo (

    IdPromo PRIMARY KEY INT UNIQUE NOT NULL,
    IdItem INT NOT NULL,
    InitialDateTime DATETIME NOT NULL,
    FinalDateTime DATETIME NOT NULL,
    Percentage INT NOT NULL,

    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)

);