from PyQt5.QtWidgets import (QApplication, QLabel, QVBoxLayout, QPushButton,
                             QWidget, QFormLayout, QDialog, QDialogButtonBox,
                             QLineEdit, QMainWindow, QToolBar, QStatusBar,
                             QHBoxLayout, QGroupBox, QGridLayout, QFrame,
                             QMenuBar, QAction, QScrollArea, QTextEdit,
                             QTabWidget, QComboBox, QMessageBox)
from PyQt5.QtGui import QPixmap, QFont, QTextDocument
from PyQt5.QtCore import QRect, Qt
from functools import partial
from core import explorer, constants
from core.users import Supplier
import os


class OperatorPanel(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.overview_tab = QWidget()
        self.supplier_approval = QWidget()
        self.product_approval = QWidget()
        self.addTab(self.overview_tab, "Tab 1")
        self.addTab(self.supplier_approval, "Tab 2")
        self.addTab(self.product_approval, "Tab 3")

        self.overview_tab.setLayout(self._create_overview())
        self.setTabText(0, 'Overview')
        self.supplier_approval.setLayout(self._create_approve_supplier())
        self.setTabText(1, 'Supplier Approval')
        self.product_approval.setLayout(self._create_approve_product())
        self.setTabText(2, 'Product Approval')
        self.setStyleSheet('border: 1px solid red; background-color: white;')

    def _create_overview(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_top_part())
        layout.addLayout(self._create_details_part())
        layout.addLayout(self._create_recent_details())
        return layout

    def _create_top_part(self):
        panel_name = QLabel('Operator Panel')

        # buttons
        button_layout = QHBoxLayout()
        new_product_button = QPushButton('Add a Product')
        reports_button = QPushButton('Reports')
        settings_button = QPushButton('Settings')

        hlayout = QHBoxLayout()
        hlayout.addWidget(panel_name)
        button_layout.addWidget(new_product_button)
        button_layout.addWidget(reports_button)
        button_layout.addWidget(settings_button)
        hlayout.addLayout(button_layout)
        hlayout.setStretch(0, 8)
        hlayout.setStretch(1, 2)
        return hlayout

    def _create_details_part(self):
        left_layout = QGridLayout()
        hlayout = QHBoxLayout()

        orders = []
        total_revenue = 0
        sold_items = 0
        unique_product_ids = set()
        dirs = os.listdir(constants.supplier_logs_filepath())
        for d in dirs:
            orders.append(explorer.get_all(os.path.join(constants.supplier_logs_filepath(), d)))
        condition = any(x != [] for x in orders)
        if condition:
            for order in orders:
                for items in order:
                    for item in items['items']:
                        total_revenue += int(item[0]) * int(item[1])
                        sold_items += item[0]
                        unique_product_ids.add(item[2])
        label1 = QLabel('Overall State')
        label1.setAlignment(Qt.AlignCenter)
        label2 = QLabel(f'Total Revenue\n${total_revenue}')
        if not condition:
            label3 = QLabel(f'Total Orders\n0')
        else:
            label3 = QLabel('Total Orders\n' + str(len(orders)))
        label4 = QLabel(f'Items Sold\n{sold_items}')
        label5 = QLabel(f'Unique Items Sold\n{len(unique_product_ids)}')

        for widget in [label5, label4, label1, label3, label2]:
            widget.setStyleSheet('background-color: #cdffc4; font-size: 20px;')
        label1.setStyleSheet('font-weight: bold; font-size: 40px; background-color: #bff0b6;')

        left_layout.addWidget(label1, 0, 0, 1, 4)
        left_layout.addWidget(label2, 1, 0)
        left_layout.addWidget(label3, 1, 1)
        left_layout.addWidget(label4, 1, 2)
        left_layout.addWidget(label5, 1, 3)

        hlayout.addLayout(left_layout)
        hlayout.setContentsMargins(0, 36, 0, 36)
        return hlayout

    def _create_recent_details(self):
        vlayout = QVBoxLayout()
        vlayout.addWidget(QLabel('RECENT TRANSACTIONS'))

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel('Transaction ID'))
        hlayout.addWidget(QLabel('Date'))
        hlayout.addWidget(QLabel('Name'))
        hlayout.addWidget(QLabel('Amount'))
        hlayout.addWidget(QLabel('Status'))
        vlayout.addLayout(hlayout)

        for i in range(5):
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel('98396820825'))
            hlayout.addWidget(QLabel('2020/04/25'))
            hlayout.addWidget(QLabel('Alex Morgan'))
            hlayout.addWidget(QLabel('$1,378'))
            hlayout.addWidget(QLabel('Online'))
            vlayout.addLayout(hlayout)

        return vlayout

    def _create_approve_supplier(self):
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        hlayout.addWidget(QLabel('Transaction ID'))
        hlayout.addWidget(QLabel('Date'))
        hlayout.addWidget(QLabel('Name'))
        hlayout.addWidget(QLabel('Amount'))
        hlayout.addWidget(QLabel('Status'))
        vlayout.addLayout(hlayout)

        unapproved_suppliers = explorer.find_all('is_approved', False, constants.supplier_filepath())

        for idx, supplier in enumerate(unapproved_suppliers):
            frame = QFrame()
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(str(supplier['phone'])))
            hlayout.addWidget(QLabel(supplier['email']))
            hlayout.addWidget(QLabel('Alex Morgan'))
            hlayout.addWidget(QLabel('$1,378'))
            hlayout.addWidget(QLabel('Online'))
            approve_button = QPushButton('Approve')
            approve_button.clicked.connect(partial(self._approve_supplier, supplier['id'], frame))
            hlayout.addWidget(approve_button)
            frame.setLayout(hlayout)
            vlayout.addWidget(frame)
        return vlayout

    def _approve_supplier(self, supplier_id, frame):
        supplier = explorer.search(supplier_id, constants.supplier_filepath())
        supplier['is_approved'] = True
        explorer.overwrite(constants.supplier_filepath(), supplier)
        QMessageBox.about(self, 'Success', 'Supplier approved!')
        frame.hide()

    def _create_approve_product(self):
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        hlayout.addWidget(QLabel('Transaction ID'))
        hlayout.addWidget(QLabel('Date'))
        hlayout.addWidget(QLabel('Name'))
        hlayout.addWidget(QLabel('Amount'))
        hlayout.addWidget(QLabel('Status'))
        vlayout.addLayout(hlayout)

        unapproved_products = explorer.find_all('is_approved', False, constants.product_data_filepath())

        for product in unapproved_products:
            frame = QFrame()
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(product['name']))
            hlayout.addWidget(QLabel(str(product['price'])))
            hlayout.addWidget(QLabel('Alex Morgan'))
            hlayout.addWidget(QLabel('$1,378'))
            hlayout.addWidget(QLabel('Online'))
            approve_button = QPushButton('Approve')
            approve_button.clicked.connect(partial(self._approve_product, product['id'], frame))
            hlayout.addWidget(approve_button)
            frame.setLayout(hlayout)
            vlayout.addWidget(frame)
        return vlayout

    def _approve_product(self, product_id, frame):
        product = explorer.search(product_id, constants.product_data_filepath())
        product['is_approved'] = True
        explorer.overwrite(constants.product_data_filepath(), product)
        frame.hide()
        QMessageBox.about(self, 'Success', 'Product approved!')
