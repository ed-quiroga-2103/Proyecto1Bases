CREATE TABLE IF NOT EXISTS Country (

    IdCountry INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(20) NOT NULL

);

CREATE TABLE IF NOT EXISTS State (
    
    IdCountry INTEGER NOT NULL,
    IdState INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(20) NOT NULL,

    FOREIGN KEY (IdCountry) REFERENCES Country (IdCountry) 

);

CREATE TABLE IF NOT EXISTS City (

    IdCity INTEGER PRIMARY KEY UNIQUE NOT NULL,
    IdState INTEGER NOT NULL,
    Name VARCHAR(20)NOT NULL,

    FOREIGN KEY (IdState) REFERENCES State (IdState)

);

CREATE TABLE IF NOT EXISTS Address (

    IdAddress INTEGER PRIMARY KEY UNIQUE NOT NULL,
    IdCity INTEGER NOT NULL,
    Detail VARCHAR(20)NOT NULL,

    FOREIGN KEY (IdCity) REFERENCES City (IdCity)

);


CREATE TABLE IF NOT EXISTS Person (

    IdPerson INTEGER PRIMARY KEY UNIQUE NOT NULL,
    FirstName VARCHAR(20)NOT NULL,
    MiddleName TEXT,
    LastName VARCHAR(20)NOT NULL,
    IdentityDoc VARCHAR(20)NOT NULL,
    IdAddress INTEGER NOT NULL,

    CONSTRAINT addressKey FOREIGN KEY (IdAddress) REFERENCES Address (IdAddress)

);

CREATE TABLE IF NOT EXISTS Category (

    IdCategory INTEGER PRIMARY KEY UNIQUE NOT NULL,
    Name VARCHAR(20)

);

CREATE TABLE IF NOT EXISTS Brand(

    IdBrand INTEGER PRIMARY KEY UNIQUE NOT NULL,
    Name VARCHAR(20) NOT NULL

);

CREATE TABLE IF NOT EXISTS Item (
    
    IdItem INTEGER PRIMARY KEY UNIQUE NOT NULL,
    Code VARCHAR(20) NOT NULL,
    IdBrand INT NOT NULL,
    Descript VARCHAR(20) NOT NULL,
    IdCategory INTEGER NOT NULL,
    Price INTEGER NOT NULL,
    Status INTEGER NOT NULL,
    EntryDate DATE NOT NULL,

    FOREIGN KEY (IdCategory) REFERENCES Category (IdCategory),
    FOREIGN KEY (IdBrand) REFERENCES Brand (IdBrand)

);

CREATE TABLE IF NOT EXISTS ItemStore (

    IdItem INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,

    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)

);


CREATE TABLE Payment(

    IdPayment INTEGER PRIMARY KEY NOT NULL,
    Name VARCHAR(20) NOT NULL

);



CREATE TABLE IF NOT EXISTS Receipt (

    IdReceipt INTEGER PRIMARY KEY UNIQUE NOT NULL AUTO_INCREMENT,
    IdEmployee INTEGER NOT NULL,
    IdCustomer INTEGER,
    Price INTEGER NOT NULL,
    SellingDate DATE NOT NULL,
    IdPayment INTEGER NOT NULL,

    FOREIGN KEY (IdEmployee) REFERENCES Person (IdPerson),
    FOREIGN KEY (IdCustomer) REFERENCES Person (IdPerson)

);

CREATE TABLE IF NOT EXISTS ItemReceipt (

    IdItem INTEGER NOT NULL,
    IdReceipt INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,

    FOREIGN KEY (IdItem) REFERENCES Item (IdItem),
    FOREIGN KEY (IdReceipt) REFERENCES Receipt (IdReceipt)
);



CREATE TABLE IF NOT EXISTS Employee (
    
    IdPerson INTEGER NOT NULL,
    Status INTEGER NOT NULL,

    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)

);

CREATE TABLE IF NOT EXISTS Customer (

    IdPerson INTEGER NOT NULL,
    Status INTEGER NOT NULL,
    Points INTEGER NOT NULL,

    FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)

);

CREATE TABLE IF NOT EXISTS Job (

    IdJob INTEGER PRIMARY KEY UNIQUE NOT NULL,
    Job VARCHAR(20)NOT NULL,
    Salary INTEGER NOT NULL

);

