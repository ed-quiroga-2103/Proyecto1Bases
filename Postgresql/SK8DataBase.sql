-- Entidades 

CREATE TABLE Country (
    IdCountry SERIAL PRIMARY KEY,
    Name VARCHAR NOT NULL
);

CREATE TABLE State (
    IdState SERIAL PRIMARY KEY,
    IdCountry INTEGER NOT NULL,
    Name VARCHAR NOT NULL,
    FOREIGN KEY (IdCountry) REFERENCES Country (IdCountry)
);

CREATE TABLE City (
    IdCity SERIAL PRIMARY KEY,
    IdState INTEGER NOT NULL,
    Name VARCHAR NOT NULL,
    FOREIGN KEY (IdState) REFERENCES State (IdState)
);

CREATE TABLE Address (
    IdAddress SERIAL PRIMARY KEY,
    IdCity INTEGER NOT NULL,
    Detail VARCHAR NOT NULL,
    FOREIGN KEY (IdCity) REFERENCES City (IdCity)
);

CREATE TABLE Person (
    IdPerson SERIAL PRIMARY KEY,
    FirstName VARCHAR NOT NULL,
    MiddleName VARCHAR,
    LastName VARCHAR NOT NULL,
    IdentityDoc VARCHAR NOT NULL,
    IdAddress INTEGER NOT NULL,
    FOREIGN KEY (IdAddress) REFERENCES Address (IdAddress)
);

CREATE TABLE Customer (
    IdPerson INTEGER NOT NULL,
    Status INTEGER NOT NULL,
    Points INTEGER NOT NULL,
    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)
);

CREATE TABLE Employee (
    IdPerson INTEGER NOT NULL,
    Status INTEGER NOT NULL,
    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)
);

CREATE TABLE Job (
    IdJob SERIAL PRIMARY KEY,
    Job VARCHAR NOT NULL,
    Salary INTEGER NOT NULL
);

CREATE TABLE Store (
    IdStore SERIAL PRIMARY KEY,
    Code INTEGER NOT NULL,
    IdAddress INTEGER NOT NULL,
    Status INTEGER NOT NULL,
    IdAdmin INTEGER NOT NULL,
    FOREIGN KEY (IdAddress) REFERENCES Address (IdAddress),
    FOREIGN KEY (IdAdmin) REFERENCES Person (IdPerson)
);

CREATE TABLE Category (
    IdCategory SERIAL PRIMARY KEY,
    Name VARCHAR NOT NULL
);

CREATE TABLE Brand (
    IdBrand SERIAL PRIMARY KEY,
    Name VARCHAR NOT NULL
);

CREATE TABLE Item (
   IdItem SERIAL PRIMARY KEY,
   Code INTEGER NOT NULL,
   IdBrand INTEGER NOT NULL,
   Description VARCHAR NOT NULL,
   IdCategory INTEGER NOT NULL,
   Price INTEGER NOT NULL,
   Status INTEGER,
   EntryDate DATE NOT NULL,
   FOREIGN KEY (IdBrand) REFERENCES Brand (IdBrand),
   FOREIGN KEY (IdCategory) REFERENCES Category (IdCategory)
);

CREATE TABLE Promo (
    IdPromo SERIAL PRIMARY KEY,
    IdStore INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    InitialDateTime timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    FinalDateTime timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    Porcentaje INTEGER NOT NULL
);

CREATE TABLE Shipment (
    IdShipment SERIAL PRIMARY KEY,
    IdStore INTEGER NOT NULL,
    RequestDate DATE NOT NULL,
    DeliveryDate DATE NOT NULL,
    FOREIGN KEY (IdStore) REFERENCES Store (IdStore)
);


CREATE TABLE Payment(

    IdPayment SERIAL PRIMARY KEY NOT NULL,
    Type VARCHAR NOT NULL

);


CREATE TABLE Receipt (
    IdReceipt SERIAL PRIMARY KEY,
    IdEmployee INTEGER NOT NULL, 
    IdPerson INTEGER,
    IdStore INTEGER NOT NULL,
    Price INTEGER NOT NULL,
    IdPayment INTEGER NOT NULL,
    SellingDate timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson),
    FOREIGN KEY (IdStore) REFERENCES Store (IdStore),
    FOREIGN KEY (IdEmployee) REFERENCES Person (IdPerson),
    FOREIGN KEY (IdPayment) REFERENCES Payment (IdPayment)
);

CREATE TABLE StoreRequest (

    IdRequest SERIAL PRIMARY KEY,
    IdStore INTEGER NOT NULL,
    RequestDate timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,

    FOREIGN KEY (IdStore) REFERENCES Store (IdStore)

);

CREATE TABLE WarehouseRequest(

    IdRequest SERIAL PRIMARY KEY,
    RequestDate timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL

);

-- Tablas Cruz

CREATE TABLE StoreRequestItem (

    IdRequest INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    Status INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (IdRequest) REFERENCES StoreRequest (IdRequest),
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)

);

