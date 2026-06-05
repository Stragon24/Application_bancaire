from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


class TransactionsView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Libellé",
            "Libellé suggéré",
            "Catégorie",
            "Catégorie parent",
            "Montant",
            "Commentaire",
            "Compte"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.table)

        self.setLayout(layout)

    def clear(self):
        self.table.setRowCount(0)

    def add_transaction(self, transaction):

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.table.setItem(
            row, 0,
            QTableWidgetItem(
                str(transaction.get("date", ""))
            )
        )

        self.table.setItem(
            row, 1,
            QTableWidgetItem(
                str(transaction.get("label", ""))
            )
        )

        self.table.setItem(
            row, 2,
            QTableWidgetItem(
                str(transaction.get("suggested_label", ""))
            )
        )

        self.table.setItem(
            row, 3,
            QTableWidgetItem(
                str(transaction.get("category", ""))
            )
        )

        self.table.setItem(
            row, 4,
            QTableWidgetItem(
                str(transaction.get("category_parent", ""))
            )
        )

        self.table.setItem(
            row, 5,
            QTableWidgetItem(
                str(transaction.get("amount", ""))
            )
        )

        self.table.setItem(
            row, 6,
            QTableWidgetItem(
                str(transaction.get("comment", ""))
            )
        )

        self.table.setItem(
            row, 7,
            QTableWidgetItem(
                str(transaction.get("account_label", ""))
            )
        )

    def load_transactions(self, transactions):

        self.clear()

        for transaction in transactions:
            self.add_transaction(transaction)