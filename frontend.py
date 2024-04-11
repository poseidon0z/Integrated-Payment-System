import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)


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
        self.office_button = QPushButton("Office")
        self.shop_button = QPushButton("Shop")

        self.main_layout.addWidget(self.bank_button)
        self.main_layout.addWidget(self.office_button)
        self.main_layout.addWidget(self.shop_button)

        self.bank_button.clicked.connect(self.display_bank_functions)
        self.office_button.clicked.connect(self.display_office_functions)
        self.shop_button.clicked.connect(self.display_shop_functions)

    def display_bank_functions(self):
        self.clear_layout()
        self.settransactionbutton()
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
        self.main_layout.addWidget(self.home_button)
        self.home_button.clicked.connect(self.setup_main_window)

    def setregistrationbutton(self):
        self.registration_button = QPushButton("Customer Registration")
        self.main_layout.addWidget(self.registration_button)
        self.registration_button.clicked.connect(
            lambda: print("Registering a new customer")
        )

    def setcheckoutbutton(self):
        self.checkout_button = QPushButton("Checkout")
        self.main_layout.addWidget(self.checkout_button)
        self.checkout_button.clicked.connect(lambda: print("Customer is checking out"))

    def setaddcartbutton(self):
        self.add_to_cart_button = QPushButton("Add to Cart")
        self.main_layout.addWidget(self.add_to_cart_button)
        self.add_to_cart_button.clicked.connect(
            lambda: print("Customer added item to cart")
        )

    def setjobbutton(self):
        self.job_button = QPushButton("Join Job")
        self.main_layout.addWidget(self.job_button)
        self.job_button.clicked.connect(lambda: print("New employee joined"))

    def setpromotionbutton(self):
        self.promotion_button = QPushButton("Get Promotion")
        self.main_layout.addWidget(self.promotion_button)
        self.promotion_button.clicked.connect(lambda: print("Somone got a promotion"))

    def setsalarybutton(self):
        self.salary_button = QPushButton("Get Salary")
        self.main_layout.addWidget(self.salary_button)
        self.salary_button.clicked.connect(lambda: print("Someone got salary"))

    def settransactionbutton(self):
        self.transaction_button = QPushButton("See Transaction History")
        self.main_layout.addWidget(self.transaction_button)
        self.transaction_button.clicked.connect(
            lambda: print("Someone asked transaction history")
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.resize(300, 80)
    sys.exit(app.exec_())
