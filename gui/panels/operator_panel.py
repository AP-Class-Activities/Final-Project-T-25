from functools import partial

from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QPushButton,
                             QWidget, QHBoxLayout, QGridLayout, QFrame,
                             QTabWidget)

from core import explorer, constants


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
        right_layout = QGridLayout()
        hlayout = QHBoxLayout()

        label1 = QLabel('Current Statement')
        label2 = QLabel('$634,000')
        label3 = QLabel('$63,500')
        label4 = QLabel('$1,000,000')

        label5 = QLabel('Current Statement')
        label6 = QLabel('$634,000')
        label7 = QLabel('$63,500')
        label8 = QLabel('$1,000,000')

        left_layout.addWidget(label1, 0, 0, 1, 3)
        left_layout.addWidget(label2, 1, 0)
        left_layout.addWidget(label3, 1, 1)
        left_layout.addWidget(label4, 1, 2)

        right_layout.addWidget(label5, 0, 0, 1, 3)
        right_layout.addWidget(label6, 1, 0)
        right_layout.addWidget(label7, 1, 1)
        right_layout.addWidget(label8, 1, 2)

        hlayout.addLayout(left_layout)
        hlayout.addLayout(right_layout)
        hlayout.setContentsMargins(0, 24, 0, 24)
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
