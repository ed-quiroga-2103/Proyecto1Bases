-- CREATE TABLE Warehouse (
--    IdWarehouse INTEGER PRIMARY KEY
-- );

-- CREATE TABLE Shipment (
--     IdShipment INTEGER PRIMARY KEY,
--     IdWarehouse INTEGER NOT NULL,
--     IdStore INTEGER NOT NULL,
--     RequestDate DATE NOT NULL,
--     DeliveryDate DATE NOT NULL,
--     FOREIGN KEY (IdWarehouse) REFERENCES Warehouse (IdWarehouse),
--     FOREIGN KEY (IdStore) REFERENCES Store (IdStore)
-- );

-- CREATE TABLE ItemShipment (
--     IdShipment INTEGER NOT NULL,
--     IdItem INTEGER NOT NULL,
--     FOREIGN KEY (IdShipment) REFERENCES Shipment (IdShipment),
--     FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
-- );

-- CREATE TABLE Item (
--    IdItem INTEGER PRIMARY KEY,
--    Code VARCHAR NOT NULL,
--    Brand VARCHAR NOT NULL,
--    Description VARCHAR NOT NULL,
--    Category VARCHAR NOT NULL,
--    Price INTEGER NOT NULL,
--    Status VARCHAR,
--    EntryDate DATE NOT NULL
-- );

-- CREATE TABLE Promo (
--     IdPromo SERIAL PRIMARY KEY,
--     IdStore INTEGER NOT NULL,
--     IdItem INTEGER NOT NULL,
--     InitialDate DATE NOT NULL,
--     FinalDate DATE NOT NULL,
--     Porcentaje INTEGER NOT NULL
-- );

-- CREATE TABLE Store (
--     IdStore INTEGER PRIMARY KEY,
--     Code VARCHAR NOT NULL,
--     IdAddress INTEGER NOT NULL,
--     Status VARCHAR,
--     IdAdmin INTEGER NOT NULL,
--     IdWarehouse INTEGER NOT NULL,
--     FOREIGN KEY (IdAddress) REFERENCES Address (IdAddress),
--     FOREIGN KEY (IdAdmin) REFERENCES Admin (IdAdmin),
--     FOREIGN KEY (IdWarehouse) REFERENCES Warehouse (IdWarehouse)
-- );

-- CREATE TABLE ItemStore (
--     IdStore INTEGER NOT NULL,
--     IdItem INTEGER NOT NULL,
--     Quantity INTEGER NOT NULL,
--     Details VARCHAR NOT NULL
--     FOREIGN KEY (IdStore) REFERENCES Store (IdStore),
--     FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
-- );

-- CREATE TABLE ItemReceipt (
--     IdReceipt INTEGER NOT NULL,
--     IdItem INTEGER NOT NULL,
--     Quantity INTEGER NOT NULL,
--     FOREIGN KEY (IdReceipt) REFERENCES Receipt (IdReceipt),
--     FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
-- );

-- CREATE TABLE Receipt (
--     IdReceipt INTEGER PRIMARY KEY,
--     IdEmployee INTEGER NOT NULL,
--     IdStore INTEGER NOT NULL,
--     Price INTEGER NOT NULL,
--     SellingDate DATE NOT NULL,
--     FOREIGN KEY (IdEmployee) REFERENCES Employee (IdEmployee),
--     FOREIGN KEY (IdStore) REFERENCES Store (IdStore)
-- );

-- CREATE TABLE ItemWarehouse (
--     IdWarehouse INTEGER NOT NULL,
--     IdItem INTEGER NOT NULL,
--     Quantity INTEGER NOT NULL,
--     FOREIGN KEY (IdWarehouse) REFERENCES Warehouse (IdWarehouse),
--     FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
-- );

-- CREATE TABLE EmployeeStore (
--     IdEmployee INTEGER NOT NULL,
--     IdStore INTEGER NOT NULL,
--     FOREIGN KEY (IdEmployee) REFERENCES Employee (IdEmployee),
--     FOREIGN KEY (IdStore) REFERENCES Store (IdStore)
-- );

-- CREATE TABLE Employee (
--     IdPerson INTEGER NOT NULL,
--     IdStore INTEGER NOT NULL,
--     IdWarehouse INTEGER NOT NULL,
--     Status VARCHAR,
--     FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson),
--     FOREIGN KEY (IdStore) REFERENCES Store (IdStore),
--     FOREIGN KEY (IdWarehouse) REFERENCES Warehouse (IdWarehouse)
-- );

-- CREATE TABLE Person (
--     IdPerson INTEGER PRIMARY KEY,
--     Name VARCHAR NOT NULL,
--     MiddleName VARCHAR NOT NULL,
--     LastName VARCHAR NOT NULL,
--     IdentityDoc VARCHAR NOT NULL,
--     IdAddress INTEGER NOT NULL,
--     FOREIGN KEY (IdAddress) REFERENCES Address (IdAddress)
-- );

-- CREATE TABLE Customer (
--     IdPerson INTEGER NOT NULL,
--     Status VARCHAR NOT NULL,
--     Points INTEGER NOT NULL,
--     FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)
-- );

-- CREATE TABLE EmployeeJob (
--     IdJob INTEGER NOT NULL,
--     IdEmployee INTEGER NOT NULL,
--     HireDate DATE NOT NULL,
--     FOREIGN KEY (IdJob) REFERENCES Job (IdJob),
--     FOREIGN KEY (IdEmployee) REFERENCES Employee (IdEmployee)
-- );

-- CREATE TABLE Job (
--     IdJob INTEGER PRIMARY KEY,
--     Job VARCHAR NOT NULL,
--     Salary INTEGER NOT NULL
-- );

-- CREATE TABLE Address (
--     IdAddress INTEGER PRIMARY KEY,
--     IdCity INTEGER NOT NULL,
--     Detail VARCHAR NOT NULL,
--     FOREIGN KEY (IdCity) REFERENCES City (IdCity)
-- );

-- CREATE TABLE City (
--     IdCity INTEGER PRIMARY KEY,
--     IdState INTEGER NOT NULL,
--     Name VARCHAR NOT NULL,
--     FOREIGN KEY (IdState) REFERENCES State (IdState)
-- );

-- CREATE TABLE State (
--     IdState INTEGER PRIMARY KEY,
--     IdCountry INTEGER NOT NULL,
--     Name VARCHAR NOT NULL,
--     FOREIGN KEY (IdCountry) REFERENCES Country (IdCountry)
-- );

-- CREATE TABLE Country (
--     IdCountry INTEGER PRIMARY KEY,
--     Name VARCHAR NOT NULL,
-- );