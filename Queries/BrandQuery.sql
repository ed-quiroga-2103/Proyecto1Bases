USE Test1;

CREATE TABLE IF NOT EXISTS Brand(

    IdBrand INTEGER PRIMARY KEY UNIQUE NOT NULL,
    Name VARCHAR(20) NOT NULL

);

INSERT INTO Brand VALUES
(1, 'Ricta'),
(2, 'C1rca'),
(3, 'Polar Skate Co'),
(4, 'Brixton'),
(5, 'Duffs'),
(6, 'Santa Cruz'),
(7, 'Vans'),
(8, 'Palace'),
(9, 'DGK'),
(10, 'Creature'),
(11, 'iPath'),
(12, 'DC Shoes'),
(13, 'Lakai'),
(14, 'HUF'),
(15, 'Chocolate'),
(16, 'Stereo'),
(17, 'Pig Wheels'),
(18, 'Girl'),
(19, 'Venture'),
(20, 'Vision Street Wear'),
(21, 'OJ Wheels'),
(22, 'Macbeth Footwear'),
(23, 'Adidas Skateboarding'),
(24, 'Axion Footwear'),
(25, 'Zoo York');
