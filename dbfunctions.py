import oracledb
import json
from datetime import datetime
import time


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
                Customer_ID VARCHAR2(15) NULL,  
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


def add_aadhar(aadhar_no, date, fname, lname):
    if not aadhar_no.isnumeric():
        return "Aadhar number is not numeric"
    elif len(aadhar_no) != 12:
        return "Aadhar number length is invalid(must be 12)"
    elif not datetime.strptime(date, "%d-%b-%Y"):
        return "DATE of Birth invalid(must be in DD/MM/YYYY format)"
    elif not fname.isalpha():
        return "Invalid first name"
    elif not lname.isalpha():
        return "Invalid Last name"
    else:
        try:
            cursor.execute(
                f"INSERT INTO Aadhar_Details values ({aadhar_no},'{date.format('%d-%b-%Y')}','{lname}','{fname}')"
            )
            cursor.connection.commit()
            # connection.commit()
        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Aadhar Number already exists")
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def add_account_details(accno, balance, password, owner_aadhar, nominee):
    # if not accno.isnumeric():
    #     return "Account number is not numeric."
    # elif len(accno) < 8 or len(accno) > 12:
    #     return "Account number length is invalid (must be between 8 and 12 characters)."
    if balance < 0:
        return "Account balance must be positive."
    elif len(owner_aadhar) != 12 or not owner_aadhar.isnumeric():
        return (
            "Owner's Aadhar number is invalid (must be numeric and 12 characters long)."
        )
    elif len(nominee) != 12 or not nominee.isnumeric():
        return "Nominee's Aadhar number is invalid (must be numeric and 12 characters long)."
    else:
        try:
            cursor.execute(
                f"INSERT INTO Account_Details values({accno},{balance},'{password}','{owner_aadhar}','{nominee}')"
            )
            cursor.connection.commit()
            #        connection.commit()

        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Account number already exists")
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def add_account_contact(accno, phno):
    # if not accno.isnumeric():
    #         return "Account number is not numeric."
    # elif len(accno)<8 or len(accno)>12:
    #         return "Account number length is invalid (must be between 8 and 12 characters)."
    # if len(phno)!=10:
    #        return "Invalid phone number"

    try:

        cursor.execute(f" INSERT INTO Account_Contacts values({accno},{phno})")
        cursor.connection.commit()
        #        connection.commit()

    except oracledb.IntegrityError as e:
        (error_obj,) = e.args
        print("Account number already exists")
        print("Error Code:", error_obj.code)
        print("Error Full Code:", error_obj.full_code)
        print("Error Message:", error_obj.message)
    else:
        print(cursor.rowcount, "record inserted.")


def add_customer_Details(cid, fname, mname, lname, mno):
    if not cid.isnumeric():
        return "Customer id is not numeric"
    elif len(cid) != 10:
        return "Customer id is invalid (must be of 10 digits)"
    elif not fname.isalpha():
        return "Invalid first name"
    elif not mname.isalpha():
        return "Invalid Middle name"
    elif not lname.isalpha():
        return "Invalid Last name"
    elif not mno.isnumeric():
        return "Mobile Number is not numeric"
    elif len(mno) != 10:
        return "Mobile number should bo of 10 degits "
    else:
        try:
            cursor.execute(
                f"INSERT INTO Customer_Details values('{cid}','{fname}','{mname}','{lname}','{mno}')"
            )
            cursor.connection.commit()
        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Customer ID already exists")
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def add_Purchase_Details(
    tid, cid, accno, debited_amount, voucher_claimed, Mode_of_Payment
):
    if not tid.isnumeric():
        return "Transaction id not numeric"
    elif not cid.isnumeric():
        return "Customer id is not numeric"
    elif len(cid) != 10:
        return "Customer id is invalid (must be of 10 digits)"
    # elif not accno.isnumeric():
    #     return "Account number is not numeric."
    # elif len(accno)<8 or len(accno)>12:
    #     return "Account number length is invalid (must be between 8 and 12 characters)."
    elif debited_amount < 0:
        return "Invalid Amount(Amount should be positive)"
    # elif
    elif Mode_of_Payment not in ["cash", "UPI", "creditCard", "debitCard"]:
        return "mode of payment should either be in cash, UPI, creditCard or debitCard"
    else:
        try:
            cursor.execute(
                f"INSERT INTO Purchase_Details values('{tid}','{cid}',{accno},{debited_amount},'{voucher_claimed}','{Mode_of_Payment}')"
            )
            cursor.connection.commit()
        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Transaction ID already exists")
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def add_Shop_Inventory(tid, Items):
    if not tid.isnumeric():
        return "Transaction id not numeric"
    # elif
    else:
        try:
            cursor.execute(f"INSERT INTO Shop_Inventory values('{tid}','{Items}')")
            cursor.connection.commit()
        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Transaction ID already exists")
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def add_Salary_Details(Dept, Des, Salary):
    if not Dept.isalpha():
        return "Invalid Department"
    elif not Des.isalpha():
        return "Invalid Designation"
    elif Salary < 0:
        return "Invalid Salary (Salary should be positive)"
    else:
        try:
            cursor.execute(
                f"INSERT INTO Salary_Details values('{Dept}','{Des}',{Salary})"
            )
            cursor.connection.commit()
        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def add_Employee_Details(Eid, Days_worked, accno, Des, Dept, Team):
    if Days_worked < 0:
        print("Invalid days worked (no. of days worked should be positive)")
    # elif not accno.isnumeric():
    #     return "Account number is not numeric."
    # elif len(accno)<8 or len(accno)>12:
    #     return "Account number length is invalid (must be between 8 and 12 characters)."
    elif not Dept.isalpha():
        return "Invalid Department"
    elif not Des.isalpha():
        return "Invalid Designation"
    else:
        try:
            cursor.execute(
                f"INSERT INTO Employee_Details values ({Eid},{Days_worked},{accno},'{Des}','{Dept}','{Team}')"
            )
            cursor.connection.commit()
        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Employee ID already exists")
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def add_Transaction_log(accno, send, Cred_debt):
    # here send refers to senders/recievers account number
    if Cred_debt not in ["C", "D"]:
        return "The values should be C(Credit) or D(Debit)"
    else:
        try:
            cursor.execute(
                f"INSERT INTO Transaction_Log values({accno},{time.time()},{send},'{Cred_debt}')"
            )
            cursor.connection.commit()
        except oracledb.IntegrityError as e:
            (error_obj,) = e.args
            print("Employee ID already exists")
            print("Error Code:", error_obj.code)
            print("Error Full Code:", error_obj.full_code)
            print("Error Message:", error_obj.message)
        else:
            print(cursor.rowcount, "record inserted.")


