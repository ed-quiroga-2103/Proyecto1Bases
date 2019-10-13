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

CREATE TABLE Receipt (
    IdReceipt SERIAL PRIMARY KEY,
    IdEmployee INTEGER NOT NULL, 
    IdPerson INTEGER,
    IdStore INTEGER NOT NULL,
    Price INTEGER NOT NULL,
    SellingDate timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,
    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson),
    FOREIGN KEY (IdStore) REFERENCES Store (IdStore),
    FOREIGN KEY (IdEmployee) REFERENCES Person (IdPerson)
);

CREATE TABLE StoreRequest (

    IdRequest SERIAL PRIMARY KEY,
    IdStore INTEGER NOT NULL,
    RequestDate timestamp without time zone DEFAULT ('now'::text)::timestamp(6) with time zone NOT NULL,

    FOREIGN KEY (IdStore) REFERENCES Store (IdStore)

);

-- Tablas Cruz

CREATE TABLE StoreRequestItem (

    IdRequest INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,
    Status INTEGER NOT NULL DEFAULT 0,

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


-- CRUD STORE

-- CREATE OR REPLACE FUNCTION InsertStore (IdStore INTEGER, Code INTEGER, IdAddress INTEGER, Status INTEGER, IdAdmin INTEGER) 
-- RETURNS VOID AS $$
-- BEGIN
--     INSERT INTO Store VALUES (IdStore,Code,IdAddress,Status,IdAdmin);
-- END
-- $$
-- LANGUAGE PLPGSQL;

-- SELECT InsertStore(3,3,1,1,1);

-- CREATE OR REPLACE FUNCTION ConsultStore(id INTEGER) 
--    RETURNS TABLE (
--      IdStore INTEGER,
--      Code INTEGER,
--      IdAddress INTEGER,
--      Status INTEGER,
--      IdAdmin INTEGER
--     ) 
-- AS $Body$
-- BEGIN
--    RETURN QUERY 
--         SELECT 
--             S.IdStore,
--             S.Code,
--             S.IdAddress,
--             S.Status,
--             S.IdAdmin
--         FROM
--             Store S
--         WHERE
--             S.IdStore = id;
-- END; 
-- $Body$ 
-- LANGUAGE PLPGSQL;

-- DROP FUNCTION ConsultStore(id INTEGER);
-- SELECT * FROM ConsultStore(1);


-- CREATE OR REPLACE FUNCTION DropStore (id INTEGER) 
-- RETURNS VOID AS $$
-- BEGIN
--     DELETE FROM Store S
--     WHERE S.IdStore = id;
-- END
-- $$
-- LANGUAGE PLPGSQL;

-- DROP FUNCTION ConsultStore(id INTEGER);
-- SELECT DropStore(3);
-- SELECT * FROM Store;


-- CRUD Employee

-- CREATE OR REPLACE FUNCTION InsertEmployee (IdPerson INTEGER, Name VARCHAR,  MiddleName VARCHAR, LastName VARCHAR, IdentityDoc VARCHAR, IdAddress INTEGER,Status INTEGER) 
-- RETURNS VOID AS $$
-- BEGIN
--     INSERT INTO Person VALUES (IdPerson, Name,  MiddleName , LastName , IdentityDoc , IdAddress);
--     INSERT INTO Employee VALUES (IdPerson , Status); 
-- END
-- $$
-- LANGUAGE PLPGSQL;

-- SELECT InsertEmployee(3,'Eduardo','Quiroga','Alfaro','1-1430-0632',1,1);
-- SELECT * FROM Person;


-- CREATE OR REPLACE FUNCTION ConsultEmployee(id INTEGER) 
--    RETURNS TABLE (
--      IdStore INTEGER,
--      Code INTEGER,
--      IdAddress INTEGER,
--      Status INTEGER,
--      IdAdmin INTEGER
--     ) 
-- AS $Body$
-- BEGIN
--    RETURN QUERY 
--         SELECT 
--             S.IdStore,
--             S.Code,
--             S.IdAddress,
--             S.Status,
--             S.IdAdmin
--         FROM
--             Store S
--         WHERE
--             S.IdStore = id;
-- END; 
-- $Body$ 
-- LANGUAGE PLPGSQL;

-- DROP FUNCTION ConsultStore(id INTEGER);
-- SELECT * FROM ConsultStore(1);




-- DROP ALL
-- DROP TABLE Country CASCADE;
-- DROP TABLE State CASCADE;
-- DROP TABLE Address CASCADE;
-- DROP TABLE Brand CASCADE;
-- DROP TABLE City CASCADE;
-- DROP TABLE Customer CASCADE;
-- DROP TABLE Employee CASCADE;
-- DROP TABLE EmployeeJob CASCADE;
-- DROP TABLE Item CASCADE;
-- DROP TABLE ItemReceipt CASCADE;
-- DROP TABLE ItemShipment CASCADE;
-- DROP TABLE ItemStore CASCADE;
-- DROP TABLE ItemWarehouse CASCADE;
-- DROP TABLE Job CASCADE;
-- DROP TABLE Person CASCADE;
-- DROP TABLE Promo CASCADE;
-- DROP TABLE Receipt CASCADE;
-- DROP TABLE Shipment CASCADE;
-- DROP TABLE Store CASCADE;
