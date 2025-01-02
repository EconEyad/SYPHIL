CREATE TABLE IF NOT EXISTS Buyer (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL,
            Address TEXT NOT NULL,
            Contact_details BIGINT NOT NULL,
            CONSTRAINT buyer_unique_name UNIQUE (Name, Address) 
        );


CREATE TABLE IF NOT EXISTS Printer (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL,
            Address TEXT NOT NULL,
            Contact_details BIGINT NOT NULL,
            CONSTRAINT printer_unique_name UNIQUE (Name, Address) 
        );


CREATE TABLE IF NOT EXISTS Product (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Item_desc TEXT NOT NULL,
            CONSTRAINT product_unique_name UNIQUE (Item_desc) 

        );

CREATE TABLE IF NOT EXISTS Supplier (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL,
            Address TEXT NOT NULL,
            Contact_details BIGINT NOT NULL,
            CONSTRAINT supplier_unique_name UNIQUE (Name, Address) 

        );

CREATE TABLE IF NOT EXISTS Agent (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL,
            CONSTRAINT agent_unique_name UNIQUE (Name) 

        );

CREATE TABLE IF NOT EXISTS Invoice (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Quotation_num TEXT,
            Payment_request_num TEXT DEFAULT NULL,
            Delivery_client_num TEXT DEFAULT NULL,
            Billing_num TEXT DEFAULT NULL,
            Collection_num TEXT DEFAULT NULL,
            Deposit_cheque_num TEXT DEFAULT NULL,
            Status TEXT NOT NULL CHECK(Status IN ('Approved', 'Disapproved'))
        );


CREATE TABLE IF NOT EXISTS Revenue (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            ID_buyer INT NOT NULL REFERENCES Buyer(ID),
            ID_printer INT NOT NULL REFERENCES Printer(ID),
            ID_product INT NOT NULL REFERENCES Product(ID),
            ID_agent INT NOT NULL REFERENCES Agent(ID),
            ID_supplier INT NOT NULL REFERENCES Supplier(ID),
            ID_invoice INT NOT NULL REFERENCES Invoice(ID),
            Price_per_item REAL NOT NULL,
            Cost_per_item REAL NOT NULL,
            Print_per_item REAL NOT NULL,
            Commission_rate REAL NOT NULL,
            Top_up REAL NOT NULL,
            Other_expenses REAL NOT NULL,
            Quantity REAL NOT NULL,
            Production_start_date TEXT DEFAULT NULL,
            Delivery_date TEXT DEFAULT NULL,
            Billing_date TEXT DEFAULT NULL,
            Payment_date TEXT DEFAULT NULL
        )
  