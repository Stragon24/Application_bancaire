from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit
)

from services.database_service import (
    get_available_years,
    get_transactions_by_period
)

from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import Qt


class NumericTableWidgetItem(
    QTableWidgetItem
):

    def __lt__(self, other):

        return (
            self.data(Qt.UserRole)
            <
            other.data(Qt.UserRole)
        )
    

class TransactionsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # =========================
        # FILTRES
        # =========================

        filters_layout = QHBoxLayout()

        filters_layout.addWidget(
            QLabel("Année")
        )

        self.year_combo = QComboBox()

        self.year_combo.currentIndexChanged.connect(
            self.refresh
        )

        filters_layout.addWidget(
            self.year_combo
        )

        filters_layout.addSpacing(20)

        filters_layout.addWidget(
            QLabel("Mois")
        )

        self.month_combo = QComboBox()

        months = [
            "Janvier",
            "Février",
            "Mars",
            "Avril",
            "Mai",
            "Juin",
            "Juillet",
            "Août",
            "Septembre",
            "Octobre",
            "Novembre",
            "Décembre"
        ]

        for i, month in enumerate(months, start=1):

            self.month_combo.addItem(
                month,
                i
            )

        self.month_combo.currentIndexChanged.connect(
            self.refresh
        )

        filters_layout.addWidget(
            self.month_combo
        )

        filters_layout.addSpacing(20)

        self.search_edit = QLineEdit()

        self.search_edit.setPlaceholderText(
            "Rechercher un libellé, une catégorie ou un compte..."
        )

        self.search_edit.textChanged.connect(
            self.refresh
        )

        filters_layout.addWidget(
            self.search_edit
        )

        layout.addLayout(
            filters_layout
        )

        # =========================
        # TABLEAU
        # =========================

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "Date",
            "Libellé",
            "Catégorie",
            "Compte",
            "Montant"
        ])

        self.table.setSortingEnabled(True)

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(
            self.table
        )

        self.setLayout(layout)

        self.load_years()

    def load_years(self):

        self.year_combo.blockSignals(True)

        self.year_combo.clear()

        years = get_available_years()

        for year in years:

            self.year_combo.addItem(
                str(year)
            )

        self.year_combo.blockSignals(False)

        if self.year_combo.count():

            self.year_combo.setCurrentIndex(0)

        self.refresh()

    def refresh(self):

        if self.year_combo.count() == 0:
            return

        year = int(
            self.year_combo.currentText()
        )

        month = self.month_combo.currentData()

        transactions = (
            get_transactions_by_period(
                year,
                month
            )
        )

        search = (
            self.search_edit.text()
            .lower()
            .strip()
        )

        rows = []

        for transaction in transactions:

            if search:

                label = (
                    transaction.label or ""
                ).lower()

                category = (
                    transaction.category or ""
                ).lower()

                account = (
                    transaction.account_label or ""
                ).lower()

                if (
                    search not in label
                    and search not in category
                    and search not in account
                ):
                    continue

            rows.append(
                transaction
            )

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            len(rows)
        )

        for row, transaction in enumerate(rows):

            date_item = QTableWidgetItem(
                transaction.date.strftime(
                    "%d/%m/%Y"
                )
            )

            date_item.setData(
                Qt.UserRole,
                transaction.date
            )

            label_item = QTableWidgetItem(
                transaction.label
            )

            category_item = QTableWidgetItem(
                transaction.category
            )

            account_item = QTableWidgetItem(
                transaction.account_label
            )
            
            amount_item = NumericTableWidgetItem(
                f"{transaction.amount:.2f} €"
            )

            amount_item.setData(
                Qt.UserRole,
                transaction.amount
            )

            if transaction.amount >= 0:

                amount_item.setForeground(
                    QColor("green")
                )

            else:

                amount_item.setForeground(
                    QColor("red")
                )

            self.table.setItem(
                row,
                0,
                date_item
            )

            self.table.setItem(
                row,
                1,
                label_item
            )

            self.table.setItem(
                row,
                2,
                category_item
            )

            self.table.setItem(
                row,
                3,
                account_item
            )

            self.table.setItem(
                row,
                4,
                amount_item
            )

        self.table.resizeColumnsToContents()

        self.table.setSortingEnabled(
            True
        )

        self.table.sortItems(
            0,
            Qt.DescendingOrder
        )