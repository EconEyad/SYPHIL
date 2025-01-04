DROP TABLE Revenue;
DROP TABLE Invoice ;
DROP TABLE Agent;
DROP TABLE Supplier;
DROP TABLE Product;
DROP TABLE Printer;
DROP TABLE Buyer;

DELETE FROM Revenue CASCADE;
DELETE FROM Invoice CASCADE;
DELETE FROM Agent CASCADE;
DELETE FROM Supplier CASCADE;
DELETE FROM Product CASCADE;
DELETE FROM Printer CASCADE;
DELETE FROM Buyer CASCADE;

SELECT * FROM Buyer;
SELECT * FROM Printer;
SELECT * FROM Product;
SELECT * FROM Supplier;
SELECT * FROM Agent;
SELECT * FROM Invoice;
SELECT * FROM Revenue;

INSERT INTO Buyer (Name, Address, Contact_details) VALUES ('John Doe', '123 Main St', 1234567890);
INSERT INTO Printer (Name, Address, Contact_details) VALUES ('Printer Company', '456 Market St', 0987654321);
INSERT INTO Product (Item_desc) VALUES ('Product A');
INSERT INTO Supplier (Name, Address, Contact_details) VALUES ('Supplier Co.', '789 Broadway', 5555555555);
INSERT INTO Agent (Name) VALUES ('Agent Smith');


ALTER TABLE invoice 
ADD COLUMN Payment_order text;

ALTER TABLE invoice
ALTER COLUMN Payment_order SET DEFAULT NULL;

INSERT INTO invoice (Payment_order) VALUES ('Q2'), ('Q3'), ('Q4'), ('Q5'), ('Q6');