def employee_resign(Eid):
    try:
        cursor.execute(f"DELETE FROM Employee_Details where Employee_ID={Eid}")
        cursor.connection.commit()

    except oracledb.IntegrityError as e:
        (error_obj,) = e.args
        print("Employee ID Does not exist")
        print("Error Code:", error_obj.code)
        print("Error Full Code:", error_obj.full_code)
        print("Error Message:", error_obj.message)
    else:
        print(cursor.rowcount, "record Deleted.")


def customer_withdraw(cid):
    try:
        cursor.execute(
            f"UPDATE Purchase_Details SET Customer_ID=NULL WHERE Customer_ID='{cid}'"
        )
        cursor.connection.commit()
    except oracledb.IntegrityError as e:
        (error_obj,) = e.args
        print("Error updating Purchase_Details:")
        print("Error Code:", error_obj.code)
        print("Error Full Code:", error_obj.full_code)
        print("Error Message:", error_obj.message)
    else:
        print(cursor.rowcount, "record(s) of Purchase_Details updated successfully.")

    try:
        cursor.execute(f"DELETE from Customer_Details where Customer_ID='{cid}'")
        cursor.connection.commit()
    except oracledb.IntegrityError as e:
        (error_obj,) = e.args
        print("Error deleting from Customer_Details:")
        print("Error Code:", error_obj.code)
        print("Error Full Code:", error_obj.full_code)
        print("Error Message:", error_obj.message)
    else:
        print(cursor.rowcount, "record(s) deleted from Customer_Details.")


def Fetch_Account_balance(accno, pw):
    try:
        cursor.execute(
            f"SELECT Account_Number,Balance from Account_Details WHERE Account_Number={accno} AND Password='{pw}'"
        )
        row = cursor.fetchone()
        if row:
            print("Account Number: " + str(row[0]) + "\n" + "Balance: " + str(row[1]))
            return row[1]
        else:
            print("Account Not found or incorrect password")
    except oracledb.IntegrityError as e:
        (error_obj,) = e.args
        print("Error deleting from Customer_Details:")
        print("Error Code:", error_obj.code)
        print("Error Full Code:", error_obj.full_code)
        print("Error Message:", error_obj.message)
    else:
        print(cursor.rowcount, "Account Details successfully fetched.")


def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


with open("pass.json") as f:
    pw = json.load(f)["pass"]

connection = oracledb.connect(user="SYSTEM", password=pw, dsn="localhost/xepdb1")

print("Successfully connected to Oracle Database")
cursor = connection.cursor()

setup(cursor)
add_aadhar("123123123123", "20-Nov-2004", "Adi", "Prabhu")
add_aadhar("123123123124", "07-Sep-2004", "Spu", "Bhat")
add_account_details(12341234, 500, "something", "123123123123", "123123123124")


if __name__ == "__main__":
    with open("pass.json") as f:
        pw = json.load(f)["pass"]

    connection = oracledb.connect(user="SYSTEM", password=pw, dsn="localhost/xepdb1")

    print("Successfully connected to Oracle Database")
    cursor = connection.cursor()

    setup(cursor)
    print(add_aadhar("123123123123", "20-Nov-2004", "Adi", "Prabhu"))
    print(add_aadhar("123123123124", "07-Sep-2004", "Spu", "Bhat"))
    print(add_aadhar("131313131313", "9-Mar-2004", "Venkatsai", "Siri"))
    print(add_aadhar("101010101010", "30-Apr-2005", "Kutta", "Thambi"))
    print(
        add_account_details(12341234, 500, "something", "123123123123", "123123123124")
    )
    print(
        add_account_details(12312312, 1000, "Anything", "131313131313", "101010101010")
    )
    print(add_customer_Details("1111111111", "Spu", "N", "Bhat", "1212121212"))
    print(add_account_contact(12312312, 1122334455))
    print(add_Purchase_Details("1234567891", "1111111111", 12341234, 100, "1", "UPI"))
    print(add_Employee_Details(1, 30, 12341234, "IT", "Manager", "Right"))
    print(add_Salary_Details("IT", "Manager", 45000))
    print(add_Shop_Inventory("1234567891", "Juice"))
    print(add_Transaction_log(12312312, 12341234, "C"))
    print(employee_resign(1))
    print(employee_resign(2))
    [print(row) for row in cursor.execute("SELECT * FROM Purchase_Details")]
    print(customer_withdraw("1111111112"))
    print(Fetch_Account_balance(12312312, "Anything"))
    print(Fetch_Account_balance(12312312, "Aything"))
    [print(row) for row in cursor.execute("SELECT * FROM Purchase_Details")]
    [print(row) for row in cursor.execute("SELECT * FROM Account_Details")]
    [print(row) for row in cursor.execute("SELECT * FROM Employee_Details")]
    print(get_current_time())