CREATE TABLE WarehouseRequestItem(

    IdRequest INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    Status INTEGER NOT NULL,

    FOREIGN KEY (IdRequest) REFERENCES StoreRequest (IdRequest),
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)

);


CREATE TABLE ItemShipment (
    IdShipment INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    FOREIGN KEY (IdShipment) REFERENCES Shipment (IdShipment),
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
);

CREATE TABLE ItemStore (
    IdStore INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY (IdStore) REFERENCES Store (IdStore),
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
);

CREATE TABLE ItemReceipt (
    IdReceipt INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY (IdReceipt) REFERENCES Receipt (IdReceipt),
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
);

CREATE TABLE ItemWarehouse (
    IdItem INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
);

CREATE TABLE EmployeeJob (
    IdJob INTEGER NOT NULL,
    IdPerson INTEGER NOT NULL,
    IdStore INTEGER NOT NULL,
    HireDate DATE NOT NULL,
    FOREIGN KEY (IdJob) REFERENCES Job (IdJob),
    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson),
    FOREIGN KEY (IdStore) REFERENCES Store (IdStore)
);
 


-- FUNCIONES_________________________________________________________________


CREATE OR REPLACE FUNCTION getItemStore(id INTEGER) 
   RETURNS TABLE (
     IdItem INTEGER,
     Quantity INTEGER
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            ItemStore.IdItem,
            ItemStore.Quantity
        FROM
            Store S
            
        INNER JOIN ItemStore  ON ItemStore.IdStore = S.IdStore
        INNER JOIN Item ON Item.IdItem = ItemStore.IdItem

        WHERE S.IdStore = id AND Item.Status = 1;
END; 
$Body$ 
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION getEmployeeStore(id INTEGER) 
   RETURNS TABLE (
     IdJob INTEGER,
     IdPerson INTEGER,
     HireDate DATE
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            EmployeeJob.IdJob,
            EmployeeJob.IdPerson,
            EmployeeJob.HireDate
        FROM
            Store S
            
        INNER JOIN EmployeeJob ON EmployeeJob.IdStore = S.IdStore
        INNER JOIN Employee ON Employee.IdPerson = EmployeeJob.IdPerson

        WHERE S.IdStore = id AND Employee.Status = 1;
END; 
$Body$ 
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION getPromoStore(id INTEGER) 
   RETURNS TABLE (
     IdPromo INTEGER,
     IdItem INTEGER,
     InitialDateTime DATE,
     FinalDateTime DATE,
     Porcentage INTEGER
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            Promo.IdPromo,
            Promo.IdItem,
            Promo.InitialDateTime,
            Promo.FinalDateTime,
            Promo.Porcentage
        FROM
            Store S
            
        INNER JOIN Promo ON Promo.IdStore = S.IdStore

        WHERE S.IdStore = id;
END; 
$Body$ 
LANGUAGE PLPGSQL;

-- Functions

CREATE OR REPLACE FUNCTION ModifyStatusItem (Id INTEGER,newStatus INTEGER)
RETURNS VOID AS $$
BEGIN

    UPDATE
        Item
    SET
        Status = newStatus
    WHERE
        IdItem = Id;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION InsertPromo (newIdStore INTEGER, newIdItem INTEGER, newInitialDateTime DATE, newFinalDateTime DATE, newPorcentage INTEGER) 
RETURNS VOID AS $$
DECLARE
   newIdPromo  INTEGER := (SELECT IdPromo FROM Promo ORDER BY IdPromo DESC LIMIT 1)+1;
BEGIN
    INSERT INTO Promo VALUES (newIdPromo,newIdStore, newIdItem, newInitialDateTime, newFinalDateTime , newPorcentage);
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION ConsultEmployee(id INTEGER) 
   RETURNS TABLE (
     IdPerson INTEGER,
     Name VARCHAR,
     MiddleName VARCHAR,
     LastName VARCHAR,
     IdentityDoc VARCHAR,
     IdAddress INTEGER,
     Status INTEGER,
     IdJob INTEGER,
     IdStore INTEGER,
     HireDate DATE,
     Job VARCHAR,
     Salary INTEGER
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            P.IdPerson,
            P.FirstName,
            P.MiddleName,
            P.LastName,
            P.IdentityDoc,
            P.IdAddress,
            E.Status,
            EJ.IdJob,
            EJ.IdStore,
            EJ.HireDate,
            J.Job,
            J.Salary
        FROM
            Person P
        INNER JOIN Employee E ON E.IdPerson = P.IdPerson 
        INNER JOIN EmployeeJob EJ ON EJ.IdPerson = E.IdPerson
        INNER JOIN Job J ON EJ.IdJob = J.IdJob
        WHERE
            E.IdPerson = id;
END; 
$Body$ 
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION InsertEmployee (Name VARCHAR,  MiddleName VARCHAR, LastName VARCHAR, IdentityDoc VARCHAR, IdAddress INTEGER,Status INTEGER,IdJob INTEGER,IdStore INTEGER,HireDate Date) 
RETURNS VOID AS $$
DECLARE
   newIdPerson  INTEGER := (SELECT IdPerson FROM Person ORDER BY IdPerson DESC LIMIT 1)+1;
BEGIN
    INSERT INTO Person VALUES (newIdPerson, Name,  MiddleName , LastName , IdentityDoc , IdAddress);
    INSERT INTO Employee VALUES (newIdPerson , Status); 
    INSERT INTO EmployeeJob Values (IdJob, newIdPerson, IdStore, HireDate);
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION ModifyEmployeePerson (Id INTEGER, newName VARCHAR,  newMiddleName VARCHAR, newLastName VARCHAR, newIdentityDoc VARCHAR, newIdAddress INTEGER) 
RETURNS VOID AS $$
BEGIN
    UPDATE
        Person
    SET
        FirstName = newName,
        MiddleName = newMiddleName,
        LastName = newLastName,
        IdentityDoc = newIdentityDoc,
        IdAddress = newIdAddress
    WHERE
        IdPerson = Id;
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION ModifyEmployee (Id INTEGER,newStatus INTEGER) 
RETURNS VOID AS $$
BEGIN
    UPDATE
        Employee
    SET
        Status = newStatus
    WHERE
        IdPerson = Id;
END
$$
LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION InsertStore (code INTEGER, idaddress INTEGER, status INTEGER, idadmin INTEGER) 
RETURNS VOID AS $$
BEGIN
    INSERT INTO Store VALUES ((SELECT IdStore FROM Store ORDER BY IdStore DESC LIMIT 1)+1,code,idaddress,status,idadmin);
END
$$
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION ConsultStore(id INTEGER) 
   RETURNS TABLE (
     IdStore INTEGER,
     Code INTEGER,
     IdAddress INTEGER,
     Status INTEGER,
     IdAdmin INTEGER
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            S.IdStore,
            S.Code,
            S.IdAddress,
            S.Status,
            S.IdAdmin
        FROM
            Store S
        WHERE
            S.IdStore = id;
END; 
$Body$ 
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION ModifyStore (id INTEGER, newcode INTEGER, newidaddress INTEGER, newstatus INTEGER, newidadmin INTEGER) 
RETURNS VOID AS $$
BEGIN
    UPDATE
        Store
    SET
        Code = newcode,
        IdAddress = newidaddress,
        Status = newstatus,
        IdAdmin = newidadmin
    WHERE
        IdStore = id;
END
$$
LANGUAGE PLPGSQL;

-- *
CREATE OR REPLACE FUNCTION getItemStore(id INTEGER) 
   RETURNS TABLE (
     IdItem INTEGER,
     Quantity INTEGER
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            ItemStore.IdItem,
            ItemStore.Quantity
        FROM
            Store S
            
        INNER JOIN ItemStore  ON ItemStore.IdStore = S.IdStore

        WHERE S.IdStore = id;
END; 
$Body$ 
LANGUAGE PLPGSQL;

-- *
CREATE OR REPLACE FUNCTION getEmployeeStore(id INTEGER) 
   RETURNS TABLE (
     IdJob INTEGER,
     IdPerson INTEGER,
     HireDate DATE
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            EmployeeJob.IdJob,
            EmployeeJob.IdPerson,
            EmployeeJob.HireDate
        FROM
            Store S
            
        INNER JOIN EmployeeJob ON EmployeeJob.IdStore = S.IdStore

        WHERE S.IdStore = id;
END; 
$Body$ 
LANGUAGE PLPGSQL;

-- *
CREATE OR REPLACE FUNCTION getPromoStore(id INTEGER) 
   RETURNS TABLE (
     IdPromo INTEGER,
     IdItem INTEGER,
     InitialDateTime DATE,
     FinalDateTime DATE,
     Porcentage INTEGER
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            Promo.IdPromo,
            Promo.IdItem,
            Promo.InitialDateTime,
            Promo.FinalDateTime,
            Promo.Porcentage
        FROM
            Store S
            
        INNER JOIN Promo ON Promo.IdStore = S.IdStore

        WHERE S.IdStore = id;
END; 
$Body$ 
LANGUAGE PLPGSQL;


CREATE OR REPLACE FUNCTION ConsultSales(id INTEGER) 
   RETURNS TABLE (
     IdReceipt INTEGER,
     IdItem INTEGER,
     SellingDate timestamp without time zone,
     Quantiy INTEGER
    ) 
AS $Body$
BEGIN
   RETURN QUERY 
        SELECT 
            Receipt.IdReceipt,
            ItemReceipt.IdItem,
            Receipt.SellingDate,
            ItemReceipt.Quantity
        FROM
            Receipt 
            
        INNER JOIN ItemReceipt ON ItemReceipt.IdReceipt = Receipt.IdReceipt

        WHERE Receipt.IdEmployee = id;
END; 
$Body$ 
LANGUAGE PLPGSQL;