CREATE TABLE IF NOT EXISTS EmployeeJob (

    IdJob INTEGER NOT NULL,
    IdPerson INTEGER NOT NULL,
    HireDate DATE,

    CONSTRAINT jobKey FOREIGN KEY (IdJob) REFERENCES Job (IdJob),
    CONSTRAINT personKey FOREIGN KEY (IdPerson) REFERENCES Person (IdPerson)

);

CREATE TABLE IF NOT EXISTS Shipment (

    IdShipment INTEGER PRIMARY KEY UNIQUE NOT NULL,
    RequestDate DATE NOT NULL,
    DeliveryDate DATE NOT NULL


);

CREATE TABLE IF NOT EXISTS ItemShipment (

    IdShipment INTEGER NOT NULL,
    IdItem INTEGER NOT NULL,

    FOREIGN KEY (IdShipment) REFERENCES Shipment (IdShipment),
    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)
);

CREATE TABLE IF NOT EXISTS Promo (

    IdPromo INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    IdItem INTEGER NOT NULL,
    InitialDateTime DATETIME NOT NULL,
    FinalDateTime DATETIME NOT NULL,
    Percentage INTEGER NOT NULL,

    FOREIGN KEY (IdItem) REFERENCES Item (IdItem)

);  



-- Consulta sobre garantía de un producto_______________________________________________
DELIMITER //
CREATE FUNCTION GarantiaProducto(SellingDate DATE)
RETURNS BOOL
BEGIN
	IF DATEDIFF(DATE(NOW()),SellingDate)> 30 THEN
		RETURN FALSE;
	  END IF;
	  
	IF DATEDIFF(DATE(NOW()),SellingDate)= 30 THEN
		RETURN TRUE;
	  END IF;
	 
	 IF DATEDIFF(DATE(NOW()),SellingDate)< 30 THEN
		RETURN TRUE;
	  END IF;
END //
DELIMITER ;

-- Consulta sobre promociones por fecha y por hora______________________________________

CREATE PROCEDURE PromocionFecha(Fecha DATE)
BEGIN
	SELECT * FROM Promo
    WHERE Fecha = Promo.FinalDateTime
END //
DELIMITER ;

-- Segunda opcion________________________________________________________________________

DELIMITER //
CREATE FUNCTION PromocionFechaHora(FinalDate DATE)
RETURNS BOOL
BEGIN
	IF DATEDIFF(FinalDate,DATE(NOW()))>= 0 THEN
		RETURN TRUE;
	  END IF;
	  
	IF DATEDIFF(FinalDate,DATE(NOW()))< 0 THEN
		RETURN TRUE;
	  END IF;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE PromocionId (Id INTEGER)
	BEGIN
		SELECT IdPromo FROM Promo
		WHERE Id = Promo.IdPromo;
		SELECT PromocionFechaHora(Promo.FinalDateTime);
	END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE SalesReport ()
BEGIN
	SELECT IR.IdReceipt, I.IdItem, B.Name, I.Price, IR.Quantity
	FROM Item I
		INNER JOIN  Brand B ON B.IdBrand = I.IdBrand
		INNER JOIN  ItemReceipt IR ON IR.IdItem = I.IdItem
	ORDER BY IR.Receipt DESC
END //
DELIMITER //


DELIMITER // 
CREATE PROCEDURE PointsReport()
	BEGIN
		SELECT P.IdPerson, P.FirstName, P.MiddleName, P.LastName, P.IdentityDoc, C.Points 
		FROM Person P
		INNER JOIN Customer C ON C.IdPerson = P.IdPerson
		ORDER BY C.Points DESC;
	END //
DELIMITER //

DELIMITER // 
CREATE PROCEDURE ConsultSalesMysql(id INTEGER)
	BEGIN
		SELECT 
             Receipt.IdReceipt,
             ItemReceipt.IdItem,
             Receipt.SellingDate,
             ItemReceipt.Quantity
         FROM
             Receipt 
            
         INNER JOIN ItemReceipt ON ItemReceipt.IdReceipt = Receipt.IdReceipt

         WHERE Receipt.IdEmployee = id

         ORDER BY Receipt.IdEmployee DESC;
	END //
DELIMITER //

