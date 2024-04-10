import oracledb
import json
from datetime import datetime


def setup(cursor):
    creation_queries = [
        """CREATE TABLE Aadhar_Details (
        Aadhar_Number VARCHAR2(15) PRIMARY KEY,
        DOB DATE,
        Last_Name VARCHAR2(15) NOT NULL,
        First_Name VARCHAR2(15) NOT NULL
        )

        """,
        """CREATE TABLE Account_Details (
                Account_Number NUMBER PRIMARY KEY,
                Balance NUMBER NOT NULL,
                Password VARCHAR2(15) NOT NULL,
                Owner_Aadhar VARCHAR2(12) NOT NULL,
                Nominee_Aadhar VARCHAR2(15),
                FOREIGN KEY (Owner_Aadhar) REFERENCES Aadhar_Details(Aadhar_Number)
        )
        """,
        """CREATE TABLE Account_Contacts (
                Account_Number NUMBER NOT NULL,
                Phone_Number NUMBER NOT NULL,
                FOREIGN KEY (Account_Number) REFERENCES Account_Details(Account_Number)
        )
        """,
        """CREATE TABLE Customer_Details (
                Customer_ID VARCHAR2(15) PRIMARY KEY,
                First_Name VARCHAR2(15) NOT NULL,
                Last_Name VARCHAR2(15),
                Middle_Name VARCHAR2(15),
                Mobile_Number NUMBER NOT NULL UNIQUE
        )
        """,
        """CREATE TABLE Purchase_Details (
                Transaction_ID VARCHAR2(30) PRIMARY KEY,
                Customer_ID VARCHAR2(15) NOT NULL,
                Account_Number NUMBER,
                debited_amount NUMBER CHECK (debited_amount > 0),
                voucher_claimed VARCHAR2(10),
                Mode_of_Payment VARCHAR2(10) NOT NULL CHECK (Mode_of_Payment IN ('cash', 'UPI', 'creditCard', 'debitCard')),
                FOREIGN KEY (Customer_ID) REFERENCES Customer_Details(Customer_ID),
                FOREIGN KEY (Account_Number) REFERENCES Account_Details(Account_Number)
        )
        """,
        """CREATE TABLE Shop_Inventory (
                Transaction_ID VARCHAR2(30) NOT NULL,
                Items VARCHAR2(20) NOT NULL,
                FOREIGN KEY (Transaction_ID) REFERENCES Purchase_Details(Transaction_ID)
        )
        """,
        """CREATE TABLE Salary_Details (
                Department VARCHAR2(20) NOT NULL,
                Designation VARCHAR2(20) NOT NULL,
                Salary NUMBER CHECK (Salary > 0)
        )
        """,
        """CREATE TABLE Employee_Details (
                Employee_ID NUMBER PRIMARY KEY,
                Days_Worked NUMBER CHECK (Days_Worked > 0),
                Account_Number NUMBER NOT NULL,
                Designation VARCHAR2(20),
                Department VARCHAR2(20),
                Team VARCHAR2(20)
        )
        """,
        """CREATE TABLE Transaction_Log (
                Account_Number NUMBER NOT NULL,
                Timestamp NUMBER NOT NULL,
                Sender_Receiver NUMBER NOT NULL,
                Credit_Debit CHAR(1) NOT NULL CHECK (Credit_Debit IN ('C', 'D')),
                FOREIGN KEY (Account_Number) REFERENCES Account_Details(Account_Number)
        )""",
    ]
    tables = [
        "Shop_Inventory",
        "Purchase_Details",
        "Customer_Details",
        "Account_Contacts",
        "Employee_Details",
        "Salary_Details",
        "Transaction_Log",
        "Account_Details",
        "Aadhar_Details",
    ]

    for table in tables:
        cursor.execute(
            f"""
            begin
                execute immediate 'drop table {table}';
                exception when others then if sqlcode <> -942 then raise; end if;
            end;"""
        )
    for query in creation_queries:
        cursor.execute(query)


if __name__ == "__main__":
    with open("pass.json") as f:
        pw = json.load(f)["pass"]

    connection = oracledb.connect(user="SYSTEM", password=pw, dsn="localhost/xepdb1")

    print("Successfully connected to Oracle Database")
    cursor = connection.cursor()

    setup(cursor)


def add_aadhar(aadhar_no,date,fname,lname):
    if aadhar_no.isnumeric() and len(aadhar_no)==12 and datetime.strptime(date,"%d-%m-%y") and fname.isalpha() and lname.isalpha():
        try:
                f"""
                cursor.execute("INSERT INTO Aadhar_Details values ({aadhar_no},{date},{lname},{fname}))"""
                cursor.connection.commit()
                # connection.commit()
        except oracledb.IntegrityError as e:
                error_obj, = e.args
                print("Aadhar Number already exists")
                print("Error Code:", error_obj.code)
                print("Error Full Code:", error_obj.full_code)
                print("Error Message:", error_obj.message)
        else:
                print(cursor.rowcount, "record inserted.")
    else:
        print("Values are not in the expected format")

def add_account_details(accno,balance,password,owner_aadhar,nominee):
        if not accno.isnumeric():
                return "Account number is not numeric."
        elif len(accno)<8 or len(accno)>12:
                return "Account number length is invalid (must be between 8 and 12 characters)."
        elif balance<0:
                return "Account balance must be positive."
        elif len(owner_aadhar)!=12 or not owner_aadhar.isnumeric():
                return "Owner's Aadhar number is invalid (must be numeric and 12 characters long)."
        elif len(nominee)!=12 or nominee.isnumeric():
                return "Nominee's Aadhar number is invalid (must be numeric and 12 characters long)."
        else:
                try:
                        f"""
                                cursor.execute("INSERT INTO Account_Details values({accno},{balance},{password},{owner_aadhar},{nominee}))"""
                        cursor.connection.commit()
                        #        connection.commit() 

                except oracledb.IntegrityError as e:
                        error_obj, = e.args
                        print("Account number already exists")
                        print("Error Code:", error_obj.code)
                        print("Error Full Code:", error_obj.full_code)
                        print("Error Message:", error_obj.message)
                else:
                        print(cursor.rowcount, "record inserted.")




