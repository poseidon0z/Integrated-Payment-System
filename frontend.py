import sys
from dbfunctions import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QLabel,
    QDialog,
    QLineEdit,
    QPlainTextEdit,
)


class AadharRegistrationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aadhar Registration")
        self.setModal(True)  # Make it modal to block interactions with parent window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.aadhar_edit = QLineEdit()
        self.aadhar_edit.setPlaceholderText("Enter Aadhar Number")
        layout.addWidget(self.aadhar_edit)

        self.dob_edit = QLineEdit()
        self.dob_edit.setPlaceholderText("Enter Date of Birth")
        layout.addWidget(self.dob_edit)

        self.first_name_edit = QLineEdit()
        self.first_name_edit.setPlaceholderText("Enter First Name")
        layout.addWidget(self.first_name_edit)

        self.last_name_edit = QLineEdit()
        self.last_name_edit.setPlaceholderText("Enter Last Name")
        layout.addWidget(self.last_name_edit)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_registration)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_registration(self):
        aadhar_number = self.aadhar_edit.text()
        dob = self.dob_edit.text()
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()

        if not (aadhar_number and dob and first_name and last_name):
            QMessageBox.critical(self, "Error", "Please provide all inputs.")
            return

        add_aadhar(aadhar_number, dob, first_name, last_name)
        QMessageBox.information(self, "Success", f"Aadhar registered successfully!")

        self.accept()  # Close the dialog


class AccountCreationWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Account Creation")
        self.setModal(True)  # Make it modal to block interactions with parent window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.account_number_edit = QLineEdit()
        self.account_number_edit.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.account_number_edit)

        self.balance_edit = QLineEdit()
        self.balance_edit.setPlaceholderText("Enter Initial Balance")
        layout.addWidget(self.balance_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter Password")
        self.password_edit.setEchoMode(
            QLineEdit.Password
        )  # Show asterisks for password
        layout.addWidget(self.password_edit)

        self.mobile_numbers_edit = QPlainTextEdit()
        self.mobile_numbers_edit.setPlaceholderText(
            "Enter Mobile Numbers (One per line)"
        )
        layout.addWidget(self.mobile_numbers_edit)

        self.owner_aadhar_edit = QLineEdit()
        self.owner_aadhar_edit.setPlaceholderText("Enter Owner's Aadhar Number")
        layout.addWidget(self.owner_aadhar_edit)

        self.nominee_aadhar_edit = QLineEdit()
        self.nominee_aadhar_edit.setPlaceholderText("Enter Nominee's Aadhar Number")
        layout.addWidget(self.nominee_aadhar_edit)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_account_creation)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_account_creation(self):
        account_number = self.account_number_edit.text()
        balance = self.balance_edit.text()
        password = self.password_edit.text()
        owner_aadhar = self.owner_aadhar_edit.text()
        nominee_aadhar = self.nominee_aadhar_edit.text()
        mobile_numbers = self.mobile_numbers_edit.toPlainText().split("\n")

        if not (
            account_number
            and balance
            and password
            and owner_aadhar
            and nominee_aadhar
            and mobile_numbers
        ):
            QMessageBox.critical(self, "Error", "Please provide all inputs.")
            return

        add_account_details(
            int(account_number), int(balance), password, owner_aadhar, nominee_aadhar
        )

        for number in mobile_numbers:
            add_account_contact(account_number, number)

        QMessageBox.information(self, "Success", "Successfully added account")

        self.accept()


class GetBalanceWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Get Account Balance")
        self.setModal(True)  # Make it modal to block interactions with parent window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.account_number_edit = QLineEdit()
        self.account_number_edit.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.account_number_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter Password")
        self.password_edit.setEchoMode(
            QLineEdit.Password
        )  # Show asterisks for password
        layout.addWidget(self.password_edit)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.get_account_balance)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def get_account_balance(self):
        account_number = self.account_number_edit.text()
        password = self.password_edit.text()

        # Validate input
        if not (account_number and password):
            QMessageBox.critical(
                self, "Error", "Please provide both account number and password."
            )
            return

        bal = Fetch_Account_balance(account_number, password)

        QMessageBox.information(self, "Success", f"Balance is {bal}")
        self.accept()  # Close the dialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setup_main_window()

    def setup_main_window(self):
        self.clear_layout()

        self.bank_button = QPushButton("Bank")
        self.bank_button.setIcon(QIcon("./Images/bank.jpeg"))
        self.bank_button.setIconSize(QSize(100, 100))

        self.office_button = QPushButton("Office")
        self.office_button.setIcon(QIcon("./Images/office.png"))
        self.office_button.setIconSize(QSize(100, 100))

        self.shop_button = QPushButton("Shop")
        self.shop_button.setIcon(QIcon("./Images/shop.jpeg"))
        self.shop_button.setIconSize(QSize(100, 100))

        self.main_layout.addWidget(self.bank_button)
        self.main_layout.addWidget(self.office_button)
        self.main_layout.addWidget(self.shop_button)

        self.bank_button.clicked.connect(self.display_bank_functions)
        self.office_button.clicked.connect(self.display_office_functions)
        self.shop_button.clicked.connect(self.display_shop_functions)

    def display_bank_functions(self):
        self.clear_layout()
        self.set_get_balance_button()
        self.settransactionbutton()
        self.setaadharregisterbutton()
        self.set_account_creation_button()
        self.sethomebutton()

    def display_office_functions(self):
        self.clear_layout()
        self.setjobbutton()
        self.setpromotionbutton()
        self.setsalarybutton()
        self.sethomebutton()

    def display_shop_functions(self):
        self.clear_layout()
        self.setregistrationbutton()
        self.setcheckoutbutton()
        self.setaddcartbutton()
        self.sethomebutton()

    def clear_layout(self):
        for i in reversed(range(self.main_layout.count())):
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def sethomebutton(self):
        self.home_button = QPushButton("Home")
        self.home_button.setIcon(QIcon("./Images/home.png"))
        self.home_button.setIconSize(QSize(100, 100))

        self.main_layout.addWidget(self.home_button)
        self.home_button.clicked.connect(self.setup_main_window)

    def setaadharregisterbutton(self):
        self.registration_button = QPushButton("Aadhar Registration")
        self.registration_button.setIcon(QIcon("./Images/register.png"))
        self.registration_button.setIconSize(QSize(100, 100))
        self.registration_button.clicked.connect(self.open_aadhar_registration_window)
        self.main_layout.addWidget(self.registration_button)

    def setregistrationbutton(self):
        self.registration_button = QPushButton("Customer Registration")
        self.registration_button.setIcon(QIcon("./Images/register.png"))
        self.registration_button.setIconSize(QSize(100, 100))
        self.main_layout.addWidget(self.registration_button)
        self.registration_button.clicked.connect(
            lambda: print("Registering a new customer")
        )

    def customerRegistration(self):
        return

    def setcheckoutbutton(self):
        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.setIcon(QIcon("./Images/checkout.png"))
        self.checkout_button.setIconSize(QSize(100, 100))
        self.main_layout.addWidget(self.checkout_button)
        self.checkout_button.clicked.connect(lambda: print("Customer is checking out"))

    def setaddcartbutton(self):
        self.add_to_cart_button = QPushButton("Add to Cart")
        self.add_to_cart_button.setIcon(QIcon("./Images/addtocart.jpeg"))
        self.add_to_cart_button.setIconSize(QSize(100, 100))
        self.main_layout.addWidget(self.add_to_cart_button)
        self.add_to_cart_button.clicked.connect(
            lambda: print("Customer added item to cart")
        )

    def setjobbutton(self):
        self.job_button = QPushButton("Join Job")
        self.job_button.setIcon(QIcon("./Images/joinus.jpeg"))
        self.job_button.setIconSize(QSize(100, 100))
        self.main_layout.addWidget(self.job_button)
        self.job_button.clicked.connect(lambda: print("New employee joined"))

    def setpromotionbutton(self):
        self.promotion_button = QPushButton("Get Promotion")
        self.promotion_button.setIcon(QIcon("./Images/promotion.jpeg"))
        self.promotion_button.setIconSize(QSize(100, 100))
        self.main_layout.addWidget(self.promotion_button)
        self.promotion_button.clicked.connect(lambda: print("Somone got a promotion"))

    def setsalarybutton(self):
        self.salary_button = QPushButton("Get Salary")
        self.salary_button.setIcon(QIcon("./Images/salary.png"))
        self.salary_button.setIconSize(QSize(100, 100))
        self.main_layout.addWidget(self.salary_button)
        self.salary_button.clicked.connect(lambda: print("Someone got salary"))

    def settransactionbutton(self):
        self.transaction_button = QPushButton("See Transaction History")
        self.transaction_button.setIcon(QIcon("./Images/passbook.jpeg"))
        self.transaction_button.setIconSize(QSize(100, 100))

        self.main_layout.addWidget(self.transaction_button)
        self.transaction_button.clicked.connect(
            lambda: print("Someone asked transaction history")
        )

    def set_account_creation_button(self):
        account_creation_button = QPushButton("Account Creation")
        account_creation_button.setIcon(QIcon("./Images/register.png"))
        account_creation_button.setIconSize(QSize(100, 100))
        account_creation_button.clicked.connect(self.open_account_creation_window)
        self.main_layout.addWidget(account_creation_button)

    def set_get_balance_button(self):
        get_balance_button = QPushButton("Get Account Balance")
        get_balance_button.setIcon(QIcon("./Images/ruppee.png"))
        get_balance_button.setIconSize(QSize(100, 100))
        get_balance_button.clicked.connect(self.open_get_balance_window)
        self.main_layout.addWidget(get_balance_button)

    def open_get_balance_window(self):
        dialog = GetBalanceWindow(self)
        if dialog.exec_() == QDialog.Accepted:
            print("Requesting Account Balance")

    def open_account_creation_window(self):
        dialog = AccountCreationWindow(self)
        if dialog.exec_() == QDialog.Accepted:
            print("Account Creation Submitted")

    def open_aadhar_registration_window(self):
        dialog = AadharRegistrationWindow(self)
        if dialog.exec_() == QDialog.Accepted:
            print("Aadhar Registration Submitted")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.resize(300, 80)
    sys.exit(app.exec_())
